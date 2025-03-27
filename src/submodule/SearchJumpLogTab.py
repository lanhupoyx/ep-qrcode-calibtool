import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime


#查看跳变
class SearchJumpLogTab:
    def __init__(self, app):
        self.tab = app.tab2 
        # 定义要备份的文件和备份文件夹
        self.SiteTableName = app.SiteTableName
        self.paramFolder = app.paramFolder
        self.SiteTablepath = self.paramFolder + self.SiteTableName
        self.notebook = app.notebook
        self.notebook.add(self.tab, text=' 2.查看跳变 ')

        # 创建输入框和按钮
        self.label_a2 = ttk.Label(self.tab, text="编号:")
        self.label_a2.grid(row=0, column=0, padx=10, pady=10)
        self.entry_a2 = ttk.Entry(self.tab, width=50)
        self.entry_a2.grid(row=0, column=1, padx=10, pady=10)
        self.button_a2 = ttk.Button(self.tab, text="查找/更新", command=self.search_log)
        self.button_a2.grid(row=0, column=2, padx=10, pady=10)
        
        self.result_text2 = tk.Text(self.tab, height=23, width=150)
        self.result_text2.grid(row=1, column=0, columnspan=3, padx=10, pady=10)


    def search_log(self):
        search_log_index = self.entry_a2.get()

        self.result_text2.delete(1.0, tk.END)  # 请空结果框
        
        # 获取当前日期
        current_date = datetime.now()
        # 格式化日期为 "年_月_日" 的格式，去掉月和日的前导零
        date_string = f"{current_date.year}-{current_date.month}-{current_date.day}"    
        logpath = "/var/xmover/log/QR_code_loc/" + date_string + "/jumperr.txt"
        log_lines = []
        try:
            with open(logpath, "r", encoding="utf-8") as file:
                log_lines = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("错误", "文档" + logpath +"未找到！")
            return

        if not search_log_index: 
            self.result_text2.insert(tk.END, "".join(log_lines))
            self.result_text2.insert(tk.END, "\n\n")
        else:
            if not search_log_index.isdigit():
                messagebox.showwarning("警告", "请输入数字！")
                return
        
            if not ((99999<int(search_log_index)) and (int(search_log_index) < 200000)):
                messagebox.showwarning("警告", "编号在100000到199999之间！")
                return
            found = False
            for i, line in enumerate(log_lines):
                if search_log_index in line:
                    found = True
                    start_line = max(0, i - 15)
                    end_line = min(len(log_lines), i + 6)
                    context_lines = log_lines[start_line:end_line]
                    self.result_text2.insert(tk.END, f"找到编号所在的行（行号：{i + 1}）及其上下文：\n")
                    self.result_text2.insert(tk.END, "".join(context_lines))
                    self.result_text2.insert(tk.END, "\n\n")

            if not found:
                messagebox.showinfo("未找到", f"文档中未找到编号 '{search_log_index}'")
        
        self.result_text2.see(tk.END) # 自动滑动到最底部
