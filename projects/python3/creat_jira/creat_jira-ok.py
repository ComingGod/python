
import csv
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from jira import JIRA
import re

# Jira Base URL
JIRA_BASE_URL = "https://jira.sw.nxp.com"

# 必填列
REQUIRED_COLUMNS = ["Summary", "Description", "Issue Type", "Assignee", "project"]

# 可选列（人类可读列名 -> 自动解析字段ID）
OPTIONAL_HUMAN_COLUMNS = ["Story Points", "Start Date", "End Date"]

# Fix Versions 列名支持两种写法
FIX_VERSIONS_COLUMNS = ["Fix Versions", "Fix Version/s"]

# 日期格式
KNOWN_DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%b/%Y",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y/%m/%d",
    "%Y.%m.%d",
]

# ---------------- 工具函数 ----------------
def normalize_date(value: str):
    """把常见日期格式转为 YYYY-MM-DD；解析失败则原样返回。"""
    v = (value or "").strip()
    if not v:
        return None
    for fmt in KNOWN_DATE_FORMATS:
        try:
            dt = datetime.datetime.strptime(v, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return v


def to_number(value: str):
    """把字符串转为数字（float），失败返回 None。"""
    v = (value or "").strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def normalize_name(s: str):
    """字段名标准化（去空格 + 小写），用于匹配 jira.fields() 的名称。"""
    return (s or "").strip().lower()


def connect_jira(username: str, password: str, log):
    try:
        log(f"[INFO] 尝试连接：{JIRA_BASE_URL} 用户名：{username}")
        jira = JIRA(server=JIRA_BASE_URL, basic_auth=(username, password))
        info = jira.server_info()
        log(f"[OK] 连接成功：version={info.get('version')}, deploymentType={info.get('deploymentType')}")
        return jira
    except Exception as e:
        messagebox.showerror("登录失败", f"无法连接 Jira：\n{e}")
        return None


def validate_csv_header(header):
    missing = [c for c in REQUIRED_COLUMNS if c not in (header or [])]
    return missing


def build_field_id_map(jira, log):
    """从 Jira 读取所有字段，构造 名称 -> 字段ID 的映射。"""
    name_to_id = {}
    try:
        fields = jira.fields()
        for f in fields:
            nm = normalize_name(f.get("name"))
            fid = f.get("id")
            if nm and fid:
                name_to_id[nm] = fid
        log(f"[INFO] 已加载 {len(name_to_id)} 个字段映射（name -> id）")
    except Exception as e:
        log(f"[WARN] 加载字段映射失败：{e}")
    return name_to_id


def resolve_optional_field_ids(jira, csv_header, log):
    """把 Story Points / Start Date / End Date 的显示名解析到真实字段 ID。"""
    name_to_id = build_field_id_map(jira, log)
    resolved = {}
    for human_col in OPTIONAL_HUMAN_COLUMNS:
        if human_col in (csv_header or []):
            key = normalize_name(human_col)
            fid = name_to_id.get(key)
            if fid:
                resolved[human_col] = fid
                log(f"[INFO] 字段解析：{human_col} -> {fid}")
            else:
                log(f"[WARN] 未在 Jira 字段中找到 '{human_col}' 的 ID，请确认该显示名与项目一致。")
    return resolved


def parse_fix_versions(text: str):
    """按逗号/分号/竖线分隔版本名，去空白。"""
    if not text:
        return []
    parts = re.split(r"[;,|]", text)
    return [p.strip() for p in parts if p.strip()]

# ---------------- 字段组装（统一在创建后 update） ----------------
def collect_fields_to_update(row: dict, resolved_ids: dict, jira, project_key: str, log):
    """
    汇总所有需要在创建后更新的字段：
    - Story Points / Start Date / End Date（使用解析出的字段ID）
    - Fix Versions（系统字段 fixVersions，强校验：不存在则抛错）
    - 其他 CSV 字段（假定列名已是字段ID或系统字段名）
    返回 dict，可直接用于 issue.update(fields=...)
    """
    fields_update = {}

    # Story Points
    sp_col = "Story Points"
    if sp_col in row and row[sp_col].strip():
        sp_val = to_number(row[sp_col])
        fid = resolved_ids.get(sp_col)
        if not fid:
            log(f"[WARN] 未解析到 Story Points 的字段ID，已跳过。")
        elif sp_val is None:
            log(f"[WARN] Story Points 值不是数字：{row[sp_col]}（已忽略）")
        else:
            fields_update[fid] = sp_val

    # Start Date
    sd_col = "Start Date"
    if sd_col in row and row[sd_col].strip():
        sd_val = normalize_date(row[sd_col])
        fid = resolved_ids.get(sd_col)
        if not fid:
            log(f"[WARN] 未解析到 Start Date 的字段ID，已跳过。")
        elif not sd_val:
            log(f"[WARN] Start Date 无效：{row[sd_col]}（已忽略）")
        else:
            fields_update[fid] = sd_val

    # End Date
    ed_col = "End Date"
    if ed_col in row and row[ed_col].strip():
        ed_val = normalize_date(row[ed_col])
        fid = resolved_ids.get(ed_col)
        if not fid:
            log(f"[WARN] 未解析到 End Date 的字段ID，已跳过。")
        elif not ed_val:
            log(f"[WARN] End Date 无效：{row[ed_col]}（已忽略）")
        else:
            fields_update[fid] = ed_val

    # Fix Versions（系统字段：fixVersions）——强制校验
    fix_col = next((c for c in FIX_VERSIONS_COLUMNS if c in row), None)
    if fix_col and row[fix_col].strip():
        names = parse_fix_versions(row[fix_col])
        if names:
            try:
                versions = jira.project_versions(project_key)
                existing_names = {getattr(v, "name", "").strip() for v in versions}
            except Exception as e:
                # 强制校验：无法获取版本也要报错
                raise RuntimeError(f"获取项目 '{project_key}' 的版本失败：{e}")
            # 找出不存在的版本并报错
            invalid_names = [n for n in names if n not in existing_names]
            if invalid_names:
                raise ValueError(
                    f"Fix Versions 不存在：{', '.join(invalid_names)}（项目={project_key}）。"
                    f"请先在项目版本中创建这些版本或修正 CSV。"
                )
            # 所有版本都合法时才设置
            fields_update["fixVersions"] = [{"name": n} for n in names]

    # 其它自定义字段或系统字段（假定 CSV 列名就是字段ID或合法系统字段名）
    for col, val in row.items():
        if col in REQUIRED_COLUMNS or col in OPTIONAL_HUMAN_COLUMNS or col in FIX_VERSIONS_COLUMNS:
            continue
        v = (val or "").strip()
        if not v:
            continue
        fields_update[col] = v

    return fields_update

# ---------------- 创建与指派 ----------------
def create_and_assign(jira: JIRA, row: dict, row_idx: int, resolved_ids, log):
    summary = (row.get("Summary") or "").strip()
    description = (row.get("Description") or "").strip()
    issuetype = (row.get("Issue Type") or "").strip()
    assignee = (row.get("Assignee") or "").strip()
    project_key = (row.get("project") or "").strip()

    if not summary or not issuetype or not project_key:
        log(f"[WARN] 第 {row_idx} 行缺少必填（Summary/Issue Type/project），跳过")
        return False

    # 创建时只填最小必需字段（避免 createmeta 不兼容）
    fields_create = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issuetype},
    }

    issue = jira.create_issue(fields=fields_create)
    log(f"[OK] 创建成功：{issue.key} | {summary}")

    # 统一在创建后更新其它字段（此处可能抛错：Fix Versions 校验不通过）
    fields_update = collect_fields_to_update(row, resolved_ids, jira, project_key, log)
    if fields_update:
        issue.update(fields=fields_update)
        log(f"[OK] 创建后更新成功：{issue.key} | 更新字段数={len(fields_update)}")

    # 指派
    if assignee:
        try:
            jira.assign_issue(issue.key, assignee)
            log(f"[OK] assign_issue 成功：{issue.key} -> {assignee}")
        except Exception as e:
            log(f"[WARN] assign_issue 失败（{issue.key} -> {assignee}）：{e}")
            # 兜底：某些老版本可用 update 的 name 格式
            try:
                issue.update(assignee={"name": assignee})
                log(f"[OK] issue.update(name) 成功：{issue.key} -> {assignee}")
            except Exception as e2:
                log(f"[ERR] issue.update(name) 也失败：{e2}")
    else:
        log("[INFO] 未提供 Assignee，保持 Unassigned")

    return True


def run(csv_path: str, username: str, password: str, log):
    jira = connect_jira(username, password, log)
    if not jira:
        return

    try:
        # 用 utf-8-sig 兼容 Excel 导出的 CSV（含 BOM）
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames
            miss = validate_csv_header(header)
            if miss:
                messagebox.showerror("CSV 列错误", f"缺少必须列：{', '.join(miss)}\n当前列：{', '.join(header or [])}")
                return

            # 解析人类列名 -> 字段ID（Story Points / Start Date / End Date）
            resolved_ids = resolve_optional_field_ids(jira, header, log)

            total = success = failed = 0
            for i, row in enumerate(reader, start=1):
                total += 1
                try:
                    ok = create_and_assign(jira, row, i, resolved_ids, log)
                    success += 1 if ok else 0
                    failed += 0 if ok else 1
                except Exception as e:
                    # 强制校验生效时，Fix Versions 不存在会走到这里
                    log(f"[ERR] 第 {i} 行失败：{e}")
                    failed += 1

            messagebox.showinfo("完成", f"处理完成：成功 {success}，失败 {failed}，总计 {total}")

    except FileNotFoundError:
        messagebox.showerror("文件错误", f"找不到文件：{csv_path}")
    except UnicodeDecodeError:
        messagebox.showerror("编码错误", "请将 CSV 保存为 UTF-8 或 UTF-8-SIG")
    except Exception as e:
        messagebox.showerror("未知错误", f"处理 CSV 出错：{e}")

# ---------------- GUI ----------------
def main():
    root = tk.Tk()
    root.title("Jira Ticket 批量创建（强制校验 Fix Versions）")
    root.resizable(False, False)

    tk.Label(root, text="CSV 文件路径：").grid(row=0, column=0, padx=10, pady=6, sticky="e")
    ent_csv = tk.Entry(root, width=54)
    ent_csv.grid(row=0, column=1, padx=10, pady=6)

    def choose_csv():
        path = filedialog.askopenfilename(
            title="选择 CSV 文件",
            filetypes=[("CSV 文件", "*.csv"), ("所有文件", "*.*")]
        )
        if path:
            ent_csv.delete(0, tk.END)
            ent_csv.insert(0, path)

    tk.Button(root, text="浏览…", command=choose_csv).grid(row=0, column=2, padx=10, pady=6)

    tk.Label(root, text="Jira 用户名：").grid(row=1, column=0, padx=10, pady=6, sticky="e")
    ent_user = tk.Entry(root, width=54)
    ent_user.grid(row=1, column=1, padx=10, pady=6)

    tk.Label(root, text="Jira 密码：").grid(row=2, column=0, padx=10, pady=6, sticky="e")
    ent_pwd = tk.Entry(root, width=54, show="*")
    ent_pwd.grid(row=2, column=1, padx=10, pady=6)

    tk.Label(root, text="日志：").grid(row=3, column=0, padx=10, pady=6, sticky="ne")
    txt_log = scrolledtext.ScrolledText(root, width=74, height=18, state="disabled")
    txt_log.grid(row=3, column=1, columnspan=2, padx=10, pady=6, sticky="w")

    def log(msg: str):
        txt_log.configure(state="normal")
        txt_log.insert(tk.END, msg + "\n")
        txt_log.see(tk.END)
        txt_log.configure(state="disabled")
        root.update_idletasks()

    def on_submit():
        csv_path = ent_csv.get().strip()
        user = ent_user.get().strip()
        pwd = ent_pwd.get().strip()
        if not csv_path or not user or not pwd:
            messagebox.showerror("缺少信息", "请填写 CSV 路径、用户名和密码")
            return
        log("[INFO] 开始处理…")
        run(csv_path, user, pwd, log)

    tk.Button(root, text="开始提交", command=on_submit).grid(row=4, column=1, pady=10)
    tk.Button(root, text="退出", command=root.destroy).grid(row=4, column=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
