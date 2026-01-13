# -*- coding: utf-8 -*-
import csv
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from jira import JIRA
import re

# ---------------- 基本配置 ----------------
JIRA_BASE_URL = "https://jira.sw.nxp.com"

# CSV 必填列
REQUIRED_COLUMNS = ["Summary", "Description", "Issue Type", "Assignee", "project"]

# 可选“人类列名” -> 自动解析其字段ID（customfield_xxx）
OPTIONAL_HUMAN_COLUMNS = ["Story Points", "Start Date", "End Date"]

# Fix Versions 列名支持两种写法
FIX_VERSIONS_COLUMNS = ["Fix Versions", "Fix Version/s"]

# Dependency 列（大小写不敏感）
DEPENDENCY_COLUMN_NAMES = ["is blocked by", "Is Blocked By", "IS BLOCKED BY"]

# Epic 列（大小写不敏感；也兼容“Epic Link”显示名）
EPIC_COLUMN_CANDIDATES = ["epic", "Epic", "EPIC", "Epic Link"]

# 日期格式
KNOWN_DATE_FORMATS = [
    "%Y-%m-%d",  # 2025-12-17
    "%d/%b/%Y",  # 17/Dec/2025
    "%d/%m/%Y",  # 17/12/2025
    "%m/%d/%Y",  # 12/17/2025
    "%Y/%m/%d",  # 2025/12/17
    "%Y.%m.%d",  # 2025.12.17
]

# ---------- 新增/增强：空白与列名标准化 ----------

def normalize_ws(s: str) -> str:
    """将字符串中的不可断空格等统一为普通空格，压缩连续空白，最后strip+lower。
    处理 NBSP(\u00A0)、Figure space(\u2007)、Narrow NBSP(\u202F) 等。
    """
    if s is None:
        return ""
    # 统一为普通空格
    s = s.replace("\u00A0", " ").replace("\u2007", " ").replace("\u202F", " ")
    # 折叠所有空白
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def normalize_name(s: str):
    """字段名标准化（去异常空白 + 小写）。"""
    return normalize_ws(s)


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


def connect_jira(username: str, password: str, log):
    try:
        log(f"[INFO] 尝试连接：{JIRA_BASE_URL} 用户名：{username}")
        jira = JIRA(server=JIRA_BASE_URL, basic_auth=(username, password))
        info = jira.server_info()
        log(f"[OK] 连接成功: version={info.get('version')}, deploymentType={info.get('deploymentType')}")
        return jira
    except Exception as e:
        messagebox.showerror("登录失败", f"无法连接 Jira：\n{e}")
        return None


def validate_csv_header(header):
    missing = [c for c in REQUIRED_COLUMNS if c not in (header or [])]
    return missing


def build_field_id_map(jira, log=None):
    """从 Jira 读取所有字段，构造 名称->字段ID 的映射。"""
    name_to_id = {}
    fields = jira.fields()
    for f in fields:
        nm = normalize_name(f.get("name"))
        fid = f.get("id")
        if nm and fid:
            name_to_id[nm] = fid
    if log:
        log(f"[INFO] 已加载 {len(name_to_id)} 个字段映射（name -> id）")
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
                log(f"[WARN] 未在 Jira 字段中找到 '{human_col}' 的 ID，请确认显示名与项目一致。")
    return resolved


def resolve_epic_link_field_id(jira, log):
    """解析 'Epic Link' 的字段ID（通常形如 customfield_10014）。"""
    name_to_id = build_field_id_map(jira)
    epic_fid = name_to_id.get("epic link")
    if not epic_fid:
        log("[ERR] 未在 Jira 字段列表中找到 'Epic Link' 的字段ID。")
    return epic_fid


def parse_fix_versions(text: str):
    """按逗号/分号/竖线分隔版本名，去空白。"""
    if not text:
        return []
    parts = re.split(r"[;,\n]", text)
    return [p.strip() for p in parts if p.strip()]


def parse_dependency_keys(text: str):
    """按逗号分隔依赖的 Issue Key，去空白。"""
    if not text:
        return []
    return [k.strip() for k in text.split(",") if k.strip()]


def find_dependency_column(row: dict):
    """在当前行里寻找 dependency 列（大小写/前后与不可见空白容错）。"""
    # 先尝试原始键命中（兼容没有异常空白的情况）
    for cand in DEPENDENCY_COLUMN_NAMES:
        if cand in row:
            return cand
    # 规范化映射：去不可见空白、大小写不敏感
    lower_map = {normalize_ws(k): k for k in row.keys()}
    for cand in DEPENDENCY_COLUMN_NAMES:
        key = normalize_ws(cand)
        if key in lower_map:
            return lower_map[key]
    return None


def find_epic_column(row: dict):
    """在当前行里寻找 epic 列（大小写容错；也兼容 'Epic Link' 列名）。"""
    for cand in EPIC_COLUMN_CANDIDATES:
        if cand in row:
            return cand
    lower_map = {normalize_ws(k): k for k in row.keys()}
    for cand in EPIC_COLUMN_CANDIDATES:
        key = normalize_ws(cand)
        if key in lower_map:
            return lower_map[key]
    return None


# ---------------- 字段组装（统一在创建后 update） ----------------

def collect_fields_to_update(row: dict, resolved_ids: dict, jira, project_key: str, log):
    """
    汇总所有需要在创建后更新的字段（不含 Epic Link，本函数只处理常规字段）：
    - Story Points / Start Date / End Date（使用解析出的字段ID）
    - Fix Versions（系统字段 fixVersions，强校验：不存在则抛错）
    - 其它 CSV 字段（假定列名已是字段ID或系统字段名；排除 dependency/epic 列）

    返回 dict，可直接用于 issue.update(fields=...)
    """
    fields_update = {}

    # Story Points
    sp_col = "Story Points"
    if sp_col in row and (row[sp_col] or "").strip():
        sp_val = to_number(row[sp_col])
        fid = resolved_ids.get(sp_col)
        if not fid:
            log("[WARN] 未解析到 Story Points 的字段ID，已跳过。")
        elif sp_val is None:
            log(f"[WARN] Story Points 值不是数字：{row[sp_col]}（已忽略）")
        else:
            fields_update[fid] = sp_val

    # Start Date
    sd_col = "Start Date"
    if sd_col in row and (row[sd_col] or "").strip():
        sd_val = normalize_date(row[sd_col])
        fid = resolved_ids.get(sd_col)
        if not fid:
            log("[WARN] 未解析到 Start Date 的字段ID，已跳过。")
        elif not sd_val:
            log(f"[WARN] Start Date 无效：{row[sd_col]}（已忽略）")
        else:
            fields_update[fid] = sd_val

    # End Date
    ed_col = "End Date"
    if ed_col in row and (row[ed_col] or "").strip():
        ed_val = normalize_date(row[ed_col])
        fid = resolved_ids.get(ed_col)
        if not fid:
            log("[WARN] 未解析到 End Date 的字段ID，已跳过。")
        elif not ed_val:
            log(f"[WARN] End Date 无效：{row[ed_col]}（已忽略）")
        else:
            fields_update[fid] = ed_val

    # Fix Versions（系统字段：fixVersions）——强制校验
    fix_col = next((c for c in FIX_VERSIONS_COLUMNS if c in row), None)
    if fix_col and (row[fix_col] or "").strip():
        names = parse_fix_versions(row[fix_col])
        if names:
            try:
                versions = jira.project_versions(project_key)
                existing_names = {getattr(v, "name", "").strip() for v in versions}
            except Exception as e:
                # 强制校验：无法获取版本也要报错
                raise RuntimeError(f"获取项目 '{project_key}' 的版本失败：{e}")
            invalid_names = [n for n in names if n not in existing_names]
            if invalid_names:
                raise ValueError(
                    f"Fix Versions 不存在：{', '.join(invalid_names)}（项目={project_key}）。"
                    f"请先在项目版本中创建这些版本或修正 CSV。"
                )
            fields_update["fixVersions"] = [{"name": n} for n in names]

    # 排除 dependency / epic 列，避免把无效键提交给 Jira
    dep_col = find_dependency_column(row)
    epic_col = find_epic_column(row)

    # 兜底：依赖列规范化集合（即使 dep_col 识别失败也能排除）
    dep_norm_set = {normalize_ws(c) for c in DEPENDENCY_COLUMN_NAMES}

    for col, val in row.items():
        if col in REQUIRED_COLUMNS or col in OPTIONAL_HUMAN_COLUMNS or col in FIX_VERSIONS_COLUMNS:
            continue
        if dep_col and col == dep_col:
            continue
        if normalize_ws(col) in dep_norm_set:  # 兜底过滤
            continue
        if epic_col and col == epic_col:
            continue  # Epic Link 另行处理

        v = (val or "").strip()
        if not v:
            continue
        fields_update[col] = v

    return fields_update


# ---------------- Epic 强校验 & 设置（仅当 CSV 提供且非空） ----------------

def precheck_epic_if_present(jira, row: dict, log):
    """
    如果 CSV 存在 epic 列且值非空：
    - 强制检查该工单存在；
    - issuetype 必须为 Epic；
    - 通过后返回 epic_issue 对象；
    否则返回 None（表示忽略，不设置 Epic Link）。
    """
    epic_col = find_epic_column(row)
    epic_value = (row.get(epic_col) if epic_col else "").strip()
    if not epic_value:
        return None  # 未提供或为空 -> 忽略
    try:
        epic_issue = jira.issue(epic_value)
    except Exception as e:
        raise ValueError(f"指定的 Epic 不存在或不可访问：{epic_value}（{e}）")
    epic_name = getattr(epic_issue.fields.issuetype, "name", "")
    if str(epic_name).strip().lower() != "epic":
        raise ValueError(f"指定的工单不是 Epic 类型：{epic_value}（实际：{epic_name}）")
    return epic_issue


def set_epic_link(jira, issue, epic_issue, log):
    """
    为指定 issue 设置 Epic Link。先尝试用 Epic 的 Key，失败再尝试 Issue ID。
    失败则抛异常，让该行记为失败。
    """
    if not epic_issue:
        return
    epic_fid = resolve_epic_link_field_id(jira, log)
    if not epic_fid:
        raise RuntimeError("未找到 'Epic Link' 字段ID，请联系 Jira 管理员在 Create/Edit 屏幕中添加该字段。")
    epic_key = epic_issue.key
    epic_id = epic_issue.id
    # 先尝试 key
    try:
        issue.update(fields={epic_fid: epic_key})
        log(f"[OK] Epic Link 设置成功（key）：{issue.key} -> {epic_key}")
        return
    except Exception as e_key:
        log(f"[WARN] Epic Link 以 Key 设置失败，尝试使用 ID：{e_key}")
    # 再尝试 id
    try:
        issue.update(fields={epic_fid: epic_id})
        log(f"[OK] Epic Link 设置成功（id）：{issue.key} -> {epic_id}")
        return
    except Exception as e_id:
        raise RuntimeError(f"Epic Link 设置失败（{issue.key} -> {epic_key}/{epic_id}）：{e_id}")


# ---------------- 依赖链接 ----------------

def resolve_depends_on_link_type(jira, log):
    """
    寻找 'Blocks' 链接类型，以便在新建票上显示 'is blocked by'。
    - inward == 'is blocked by'（忽略大小写）
    - 或 name == 'Blocks'（忽略大小写）
    返回 (link_type_name, link_type_id) 或 (None, None)
    """
    try:
        types = jira.issue_link_types()
    except Exception as e:
        log(f"[WARN] 获取 Issue Link Types 失败：{e}")
        return (None, None)
    for t in types:
        name = (getattr(t, "name", "") or "").strip()
        inward = (getattr(t, "inward", "") or "").strip().lower()
        if inward == "is blocked by" or name.lower() in ("blocks",):
            tid = getattr(t, "id", None)
            return (name or "Blocks", tid)
    return (None, None)


def apply_dependency_links(jira, issue_key: str, row: dict, log):
    """
    如果 CSV 提供 dependency，则为当前新建工单创建 'depends on' 链接。
    方向：outwardIssue = 新建工单, inwardIssue = 依赖目标工单。
    """
    dep_col = find_dependency_column(row)
    if not dep_col:
        return
    raw = (row.get(dep_col) or "").strip()
    if not raw:
        return
    keys = parse_dependency_keys(raw)
    if not keys:
        return
    link_type_name, link_type_id = resolve_depends_on_link_type(jira, log)
    if not link_type_name and not link_type_id:
        log("[WARN] 未找到 'depends on' 链接类型，已跳过依赖创建。请在 Jira 中配置 Dependency 链接类型。")
        return
    link_type = link_type_name if link_type_name else link_type_id
    for k in keys:
        # 校验目标工单存在
        try:
            _ = jira.issue(k)
        except Exception as e:
            log(f"[ERR] 依赖目标不存在或不可访问：{k}（{e}），已跳过该依赖。")
            continue
        # 创建链接
        try:
            jira.create_issue_link(type=link_type, inwardIssue=k, outwardIssue=issue_key)
            log(f"[OK] 依赖链接创建：{issue_key} is blocked by {k}")
        except Exception as e:
            log(f"[ERR] 依赖链接失败：{issue_key} -> {k}（{e}）")


# ---------------- 创建与指派 ----------------

def create_and_assign(jira: JIRA, row: dict, resolved_ids, log):
    summary = (row.get("Summary") or "").strip()
    description = (row.get("Description") or "").strip()
    issuetype = (row.get("Issue Type") or "").strip()
    assignee = (row.get("Assignee") or "").strip()
    project_key = (row.get("project") or "").strip()

    # Epic：若提供且非空 -> 强校验；若未提供或为空 -> 忽略
    epic_issue = precheck_epic_if_present(jira, row, log)

    if not summary or not issuetype or not project_key:
        log("[WARN] 缺少必填（Summary/Issue Type/project），跳过")
        return False

    # 创建时只填最小必需字段（避免 createmeta 不兼容）
    fields_create = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issuetype},
    }

    issue = jira.create_issue(fields=fields_create)
    log(f"[OK] 创建成功：{issue.key} \n {summary}")

    # 统一在创建后更新其它字段（此处可能抛错：Fix Versions 校验不通过）
    fields_update = collect_fields_to_update(row, resolved_ids, jira, project_key, log)
    if fields_update:
        issue.update(fields=fields_update)
        log(f"[OK] 创建后更新成功：{issue.key} \n 更新字段数={len(fields_update)}")

    # 设置 Epic Link（若提供且非空；当前工单类型不是 Epic 才设置）
    if epic_issue and issuetype.strip().lower() != "epic":
        set_epic_link(jira, issue, epic_issue, log)
    elif epic_issue and issuetype.strip().lower() == "epic":
        log("[WARN] 当前工单类型为 Epic，忽略 Epic Link 设置。")

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

    # 依赖链接（在创建完成后处理）
    apply_dependency_links(jira, issue.key, row, log)

    return True


# ---------------- 主流程 ----------------

def run(csv_path: str, username: str, password: str, log, log_section, ticket_prefix_fn):
    jira = connect_jira(username, password, log)
    if not jira:
        return
    try:
        # 用 utf-8-sig 兼容 Excel 导出的 CSV（含 BOM）
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames
            # 调试输出：显示表头的 repr 便于发现不可见空白
            log(f"[DEBUG] CSV 表头: {[repr(h) for h in (header or [])]}")

            miss = validate_csv_header(header)
            if miss:
                messagebox.showerror("CSV 列错误", f"缺少必需列：{', '.join(miss)}\n当前列：{', '.join(header or [])}")
                return

            # 解析人类列名 -> 字段ID（Story Points / Start Date / End Date）
            resolved_ids = resolve_optional_field_ids(jira, header, log)

            # 统计总行数（为打印 X/N 做准备）
            rows = list(reader)
            total = len(rows)
            success = failed = 0

            for i, row in enumerate(rows, start=1):
                # 章节头：===== Ticket i / N =====
                log_section(i, total)
                # 为当前 Ticket 构造带前缀的日志函数（统一加 [Ti]）
                T = ticket_prefix_fn(i)  # e.g., "[T3]"
                wlog = lambda msg, _T=T: log(f"{_T} {msg}")

                try:
                    ok = create_and_assign(jira, row, resolved_ids, wlog)
                    success += 1 if ok else 0
                    failed += 0 if ok else 1
                except Exception as e:
                    wlog(f"[ERR] 处理失败：{e}")
                    failed += 1

            # 收尾分隔（相邻 ticket 之间的横线）
            log("──────────────────────────────────────────────────────────")
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
    root.title("Jira Ticket 批量创建（Author: Richard）")
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

    # 基础日志函数
    def log(msg: str):
        txt_log.configure(state="normal")
        txt_log.insert(tk.END, msg + "\n")
        txt_log.see(tk.END)
        txt_log.configure(state="disabled")
        root.update_idletasks()

    # 章节分隔（Ticket i / N）
    def log_section(i: int, total: int):
        txt_log.configure(state="normal")
        if i > 1:
            txt_log.insert(tk.END, "\n")
        txt_log.insert(tk.END, f"===== Ticket {i} / {total} =====\n")
        txt_log.configure(state="disabled")
        txt_log.see(tk.END)
        root.update_idletasks()

    # 生成当前 Ticket 的前缀，例如 [T3]
    def ticket_prefix_fn(i: int) -> str:
        return f"[T{i}]"

    # 清空日志
    def clear_log():
        txt_log.configure(state="normal")
        txt_log.delete("1.0", tk.END)
        txt_log.insert(tk.END, "[INFO] 已清空日志\n")
        txt_log.configure(state="disabled")
        txt_log.see(tk.END)

    def on_submit():
        csv_path = ent_csv.get().strip()
        user = ent_user.get().strip()
        pwd = ent_pwd.get().strip()
        if not csv_path or not user or not pwd:
            messagebox.showerror("缺少信息", "请填写 CSV 路径、用户名和密码")
            return
        log("[INFO] 开始处理…")
        run(csv_path, user, pwd, log, log_section, ticket_prefix_fn)

    # 操作按钮
    btn_frame = tk.Frame(root)
    btn_frame.grid(row=4, column=1, columnspan=2, pady=10)
    tk.Button(btn_frame, text="开始提交", command=on_submit, width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="清空日志", command=clear_log, width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="退出", command=root.destroy, width=12).grid(row=0, column=2, padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()
