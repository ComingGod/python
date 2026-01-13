# import csv
# import sys
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# from jira import JIRA

# # 候选 Base URL（先试带 /jira，再试不带）
# CANDIDATE_BASE_URLS = [
#     "https://jira.sw.nxp.com/jira",
#     "https://jira.sw.nxp.com",
# ]

# REQUIRED_COLUMNS = ["Summary", "Description", "Issue Type", "Reporter", "Assignee", "project"]

# def validate_csv_header(header):
#     missing = [col for col in REQUIRED_COLUMNS if col not in header]
#     return missing

# def try_connect(base_url, username, password, log_fn):
#     try:
#         log_fn(f"[INFO] 尝试连接：{base_url} 用户名：{username}")
#         jira = JIRA(server=base_url, basic_auth=(username, password))
#         info = jira.server_info()
#         log_fn(f"[OK] 连接成功：version={info.get('version')}, deploymentType={info.get('deploymentType')}")
#         return jira, base_url
#     except Exception as e:
#         msg = str(e)
#         if "<html" in msg.lower() or "doctype" in msg.lower() or "dead link" in msg.lower():
#             log_fn(f"[ERR] 收到 HTML（疑似跳登录页），REST 未命中：{base_url}")
#         else:
#             log_fn(f"[ERR] 连接失败：{base_url} | {e}")
#         return None, None

# def connect_jira(username, password, log_fn):
#     for base in CANDIDATE_BASE_URLS:
#         jira, ok_base = try_connect(base, username, password, log_fn)
#         if jira:
#             return jira, ok_base
#     messagebox.showerror("登录失败", "无法连接 Jira REST API，请检查：\n1) URL 是否正确\n2) 用户名/密码是否有效\n3) VPN是否连接")
#     return None, None

# def create_jira_tickets(csv_file, username, password, log_fn):
#     jira, base_url = connect_jira(username, password, log_fn)
#     if not jira:
#         return

#     try:
#         with open(csv_file, newline="", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             header = reader.fieldnames or []
#             missing = validate_csv_header(header)
#             if missing:
#                 messagebox.showerror("CSV 列错误", f"缺少必须列：{', '.join(missing)}\n当前列：{', '.join(header)}")
#                 return

#             total = success = failed = 0

#             for row in reader:
#                 total += 1
#                 summary = (row.get("Summary") or "").strip()
#                 description = (row.get("Description") or "").strip()
#                 issue_type = (row.get("Issue Type") or "").strip()
#                 assignee = (row.get("Assignee") or "").strip()
#                 project_key = (row.get("project") or "").strip()

#                 if not summary or not issue_type or not project_key:
#                     log_fn(f"[WARN] 第 {total} 行缺少必填字段，已跳过")
#                     failed += 1
#                     continue

#                 # 基础字段
#                 fields = {
#                     "project": {"key": project_key},
#                     "summary": summary,
#                     "description": description,
#                     "issuetype": {"name": issue_type},
#                 }

#                 # 动态添加 CSV 中的其他列（处理必填自定义字段）
#                 for col in row:
#                     if col not in REQUIRED_COLUMNS and row[col].strip():
#                         fields[col] = row[col].strip()

#                 try:
#                     issue = jira.create_issue(fields=fields)
#                     log_fn(f"[OK] 创建成功：{issue.key} | {summary}")
#                     success += 1

#                     # 创建后分配 Assignee
#                     if assignee:
#                         try:
#                             jira.assign_issue(issue.key, assignee)
#                             log_fn(f"[OK] 指派成功：{assignee} -> {issue.key}")
#                         except Exception as ae:
#                             log_fn(f"[WARN] 指派失败：{assignee} -> {issue.key} | {ae}")

#                 except Exception as e:
#                     log_fn(f"[ERR] 创建失败（第 {total} 行）：{summary} | 错误：{e}")
#                     failed += 1

#             messagebox.showinfo("完成", f"处理完成：成功 {success}，失败 {failed}，总计 {total}")

#     except FileNotFoundError:
#         messagebox.showerror("文件错误", f"找不到文件：{csv_file}")
#     except UnicodeDecodeError:
#         messagebox.showerror("编码错误", "请将 CSV 保存为 UTF-8")
#     except Exception as e:
#         messagebox.showerror("未知错误", f"处理 CSV 出错：{e}")

# # ---------------- GUI ----------------

# def main():
#     root = tk.Tk()
#     root.title("Jira Ticket 自动创建工具（用户名+密码）")
#     root.resizable(False, False)

#     tk.Label(root, text="CSV 文件路径：").grid(row=0, column=0, padx=10, pady=6, sticky="e")
#     csv_entry = tk.Entry(root, width=54)
#     csv_entry.grid(row=0, column=1, padx=10, pady=6)

#     def select_csv():
#         path = filedialog.askopenfilename(title="选择 CSV 文件", filetypes=[("CSV 文件", "*.csv"), ("所有文件", "*.*")])
#         if path:
#             csv_entry.delete(0, tk.END)
#             csv_entry.insert(0, path)
#     tk.Button(root, text="浏览…", command=select_csv).grid(row=0, column=2, padx=10, pady=6)

#     tk.Label(root, text="Jira 用户名：").grid(row=1, column=0, padx=10, pady=6, sticky="e")
#     username_entry = tk.Entry(root, width=54)
#     username_entry.grid(row=1, column=1, padx=10, pady=6)

#     tk.Label(root, text="Jira 密码：").grid(row=2, column=0, padx=10, pady=6, sticky="e")
#     password_entry = tk.Entry(root, width=54, show="*")
#     password_entry.grid(row=2, column=1, padx=10, pady=6)

#     tk.Label(root, text="日志：").grid(row=3, column=0, padx=10, pady=6, sticky="ne")
#     log_box = scrolledtext.ScrolledText(root, width=74, height=18, state="disabled")
#     log_box.grid(row=3, column=1, columnspan=2, padx=10, pady=6, sticky="w")

#     def append_log(text):
#         log_box.configure(state="normal")
#         log_box.insert(tk.END, text + "\n")
#         log_box.see(tk.END)
#         log_box.configure(state="disabled")
#         root.update_idletasks()

#     def submit():
#         csv_path = csv_entry.get().strip()
#         username = username_entry.get().strip()
#         password = password_entry.get().strip()

#         if not csv_path or not username or not password:
#             messagebox.showerror("缺少信息", "请填写 CSV 路径、用户名和密码")
#             return

#         append_log("[INFO] 开始处理…")
#         create_jira_tickets(csv_path, username, password, append_log)

#     tk.Button(root, text="开始提交", command=submit).grid(row=4, column=1, pady=10)
#     tk.Button(root, text="退出", command=root.destroy).grid(row=4, column=2, pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     main()


############################################################################################################################################





############################################################################################################################################


# import csv
# import sys
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# from jira import JIRA

# # 候选 Base URL
# CANDIDATE_BASE_URLS = [
#     "https://jira.sw.nxp.com/jira",
#     "https://jira.sw.nxp.com",
# ]

# REQUIRED_COLUMNS = ["Summary", "Description", "Issue Type", "Reporter", "Assignee", "project"]

# def validate_csv_header(header):
#     missing = [col for col in REQUIRED_COLUMNS if col not in header]
#     return missing

# def try_connect(base_url, username, password, log_fn):
#     try:
#         log_fn(f"[INFO] 尝试连接：{base_url} 用户名：{username}")
#         jira = JIRA(server=base_url, basic_auth=(username, password))
#         info = jira.server_info()
#         log_fn(f"[OK] 连接成功：version={info.get('version')}, deploymentType={info.get('deploymentType')}")
#         return jira, base_url
#     except Exception as e:
#         msg = str(e)
#         if "<html" in msg.lower() or "doctype" in msg.lower() or "dead link" in msg.lower():
#             log_fn(f"[ERR] 收到 HTML（疑似跳登录页），REST 未命中：{base_url}")
#         else:
#             log_fn(f"[ERR] 连接失败：{base_url} | {e}")
#         return None, None

# def connect_jira(username, password, log_fn):
#     for base in CANDIDATE_BASE_URLS:
#         jira, ok_base = try_connect(base, username, password, log_fn)
#         if jira:
#             return jira, ok_base
#     messagebox.showerror("登录失败", "无法连接 Jira REST API，请检查：\n1) URL 是否正确\n2) 用户名/密码是否有效\n3) VPN是否连接")
#     return None, None

# def assign_issue_safely(jira, issue, assignee_input, log_fn):
#     if not assignee_input:
#         log_fn("[INFO] 未提供 Assignee，跳过指派")
#         return

#     name = None
#     try:
#         candidates = jira.search_users(query=assignee_input, maxResults=5)
#         if candidates:
#             u = candidates[0]
#             name = getattr(u, 'name', None) or getattr(u, 'key', None)
#             log_fn(f"[INFO] 用户解析：输入={assignee_input} -> 使用 name={name or assignee_input}")
#     except Exception as e:
#         log_fn(f"[WARN] search_users 失败：{e}，将直接使用输入值进行指派")

#     try:
#         jira.assign_issue(issue.key, name or assignee_input)
#         log_fn(f"[OK] assign_issue 成功：{issue.key} -> {name or assignee_input}")
#         return
#     except Exception as e:
#         log_fn(f"[WARN] assign_issue 失败：{e}")

#     try:
#         issue.update(assignee={"name": name or assignee_input})
#         log_fn(f"[OK] issue.update(name) 成功：{issue.key} -> {name or assignee_input}")
#         return
#     except Exception as e2:
#         log_fn(f"[ERR] issue.update(name) 也失败：{e2}")
#         log_fn("[ERR] 指派未成功，请检查权限、工作流或项目设置。")

# def create_jira_tickets(csv_file, username, password, log_fn):
#     jira, base_url = connect_jira(username, password, log_fn)
#     if not jira:
#         return

#     try:
#         with open(csv_file, newline="", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             header = reader.fieldnames or []
#             missing = validate_csv_header(header)
#             if missing:
#                 messagebox.showerror("CSV 列错误", f"缺少必须列：{', '.join(missing)}\n当前列：{', '.join(header)}")
#                 return

#             total = success = failed = 0

#             for row in reader:
#                 total += 1
#                 summary = (row.get("Summary") or "").strip()
#                 description = (row.get("Description") or "").strip()
#                 issue_type = (row.get("Issue Type") or "").strip()
#                 assignee = (row.get("Assignee") or "").strip()
#                 project_key = (row.get("project") or "").strip()

#                 if not summary or not issue_type or not project_key:
#                     log_fn(f"[WARN] 第 {total} 行缺少必填字段，已跳过")
#                     failed += 1
#                     continue

#                 fields = {
#                     "project": {"key": project_key},
#                     "summary": summary,
#                     "description": description,
#                     "issuetype": {"name": issue_type},
#                 }

#                 # 动态添加 CSV 中的额外列（处理必填自定义字段）
#                 for col in row:
#                     if col not in REQUIRED_COLUMNS and row[col].strip():
#                         fields[col] = row[col].strip()

#                 try:
#                     issue = jira.create_issue(fields=fields)
#                     log_fn(f"[OK] 创建成功：{issue.key} | {summary}")
#                     success += 1

#                     # 创建后指派
#                     assign_issue_safely(jira, issue, assignee, log_fn)

#                 except Exception as e:
#                     log_fn(f"[ERR] 创建失败（第 {total} 行）：{summary} | 错误：{e}")
#                     failed += 1

#             messagebox.showinfo("完成", f"处理完成：成功 {success}，失败 {failed}，总计 {total}")

#     except FileNotFoundError:
#         messagebox.showerror("文件错误", f"找不到文件：{csv_file}")
#     except UnicodeDecodeError:
#         messagebox.showerror("编码错误", "请将 CSV 保存为 UTF-8")
#     except Exception as e:
#         messagebox.showerror("未知错误", f"处理 CSV 出错：{e}")

# # ---------------- GUI ----------------

# def main():
#     root = tk.Tk()
#     root.title("Jira Ticket 自动创建工具（用户名+密码）")
#     root.resizable(False, False)

#     tk.Label(root, text="CSV 文件路径：").grid(row=0, column=0, padx=10, pady=6, sticky="e")
#     csv_entry = tk.Entry(root, width=54)
#     csv_entry.grid(row=0, column=1, padx=10, pady=6)

#     def select_csv():
#         path = filedialog.askopenfilename(title="选择 CSV 文件", filetypes=[("CSV 文件", "*.csv"), ("所有文件", "*.*")])
#         if path:
#             csv_entry.delete(0, tk.END)
#             csv_entry.insert(0, path)
#     tk.Button(root, text="浏览…", command=select_csv).grid(row=0, column=2, padx=10, pady=6)

#     tk.Label(root, text="Jira 用户名：").grid(row=1, column=0, padx=10, pady=6, sticky="e")
#     username_entry = tk.Entry(root, width=54)
#     username_entry.grid(row=1, column=1, padx=10, pady=6)

#     tk.Label(root, text="Jira 密码：").grid(row=2, column=0, padx=10, pady=6, sticky="e")
#     password_entry = tk.Entry(root, width=54, show="*")
#     password_entry.grid(row=2, column=1, padx=10, pady=6)

#     tk.Label(root, text="日志：").grid(row=3, column=0, padx=10, pady=6, sticky="ne")
#     log_box = scrolledtext.ScrolledText(root, width=74, height=18, state="disabled")
#     log_box.grid(row=3, column=1, columnspan=2, padx=10, pady=6, sticky="w")

#     def append_log(text):
#         log_box.configure(state="normal")
#         log_box.insert(tk.END, text + "\n")
#         log_box.see(tk.END)
#         log_box.configure(state="disabled")
#         root.update_idletasks()

#     def submit():
#         csv_path = csv_entry.get().strip()
#         username = username_entry.get().strip()
#         password = password_entry.get().strip()

#         if not csv_path or not username or not password:
#             messagebox.showerror("缺少信息", "请填写 CSV 路径、用户名和密码")
#             return

#         append_log("[INFO] 开始处理…")
#         create_jira_tickets(csv_path, username, password, append_log)

#     tk.Button(root, text="开始提交", command=submit).grid(row=4, column=1, pady=10)
#     tk.Button(root, text="退出", command=root.destroy).grid(row=4, column=2, pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     main()



# import csv
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# from jira import JIRA

# # 固定为你环境命中的 Base URL（不带 /jira）
# JIRA_BASE_URL = "https://jira.sw.nxp.com"

# # CSV 必须包含的列
# REQUIRED_COLUMNS = ["Summary", "Description", "Issue Type", "Reporter", "Assignee", "project"]

# def validate_csv_header(header):
#     missing = [c for c in REQUIRED_COLUMNS if c not in (header or [])]
#     return missing

# def connect_jira(username: str, password: str, log):
#     try:
#         log(f"[INFO] 尝试连接：{JIRA_BASE_URL} 用户名：{username}")
#         jira = JIRA(server=JIRA_BASE_URL, basic_auth=(username, password))
#         info = jira.server_info()
#         log(f"[OK] 连接成功：version={info.get('version')}, deploymentType={info.get('deploymentType')}")
#         return jira
#     except Exception as e:
#         messagebox.showerror("登录失败", f"无法连接 Jira：{e}")
#         return None

# def create_and_assign(jira: JIRA, row: dict, row_idx: int, log):
#     summary     = (row.get("Summary") or "").strip()
#     description = (row.get("Description") or "").strip()
#     issuetype   = (row.get("Issue Type") or "").strip()
#     assignee    = (row.get("Assignee") or "").strip()
#     project_key = (row.get("project") or "").strip()

#     if not summary or not issuetype or not project_key:
#         log(f"[WARN] 第 {row_idx} 行缺少必填（Summary/Issue Type/project），跳过")
#         return False

#     # 基础创建字段
#     fields = {
#         "project": {"key": project_key},
#         "summary": summary,
#         "description": description,
#         "issuetype": {"name": issuetype},
#         # 不设置 reporter，由系统自动确定
#     }

#     # 附带 CSV 里的其它列（自定义字段等）
#     for col, val in row.items():
#         if col in REQUIRED_COLUMNS: 
#             continue
#         v = (val or "").strip()
#         if v:
#             fields[col] = v

#     # 创建
#     issue = jira.create_issue(fields=fields)
#     log(f"[OK] 创建成功：{issue.key} | {summary}")

#     # 创建后直接指派（Server 环境可用登录名）
#     if assignee:
#         try:
#             jira.assign_issue(issue.key, assignee)  # 例如 "nxa28190"
#             log(f"[OK] assign_issue 成功：{issue.key} -> {assignee}")
#         except Exception as e:
#             log(f"[WARN] assign_issue 失败（{issue.key} -> {assignee}）：{e}")
#     else:
#         log("[INFO] 未提供 Assignee，保持 Unassigned")

#     return True

# def run(csv_path: str, username: str, password: str, log):
#     jira = connect_jira(username, password, log)
#     if not jira:
#         return

#     try:
#         with open(csv_path, newline="", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             header = reader.fieldnames
#             miss = validate_csv_header(header)
#             if miss:
#                 messagebox.showerror("CSV 列错误", f"缺少必须列：{', '.join(miss)}\n当前列：{', '.join(header or [])}")
#                 return

#             total = success = failed = 0
#             for i, row in enumerate(reader, start=1):
#                 total += 1
#                 try:
#                     ok = create_and_assign(jira, row, i, log)
#                     success += 1 if ok else 0
#                     failed  += 0 if ok else 1
#                 except Exception as e:
#                     log(f"[ERR] 第 {i} 行失败：{e}")
#                     failed += 1

#             messagebox.showinfo("完成", f"处理完成：成功 {success}，失败 {failed}，总计 {total}")
#     except FileNotFoundError:
#         messagebox.showerror("文件错误", f"找不到文件：{csv_path}")
#     except UnicodeDecodeError:
#         messagebox.showerror("编码错误", "请将 CSV 保存为 UTF-8")
#     except Exception as e:
#         messagebox.showerror("未知错误", f"处理 CSV 出错：{e}")

# # ---------------- GUI ----------------

# def main():
#     root = tk.Tk()
#     root.title("Jira Ticket 批量创建（Server / Basic Auth）")
#     root.resizable(False, False)

#     tk.Label(root, text="CSV 文件路径：").grid(row=0, column=0, padx=10, pady=6, sticky="e")
#     ent_csv = tk.Entry(root, width=54)
#     ent_csv.grid(row=0, column=1, padx=10, pady=6)

#     def choose_csv():
#         path = filedialog.askopenfilename(title="选择 CSV 文件",
#                                           filetypes=[("CSV 文件", "*.csv"), ("所有文件", "*.*")])
#         if path:
#             ent_csv.delete(0, tk.END)
#             ent_csv.insert(0, path)
#     tk.Button(root, text="浏览…", command=choose_csv).grid(row=0, column=2, padx=10, pady=6)

#     tk.Label(root, text="Jira 用户名：").grid(row=1, column=0, padx=10, pady=6, sticky="e")
#     ent_user = tk.Entry(root, width=54)
#     ent_user.grid(row=1, column=1, padx=10, pady=6)

#     tk.Label(root, text="Jira 密码：").grid(row=2, column=0, padx=10, pady=6, sticky="e")
#     ent_pwd = tk.Entry(root, width=54, show="*")
#     ent_pwd.grid(row=2, column=1, padx=10, pady=6)

#     tk.Label(root, text="日志：").grid(row=3, column=0, padx=10, pady=6, sticky="ne")
#     txt_log = scrolledtext.ScrolledText(root, width=74, height=18, state="disabled")
#     txt_log.grid(row=3, column=1, columnspan=2, padx=10, pady=6, sticky="w")

#     def log(msg: str):
#         txt_log.configure(state="normal")
#         txt_log.insert(tk.END, msg + "\n")
#         txt_log.see(tk.END)
#         txt_log.configure(state="disabled")
#         root.update_idletasks()

#     def on_submit():
#         csv_path = ent_csv.get().strip()
#         user = ent_user.get().strip()
#         pwd  = ent_pwd.get().strip()
#         if not csv_path or not user or not pwd:
#             messagebox.showerror("缺少信息", "请填写 CSV 路径、用户名和密码")
#             return
#         log("[INFO] 开始处理…")
#         run(csv_path, user, pwd, log)

#     tk.Button(root, text="开始提交", command=on_submit).grid(row=4, column=1, pady=10)
#     tk.Button(root, text="退出", command=root.destroy).grid(row=4, column=2, pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     main()




# import csv
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# from jira import JIRA

# # 固定为你环境命中的 Base URL（不带 /jira）
# JIRA_BASE_URL = "https://jira.sw.nxp.com"

# # CSV 必须包含的列（已移除 Reporter）
# REQUIRED_COLUMNS = ["Summary", "Description", "Issue Type", "Assignee", "project"]

# def validate_csv_header(header):
#     missing = [c for c in REQUIRED_COLUMNS if c not in (header or [])]
#     return missing

# def connect_jira(username: str, password: str, log):
#     try:
#         log(f"[INFO] 尝试连接：{JIRA_BASE_URL} 用户名：{username}")
#         jira = JIRA(server=JIRA_BASE_URL, basic_auth=(username, password))
#         info = jira.server_info()
#         log(f"[OK] 连接成功：version={info.get('version')}, deploymentType={info.get('deploymentType')}")
#         return jira
#     except Exception as e:
#         messagebox.showerror("登录失败", f"无法连接 Jira：{e}")
#         return None

# def create_and_assign(jira: JIRA, row: dict, row_idx: int, log):
#     summary     = (row.get("Summary") or "").strip()
#     description = (row.get("Description") or "").strip()
#     issuetype   = (row.get("Issue Type") or "").strip()
#     assignee    = (row.get("Assignee") or "").strip()
#     project_key = (row.get("project") or "").strip()

#     if not summary or not issuetype or not project_key:
#         log(f"[WARN] 第 {row_idx} 行缺少必填（Summary/Issue Type/project），跳过")
#         return False

#     # 基础创建字段（Reporter 不设置，由系统自动确定）
#     fields = {
#         "project": {"key": project_key},
#         "summary": summary,
#         "description": description,
#         "issuetype": {"name": issuetype},
#     }

#     # 附带 CSV 里的其它列（自定义字段等，如 customfield_15401 等）
#     for col, val in row.items():
#         if col in REQUIRED_COLUMNS:
#             continue
#         v = (val or "").strip()
#         if v:
#             fields[col] = v

#     # 创建
#     issue = jira.create_issue(fields=fields)
#     log(f"[OK] 创建成功：{issue.key} | {summary}")

#     # 创建后直接指派（Server 环境可用登录名，如 nxa28190）
#     if assignee:
#         try:
#             jira.assign_issue(issue.key, assignee)
#             log(f"[OK] assign_issue 成功：{issue.key} -> {assignee}")
#         except Exception as e:
#             log(f"[WARN] assign_issue 失败（{issue.key} -> {assignee}）：{e}")
#     else:
#         log("[INFO] 未提供 Assignee，保持 Unassigned")

#     return True

# def run(csv_path: str, username: str, password: str, log):
#     jira = connect_jira(username, password, log)
#     if not jira:
#         return

#     try:
#         with open(csv_path, newline="", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             header = reader.fieldnames
#             miss = validate_csv_header(header)
#             if miss:
#                 messagebox.showerror("CSV 列错误", f"缺少必须列：{', '.join(miss)}\n当前列：{', '.join(header or [])}")
#                 return

#             total = success = failed = 0
#             for i, row in enumerate(reader, start=1):
#                 total += 1
#                 try:
#                     ok = create_and_assign(jira, row, i, log)
#                     success += 1 if ok else 0
#                     failed  += 0 if ok else 1
#                 except Exception as e:
#                     log(f"[ERR] 第 {i} 行失败：{e}")
#                     failed += 1

#             messagebox.showinfo("完成", f"处理完成：成功 {success}，失败 {failed}，总计 {total}")
#     except FileNotFoundError:
#         messagebox.showerror("文件错误", f"找不到文件：{csv_path}")
#     except UnicodeDecodeError:
#         messagebox.showerror("编码错误", "请将 CSV 保存为 UTF-8")
#     except Exception as e:
#         messagebox.showerror("未知错误", f"处理 CSV 出错：{e}")

# # ---------------- GUI ----------------

# def main():
#     root = tk.Tk()
#     root.title("Jira Ticket 批量创建（Server / Basic Auth）")
#     root.resizable(False, False)

#     tk.Label(root, text="CSV 文件路径：").grid(row=0, column=0, padx=10, pady=6, sticky="e")
#     ent_csv = tk.Entry(root, width=54)
#     ent_csv.grid(row=0, column=1, padx=10, pady=6)

#     def choose_csv():
#         path = filedialog.askopenfilename(title="选择 CSV 文件",
#                                           filetypes=[("CSV 文件", "*.csv"), ("所有文件", "*.*")])
#         if path:
#             ent_csv.delete(0, tk.END)
#             ent_csv.insert(0, path)
#     tk.Button(root, text="浏览…", command=choose_csv).grid(row=0, column=2, padx=10, pady=6)

#     tk.Label(root, text="Jira 用户名：").grid(row=1, column=0, padx=10, pady=6, sticky="e")
#     ent_user = tk.Entry(root, width=54)
#     ent_user.grid(row=1, column=1, padx=10, pady=6)

#     tk.Label(root, text="Jira 密码：").grid(row=2, column=0, padx=10, pady=6, sticky="e")
#     ent_pwd = tk.Entry(root, width=54, show="*")
#     ent_pwd.grid(row=2, column=1, padx=10, pady=6)

#     tk.Label(root, text="日志：").grid(row=3, column=0, padx=10, pady=6, sticky="ne")
#     txt_log = scrolledtext.ScrolledText(root, width=74, height=18, state="disabled")
#     txt_log.grid(row=3, column=1, columnspan=2, padx=10, pady=6, sticky="w")

#     def log(msg: str):
#         txt_log.configure(state="normal")
#         txt_log.insert(tk.END, msg + "\n")
#         txt_log.see(tk.END)
#         txt_log.configure(state="disabled")
#         root.update_idletasks()

#     def on_submit():
#         csv_path = ent_csv.get().strip()
#         user = ent_user.get().strip()
#         pwd  = ent_pwd.get().strip()
#         if not csv_path or not user or not pwd:
#             messagebox.showerror("缺少信息", "请填写 CSV 路径、用户名和密码")
#             return
#         log("[INFO] 开始处理…")
#         run(csv_path, user, pwd, log)

#     tk.Button(root, text="开始提交", command=on_submit).grid(row=4, column=1, pady=10)
#     tk.Button(root, text="退出", command=root.destroy).grid(row=4, column=2, pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     main()



# import csv
# import datetime
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# from jira import JIRA


# # 你们环境命中的 Base URL（不带 /jira）
# JIRA_BASE_URL = "https://jira.sw.nxp.com"

# # CSV 必填列（已去掉 Reporter）
# REQUIRED_COLUMNS = ["Summary", "Description", "Issue Type", "Assignee", "project"]

# # 可选的“人类可读列名”，自动解析其真实字段 ID（不再手填 customfield_xxxx）
# OPTIONAL_HUMAN_COLUMNS = ["Story Points", "Start Date", "End Date"]

# # 支持的日期输入格式（会统一转换为 YYYY-MM-DD）
# KNOWN_DATE_FORMATS = [
#     "%Y-%m-%d",        # 2025-12-17
#     "%d/%b/%Y",        # 17/Dec/2025（Jira 日期控件常见）
#     "%d/%m/%Y",        # 17/12/2025
#     "%m/%d/%Y",        # 12/17/2025
#     "%Y/%m/%d",        # 2025/12/17
#     "%Y.%m.%d",        # 2025.12.17
# ]


# # ---------------- 工具函数 ----------------

# def normalize_date(value: str):
#     """将常见日期格式转为 Jira Date 格式 YYYY-MM-DD。"""
#     v = (value or "").strip()
#     if not v:
#         return None
#     for fmt in KNOWN_DATE_FORMATS:
#         try:
#             dt = datetime.datetime.strptime(v, fmt)
#             return dt.strftime("%Y-%m-%d")
#         except ValueError:
#             continue
#     # 无法解析则原样返回，让服务器决定是否接受，同时日志会提示
#     return v

# def to_number(value: str):
#     """Story Points 转为数字（支持浮点）。"""
#     v = (value or "").strip()
#     if not v:
#         return None
#     try:
#         return float(v)
#     except ValueError:
#         return None

# def connect_jira(username: str, password: str, log):
#     """Basic Auth 连接 Jira 并打印版本信息。"""
#     try:
#         log(f"[INFO] 尝试连接：{JIRA_BASE_URL} 用户名：{username}")
#         jira = JIRA(server=JIRA_BASE_URL, basic_auth=(username, password))
#         info = jira.server_info()
#         log(f"[OK] 连接成功：version={info.get('version')}, deploymentType={info.get('deploymentType')}")
#         return jira
#     except Exception as e:
#         messagebox.showerror("登录失败", f"无法连接 Jira：\n{e}")
#         return None

# def validate_csv_header(header):
#     """校验 CSV 是否包含必填列。"""
#     missing = [c for c in REQUIRED_COLUMNS if c not in (header or [])]
#     return missing

# def normalize_name(s: str):
#     """字段名标准化（去空格、小写），用于匹配 fields() 返回的名称。"""
#     return (s or "").strip().lower()

# def build_field_id_map(jira, log):
#     """
#     从 Jira 读取所有字段，构造 名称 -> 字段ID 的映射。
#     例如： 'story points' -> 'customfield_10026'
#     """
#     name_to_id = {}
#     try:
#         fields = jira.fields()  # 返回 [{id:..., name:...}, ...]
#         for f in fields:
#             nm = normalize_name(f.get("name"))
#             fid = f.get("id")
#             if nm and fid:
#                 name_to_id[nm] = fid
#         log(f"[INFO] 已加载 {len(name_to_id)} 个字段映射（name -> id）")
#     except Exception as e:
#         log(f"[WARN] 加载字段映射失败：{e}")
#     return name_to_id

# def resolve_optional_field_ids(jira, csv_header, log):
#     """
#     根据 CSV 中的“人类可读列名”（Story Points/Start Date/End Date），
#     自动查找对应的 Jira 字段 ID（customfield_xxx）。
#     返回：dict: {列名: 字段ID}
#     """
#     name_to_id = build_field_id_map(jira, log)
#     resolved = {}
#     for human_col in OPTIONAL_HUMAN_COLUMNS:
#         if human_col in (csv_header or []):
#             key = normalize_name(human_col)
#             fid = name_to_id.get(key)
#             if fid:
#                 resolved[human_col] = fid
#                 log(f"[INFO] 字段解析：{human_col} -> {fid}")
#             else:
#                 log(f"[WARN] 未在 Jira 字段中找到 '{human_col}' 的 ID，若该字段是自定义字段，请确认显示名与项目一致。")
#     return resolved

# def get_createmeta_field_ids(jira, project_key: str, issuetype_name: str, log):
#     """
#     查询 Create Screen 上允许在“创建时”提交的字段 ID 集合。
#     """
#     allowed = set()
#     try:
#         meta = jira.createmeta(
#             projectKeys=project_key,
#             issuetypeNames=issuetype_name,
#             expand="projects.issuetypes.fields"
#         )
#         # 解析返回结构
#         for proj in meta.get("projects", []):
#             for it in proj.get("issuetypes", []):
#                 for fid, fdef in (it.get("fields", {}) or {}).items():
#                     allowed.add(fid)
#         log(f"[INFO] CreateMeta 可创建字段数：{len(allowed)}（项目={project_key}, 类型={issuetype_name}）")
#     except Exception as e:
#         log(f"[WARN] createmeta 查询失败（项目={project_key}, 类型={issuetype_name}）：{e}")
#     return allowed

# def apply_optional_fields(fields_to_create: dict, fields_to_update: dict,
#                           row: dict, create_allowed_ids: set, resolved_ids: dict, log):
#     """
#     把 CSV 中的 Story Points / Start Date / End Date 注入到创建或后续更新的字段字典。
#     规则：
#       - 如果该字段 ID 存在且在 createmeta 允许创建，则放入 fields_to_create。
#       - 否则放入 fields_to_update（创建成功后再 update）。
#     """
#     # Story Points
#     sp_col = "Story Points"
#     if sp_col in row and row[sp_col].strip():
#         sp_val = to_number(row[sp_col])
#         fid = resolved_ids.get(sp_col)  # 自动解析到的 customfield_xxx
#         if not fid:
#             log(f"[WARN] 未解析到 Story Points 的字段ID，已跳过。")
#         elif sp_val is None:
#             log(f"[WARN] Story Points 值不是数字：{row[sp_col]}（已忽略）")
#         else:
#             if fid in create_allowed_ids:
#                 fields_to_create[fid] = sp_val
#             else:
#                 fields_to_update[fid] = sp_val

#     # Start Date
#     sd_col = "Start Date"
#     if sd_col in row and row[sd_col].strip():
#         sd_val = normalize_date(row[sd_col])
#         fid = resolved_ids.get(sd_col)
#         if not fid:
#             log(f"[WARN] 未解析到 Start Date 的字段ID，已跳过。")
#         elif not sd_val:
#             log(f"[WARN] Start Date 无效：{row[sd_col]}（已忽略）")
#         else:
#             if fid in create_allowed_ids:
#                 fields_to_create[fid] = sd_val
#             else:
#                 fields_to_update[fid] = sd_val

#     # End Date
#     ed_col = "End Date"
#     if ed_col in row and row[ed_col].strip():
#         ed_val = normalize_date(row[ed_col])
#         fid = resolved_ids.get(ed_col)
#         if not fid:
#             log(f"[WARN] 未解析到 End Date 的字段ID，已跳过。")
#         elif not ed_val:
#             log(f"[WARN] End Date 无效：{row[ed_col]}（已忽略）")
#         else:
#             if fid in create_allowed_ids:
#                 fields_to_create[fid] = ed_val
#             else:
#                 fields_to_update[fid] = ed_val


# # ---------------- 创建与指派流程 ----------------

# def create_and_assign(jira: JIRA, row: dict, row_idx: int, csv_header, resolved_ids, log):
#     summary     = (row.get("Summary") or "").strip()
#     description = (row.get("Description") or "").strip()
#     issuetype   = (row.get("Issue Type") or "").strip()
#     assignee    = (row.get("Assignee") or "").strip()
#     project_key = (row.get("project") or "").strip()

#     if not summary or not issuetype or not project_key:
#         log(f"[WARN] 第 {row_idx} 行缺少必填（Summary/Issue Type/project），跳过")
#         return False

#     # 查询 Create Screen 允许的字段 ID
#     create_allowed = get_createmeta_field_ids(jira, project_key, issuetype, log)

#     # 基础创建字段（Reporter 不设置，由系统自动）
#     fields_create = {
#         "project": {"key": project_key},
#         "summary": summary,
#         "description": description,
#         "issuetype": {"name": issuetype},
#     }
#     fields_update = {}

#     # 注入 Story Points / Start / End（区分创建与更新）
#     apply_optional_fields(fields_create, fields_update, row, create_allowed, resolved_ids, log)

#     # 其它自定义字段（如 Found In、Original Reporter role 等），如果字段 ID 在 Create Screen 允许，则创建时带上，否则创建后更新
#     for col, val in row.items():
#         if col in REQUIRED_COLUMNS or col in OPTIONAL_HUMAN_COLUMNS:
#             continue
#         v = (val or "").strip()
#         if not v:
#             continue
#         fid = col  # 这里假设你 CSV 填的是字段ID（如 customfield_15401）
#         if fid in create_allowed:
#             fields_create[fid] = v
#         else:
#             fields_update[fid] = v

#     # 创建
#     issue = jira.create_issue(fields=fields_create)
#     log(f"[OK] 创建成功：{issue.key} | {summary}")

#     # 若有需要后续更新的字段，执行 update（Edit Screen 通常允许）
#     if fields_update:
#         try:
#             issue.update(fields=fields_update)
#             log(f"[OK] 创建后更新成功：{issue.key} | 更新字段数={len(fields_update)}")
#         except Exception as e:
#             log(f"[WARN] 创建后更新失败（{issue.key}）：{e}")

#     # 创建后直接指派（Server 环境可用登录名，如 nxa28190）
#     if assignee:
#         try:
#             jira.assign_issue(issue.key, assignee)
#             log(f"[OK] assign_issue 成功：{issue.key} -> {assignee}")
#         except Exception as e:
#             log(f"[WARN] assign_issue 失败（{issue.key} -> {assignee}）：{e}")
#             # 兜底：某些版本用 update 的老式 name 也能成功
#             try:
#                 issue.update(assignee={"name": assignee})
#                 log(f"[OK] issue.update(name) 成功：{issue.key} -> {assignee}")
#             except Exception as e2:
#                 log(f"[ERR] issue.update(name) 也失败：{e2}")
#     else:
#         log("[INFO] 未提供 Assignee，保持 Unassigned")

#     return True


# def run(csv_path: str, username: str, password: str, log):
#     jira = connect_jira(username, password, log)
#     if not jira:
#         return

#     try:
#         with open(csv_path, newline="", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             header = reader.fieldnames
#             miss = validate_csv_header(header)
#             if miss:
#                 messagebox.showerror("CSV 列错误", f"缺少必须列：{', '.join(miss)}\n当前列：{', '.join(header or [])}")
#                 return

#             # 解析人类列名 -> 字段ID（Story Points / Start Date / End Date）
#             resolved_ids = resolve_optional_field_ids(jira, header, log)

#             total = success = failed = 0
#             for i, row in enumerate(reader, start=1):
#                 total += 1
#                 try:
#                     ok = create_and_assign(jira, row, i, header, resolved_ids, log)
#                     success += 1 if ok else 0
#                     failed  += 0 if ok else 1
#                 except Exception as e:
#                     log(f"[ERR] 第 {i} 行失败：{e}")
#                     failed += 1

#             messagebox.showinfo("完成", f"处理完成：成功 {success}，失败 {failed}，总计 {total}")
#     except FileNotFoundError:
#         messagebox.showerror("文件错误", f"找不到文件：{csv_path}")
#     except UnicodeDecodeError:
#         messagebox.showerror("编码错误", "请将 CSV 保存为 UTF-8")
#     except Exception as e:
#         messagebox.showerror("未知错误", f"处理 CSV 出错：{e}")


# # ---------------- GUI ----------------

# def main():
#     root = tk.Tk()
#     root.title("Jira Ticket 批量创建（自动解析字段ID & 分离创建/更新）")
#     root.resizable(False, False)

#     tk.Label(root, text="CSV 文件路径：").grid(row=0, column=0, padx=10, pady=6, sticky="e")
#     ent_csv = tk.Entry(root, width=54)
#     ent_csv.grid(row=0, column=1, padx=10, pady=6)

#     def choose_csv():
#         path = filedialog.askopenfilename(
#             title="选择 CSV 文件",
#             filetypes=[("CSV 文件", "*.csv"), ("所有文件", "*.*")]
#         )
#         if path:
#             ent_csv.delete(0, tk.END)
#             ent_csv.insert(0, path)
#     tk.Button(root, text="浏览…", command=choose_csv).grid(row=0, column=2, padx=10, pady=6)

#     tk.Label(root, text="Jira 用户名：").grid(row=1, column=0, padx=10, pady=6, sticky="e")
#     ent_user = tk.Entry(root, width=54)
#     ent_user.grid(row=1, column=1, padx=10, pady=6)

#     tk.Label(root, text="Jira 密码：").grid(row=2, column=0, padx=10, pady=6, sticky="e")
#     ent_pwd = tk.Entry(root, width=54, show="*")
#     ent_pwd.grid(row=2, column=1, padx=10, pady=6)

#     tk.Label(root, text="日志：").grid(row=3, column=0, padx=10, pady=6, sticky="ne")
#     txt_log = scrolledtext.ScrolledText(root, width=74, height=18, state="disabled")
#     txt_log.grid(row=3, column=1, columnspan=2, padx=10, pady=6, sticky="w")

#     def log(msg: str):
#         txt_log.configure(state="normal")
#         txt_log.insert(tk.END, msg + "\n")
#         txt_log.see(tk.END)
#         txt_log.configure(state="disabled")
#         root.update_idletasks()

#     def on_submit():
#         csv_path = ent_csv.get().strip()
#         user = ent_user.get().strip()
#         pwd  = ent_pwd.get().strip()
#         if not csv_path or not user or not pwd:
#             messagebox.showerror("缺少信息", "请填写 CSV 路径、用户名和密码")
#             return
#         log("[INFO] 开始处理…")
#         run(csv_path, user, pwd, log)

#     tk.Button(root, text="开始提交", command=on_submit).grid(row=4, column=1, pady=10)
#     tk.Button(root, text="退出", command=root.destroy).grid(row=4, column=2, pady=10)

#     root.mainloop()


# if __name__ == "__main__":
#     main()

######################################################################################################################





import csv
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from jira import JIRA


# 你们环境命中的 Base URL（不带 /jira）
JIRA_BASE_URL = "https://jira.sw.nxp.com"

# CSV 必填列（已去掉 Reporter）
REQUIRED_COLUMNS = ["Summary", "Description", "Issue Type", "Assignee", "project"]

# 可选的“人类可读列名”，自动解析其真实字段 ID（不再手填 customfield_xxxx）
OPTIONAL_HUMAN_COLUMNS = ["Story Points", "Start Date", "End Date"]

# Fix Versions 列名（两种写法都支持）
FIX_VERSIONS_COLUMNS = ["Fix Versions", "Fix Version/s"]

# 支持的日期输入格式（会统一转换为 YYYY-MM-DD）
KNOWN_DATE_FORMATS = [
    "%Y-%m-%d",        # 2025-12-17
    "%d/%b/%Y",        # 17/Dec/2025（Jira 日期控件常见）
    "%d/%m/%Y",        # 17/12/2025
    "%m/%d/%Y",        # 12/17/2025
    "%Y/%m/%d",        # 2025/12/17
    "%Y.%m.%d",        # 2025.12.17
]


# ---------------- 工具函数 ----------------

def normalize_date(value: str):
    """将常见日期格式转为 Jira Date 格式 YYYY-MM-DD。"""
    v = (value or "").strip()
    if not v:
        return None
    for fmt in KNOWN_DATE_FORMATS:
        try:
            dt = datetime.datetime.strptime(v, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # 无法解析则原样返回，让服务器决定是否接受，同时日志会提示
    return v

def to_number(value: str):
    """Story Points 转为数字（支持浮点）。"""
    v = (value or "").strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None

def connect_jira(username: str, password: str, log):
    """Basic Auth 连接 Jira 并打印版本信息。"""
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
    """校验 CSV 是否包含必填列。"""
    missing = [c for c in REQUIRED_COLUMNS if c not in (header or [])]
    return missing

def normalize_name(s: str):
    """字段名标准化（去空格、小写），用于匹配 fields() 返回的名称。"""
    return (s or "").strip().lower()

def build_field_id_map(jira, log):
    """
    从 Jira 读取所有字段，构造 名称 -> 字段ID 的映射。
    例如： 'story points' -> 'customfield_10026'
    """
    name_to_id = {}
    try:
        fields = jira.fields()  # 返回 [{id:..., name:...}, ...]
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
    """
    根据 CSV 中的“人类可读列名”（Story Points/Start Date/End Date），
    自动查找对应的 Jira 字段 ID（customfield_xxx）。
    返回：dict: {列名: 字段ID}
    """
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
                log(f"[WARN] 未在 Jira 字段中找到 '{human_col}' 的 ID，若该字段是自定义字段，请确认显示名与项目一致。")
    return resolved

def get_createmeta_field_ids(jira, project_key: str, issuetype_name: str, log):
    """
    查询 Create Screen 上允许在“创建时”提交的字段 ID 集合。
    """
    allowed = set()
    try:
        meta = jira.createmeta(
            projectKeys=project_key,
            issuetypeNames=issuetype_name,
            expand="projects.issuetypes.fields"
        )
        # 解析返回结构
        for proj in meta.get("projects", []):
            for it in proj.get("issuetypes", []):
                for fid, fdef in (it.get("fields", {}) or {}).items():
                    allowed.add(fid)
        log(f"[INFO] CreateMeta 可创建字段数：{len(allowed)}（项目={project_key}, 类型={issuetype_name}）")
    except Exception as e:
        log(f"[WARN] createmeta 查询失败（项目={project_key}, 类型={issuetype_name}）：{e}")
    return allowed

def parse_fix_versions(text: str):
    """
    从 CSV 值解析 Fix Versions 名称列表。
    支持分隔符：逗号/分号/竖线。
    """
    if not text:
        return []
    raw = [p.strip() for p in re_split_multi(text)]
    return [p for p in raw if p]

def re_split_multi(text: str):
    """按多种分隔符拆分：逗号、分号、竖线。"""
    import re
    return re.split(r"[;,|]", text)


# ---------------- 可选字段注入 ----------------

def apply_optional_fields(fields_to_create: dict, fields_to_update: dict,
                          row: dict, create_allowed_ids: set, resolved_ids: dict, log):
    """
    把 CSV 中的 Story Points / Start Date / End Date 注入到创建或后续更新的字段字典。
    规则：
      - 如果该字段 ID 存在且在 createmeta 允许创建，则放入 fields_to_create。
      - 否则放入 fields_to_update（创建成功后再 update）。
    """
    # Story Points
    sp_col = "Story Points"
    if sp_col in row and row[sp_col].strip():
        sp_val = to_number(row[sp_col])
        fid = resolved_ids.get(sp_col)  # 自动解析到的 customfield_xxx
        if not fid:
            log(f"[WARN] 未解析到 Story Points 的字段ID，已跳过。")
        elif sp_val is None:
            log(f"[WARN] Story Points 值不是数字：{row[sp_col]}（已忽略）")
        else:
            if fid in create_allowed_ids:
                fields_to_create[fid] = sp_val
            else:
                fields_to_update[fid] = sp_val

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
            if fid in create_allowed_ids:
                fields_to_create[fid] = sd_val
            else:
                fields_to_update[fid] = sd_val

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
            if fid in create_allowed_ids:
                fields_to_create[fid] = ed_val
            else:
                fields_to_update[fid] = ed_val


def apply_fix_versions(fields_to_create: dict, fields_to_update: dict,
                       row: dict, create_allowed_ids: set, jira, project_key: str, log):
    """
    处理 Fix Versions：只接受项目中已存在的版本名。
    将其转换为 [{'name': 'v1'}, {'name': 'v2'}] 的形式，按 createmeta 切分创建/更新。
    """
    # 找到 CSV 中的 Fix Versions 列名
    fix_col = None
    for c in FIX_VERSIONS_COLUMNS:
        if c in row:
            fix_col = c
            break
    if not fix_col:
        return  # 未提供该列

    raw = (row.get(fix_col) or "").strip()
    if not raw:
        return

    # 解析版本名列表
    names = parse_fix_versions(raw)
    if not names:
        return

    # 查询项目已有版本列表，过滤不存在的版本
    try:
        versions = jira.project_versions(project_key)
        existing_names = {getattr(v, "name", "").strip() for v in versions}
    except Exception as e:
        log(f"[WARN] 获取项目版本失败（{project_key}）：{e}")
        existing_names = set()

    valid_names = [n for n in names if n in existing_names] if existing_names else names
    invalid_names = [n for n in names if n not in existing_names] if existing_names else []

    if invalid_names:
        log(f"[WARN] 下列 Fix Versions 在项目 '{project_key}' 中不存在，已忽略：{', '.join(invalid_names)}")

    if not valid_names:
        return

    payload = [{"name": n} for n in valid_names]

    # fixVersions 是系统字段，字段ID即 'fixVersions'
    if "fixVersions" in create_allowed_ids:
        fields_to_create["fixVersions"] = payload
    else:
        fields_to_update["fixVersions"] = payload


# ---------------- 创建与指派流程 ----------------

def create_and_assign(jira: JIRA, row: dict, row_idx: int, csv_header, resolved_ids, log):
    summary     = (row.get("Summary") or "").strip()
    description = (row.get("Description") or "").strip()
    issuetype   = (row.get("Issue Type") or "").strip()
    assignee    = (row.get("Assignee") or "").strip()
    project_key = (row.get("project") or "").strip()

    if not summary or not issuetype or not project_key:
        log(f"[WARN] 第 {row_idx} 行缺少必填（Summary/Issue Type/project），跳过")
        return False

    # 查询 Create Screen 允许的字段 ID
    create_allowed = get_createmeta_field_ids(jira, project_key, issuetype, log)

    # 基础创建字段（Reporter 不设置，由系统自动）
    fields_create = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issuetype},
    }
    fields_update = {}

    # 注入 Story Points / Start / End（区分创建与更新）
    apply_optional_fields(fields_create, fields_update, row, create_allowed, resolved_ids, log)

    # 注入 Fix Versions（系统字段 fixVersions）
    apply_fix_versions(fields_create, fields_update, row, create_allowed, jira, project_key, log)

    # 其它自定义字段（如 Found In、Original Reporter role 等），如果字段 ID 在 Create Screen 允许，则创建时带上，否则创建后更新
    for col, val in row.items():
        # 已处理过的列跳过
        if col in REQUIRED_COLUMNS or col in OPTIONAL_HUMAN_COLUMNS or col in FIX_VERSIONS_COLUMNS:
            continue
        v = (val or "").strip()
        if not v:
            continue
        fid = col  # 这里假设你 CSV 填的是字段ID（如 customfield_15401）
        if fid in create_allowed:
            fields_create[fid] = v
        else:
            fields_update[fid] = v

    # 创建
    issue = jira.create_issue(fields=fields_create)
    log(f"[OK] 创建成功：{issue.key} | {summary}")

    # 若有需要后续更新的字段，执行 update（Edit Screen 通常允许）
    if fields_update:
        try:
            issue.update(fields=fields_update)
            log(f"[OK] 创建后更新成功：{issue.key} | 更新字段数={len(fields_update)}")
        except Exception as e:
            log(f"[WARN] 创建后更新失败（{issue.key}）：{e}")

    # 创建后直接指派（Server 环境可用登录名，如 nxa28190）
    if assignee:
        try:
            jira.assign_issue(issue.key, assignee)
            log(f"[OK] assign_issue 成功：{issue.key} -> {assignee}")
        except Exception as e:
            log(f"[WARN] assign_issue 失败（{issue.key} -> {assignee}）：{e}")
            # 兜底：某些版本用 update 的老式 name 也能成功
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
        with open(csv_path, newline="", encoding="utf-8") as f:
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
                    ok = create_and_assign(jira, row, i, header, resolved_ids, log)
                    success += 1 if ok else 0
                    failed  += 0 if ok else 1
                except Exception as e:
                    log(f"[ERR] 第 {i} 行失败：{e}")
                    failed += 1

            messagebox.showinfo("完成", f"处理完成：成功 {success}，失败 {failed}，总计 {total}")
    except FileNotFoundError:
        messagebox.showerror("文件错误", f"找不到文件：{csv_path}")
    except UnicodeDecodeError:
        messagebox.showerror("编码错误", "请将 CSV 保存为 UTF-8")
    except Exception as e:
        messagebox.showerror("未知错误", f"处理 CSV 出错：{e}")


# ---------------- GUI ----------------

def main():
    root = tk.Tk()
    root.title("Jira Ticket 批量创建（含 Fix Versions / Story Points / Start / End）")
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
        pwd  = ent_pwd.get().strip()
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



