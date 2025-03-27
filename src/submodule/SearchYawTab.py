import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from submodule.reboot import reboot



#修改方向角
class SearchYawTab(reboot):
    def __init__(self, app):
        self.tab = app.tab3
        # 定义要备份的文件和备份文件夹
        self.SiteTableName = app.SiteTableName
        self.paramFolder = app.paramFolder
        self.SiteTablepath = self.paramFolder + self.SiteTableName
        self.notebook = app.notebook
        
        # 添加标签页到 Notebook
        self.notebook.add(self.tab, text=' 3.修改角度 ')
        
        # 创建输入框和按钮
        self.label_a = ttk.Label(self.tab, text="编号:")
        self.label_a.grid(row=0, column=0, padx=10, pady=10)
        self.entry_a = ttk.Entry(self.tab, width=50)
        self.entry_a.grid(row=0, column=1, padx=10, pady=10)
        self.button_a = ttk.Button(self.tab, text="查找", command=self.search_string_a)
        self.button_a.grid(row=0, column=2, padx=10, pady=10)
        self.button_ym = ttk.Button(self.tab, text="角度 -0.1", command=self.yaw_minus_string_a)
        self.button_ym.grid(row=0, column=3, padx=10, pady=10)
        self.button_yp = ttk.Button(self.tab, text="角度 +0.1", command=self.yaw_plus_string_a)
        self.button_yp.grid(row=0, column=4, padx=10, pady=10)
        self.button_rb = ttk.Button(self.tab, text="重启二维码定位", command=self.reboot_qrcodeLoc)
        self.button_rb.grid(row=0, column=5, padx=10, pady=10)

        self.result_text = tk.Text(self.tab, height=23, width=150)
        self.result_text.grid(row=1, column=0, columnspan=6, padx=10, pady=10)
        
        # 初始化文档内容
        self.document_lines = []
        self.document_lines_temp = []
        self.isFound = False
        self.index_last = 0
        
        
    def load_document(self):
        try:
            with open(self.SiteTablepath, "r", encoding="utf-8") as file:
                self.document_lines = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("错误", "文档" + self.SiteTablepath +"未找到！")
            self.document_lines = []

    def search_string_a(self):
        search_string = self.entry_a.get()
        if not search_string:
            messagebox.showwarning("警告", "请输入编号！")
            return

        if not search_string.isdigit():
            messagebox.showwarning("警告", "请输入数字！")
            return
        
        if not ((99999<int(search_string)) and (int(search_string) < 200000)):
            messagebox.showwarning("警告", "编号在100000到199999之间！")
            return
        
        self.result_text.delete(1.0, tk.END)  # 请空结果框
        found = False
        
        self.load_document() #加载文件
        
        for i, line in enumerate(self.document_lines):
            if search_string in line:
                found = True
                self.isFound = True
                self.index_last = search_string
                start_line = max(0, i - 5)
                end_line = min(len(self.document_lines), i + 6)
                context_lines = self.document_lines[start_line:end_line]
                self.result_text.insert(tk.END, f"找到编号所在的行（行号：{i + 1}）及其上下文：\n")
                self.result_text.insert(tk.END, "".join(context_lines))
                self.result_text.insert(tk.END, "\n\n")

        if not found:
            messagebox.showinfo("未找到", f"文档中未找到编号 '{search_string}'")
            
    def yaw_minus_string_a(self):
        self.yaw_change("minus")

    def yaw_plus_string_a(self):
        self.yaw_change("plus")

    def yaw_change(self, PorM):
        search_string = self.entry_a.get()
        
        if search_string != self.index_last:
            self.isFound = False
            
        if not self.isFound:
            messagebox.showwarning("警告", "请先进行查找！")
            return

        if not search_string:
            messagebox.showwarning("警告", "请输入编号！")
            return
        
        if not search_string.isdigit():
            messagebox.showwarning("警告", "请输入数字！")
            return
        
        if not ((99999<int(search_string)) and (int(search_string) < 200000)):
            messagebox.showwarning("警告", "编号在100000到199999之间！")
            return
        
        self.result_text.delete(1.0, tk.END)  # 请空结果框
        found = False
       
        self.document_lines_temp = []
        
        self.load_document() #加载文件
        
        # 遍历每一行，查找目标编号
        for line in self.document_lines:
            if search_string in line:
                # 找到最后一个逗号的位置
                last_comma_index = line.rfind(',')
                if last_comma_index != -1:
                    if "plus" == PorM:
                        yaw = round(float(line[(last_comma_index+1):-1]) + 0.1, 6)
                    elif "minus" == PorM:
                        yaw = round(float(line[(last_comma_index+1):-1]) - 0.1, 6)
                    else:
                        messagebox.showerror("错误", "not plus or minus!")
                        return
                    # 删除最后一个逗号后面的内容，并在末尾添加 "0"
                    line = line[:(last_comma_index+1)] + str(yaw) + "\n"
            #print(line)
            self.document_lines_temp.append(line)
        self.document_lines = self.document_lines_temp
        
        # 将修改后的内容写回文件
        with open(self.SiteTablepath, 'w', encoding='utf-8') as file:
            file.writelines(self.document_lines)
        

        # 显示编号的上下文
        self.result_text.delete(1.0, tk.END)  # 请空结果框
        found = False

        for i, line in enumerate(self.document_lines):
            if search_string in line:
                found = True
                start_line = max(0, i - 5)
                end_line = min(len(self.document_lines), i + 6)
                context_lines = self.document_lines[start_line:end_line]
                self.result_text.insert(tk.END, f"编号所在的行（行号：{i + 1}）及其上下文：\n")
                self.result_text.insert(tk.END, "".join(context_lines))
                self.result_text.insert(tk.END, "\n\n")

        if not found:
            messagebox.showinfo("未找到", f"文档中未找到编号 '{search_string}'")

        if "plus" == PorM:
            messagebox.showinfo("成功", "编号"+str(search_string)+"方向角增大0.1")
        elif "minus" == PorM:
            messagebox.showinfo("成功", "编号"+str(search_string)+"方向角减小0.1")
        else:
            messagebox.showerror("错误", "not plus or minus!")
            return
