import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from reboot import reboot

from topFrame import topFrame

#------------------------------修改编号---------------------------------------

class ChangeIndexTab(reboot): 
    def __init__(self, app):
        self.tab = app.tab1
        # 定义要备份的文件和备份文件夹
        self.SiteTableName = app.SiteTableName
        self.paramFolder = app.paramFolder
        self.SiteTablepath = self.paramFolder + self.SiteTableName
        self.notebook = app.notebook
        
        # 添加标签页到 Notebook
        self.notebook.add(self.tab, text=' 1.相机标定 ')
        
        self.label_lidar = ttk.Label(self.tab, text="Lidar loc:")
        self.label_lidar.grid(row=0, column=0, padx=10, pady=10)
        self.canvas_lidar = tk.Canvas(self.tab, width=60, height=30, bg="#d9d9d9")
        self.canvas_lidar.grid(row=0, column=1, padx=10, pady=10)
        self.light_lidar = self.canvas_lidar.create_rectangle(0, 0, 60, 30, fill="green")  # 默认灰色
        
        self.label_qrcode = ttk.Label(self.tab, text="QR-code:")
        self.label_qrcode.grid(row=1, column=0, padx=10, pady=10)
        self.canvas_qrcode = tk.Canvas(self.tab, width=60, height=30, bg="#d9d9d9")
        self.canvas_qrcode.grid(row=1, column=1, padx=10, pady=10)
        self.light_qrcode = self.canvas_qrcode.create_rectangle(0, 0, 60, 30, fill="red")  # 默认灰色
        
        self.label_x = ttk.Label(self.tab, text="x:")
        self.label_x.grid(row=0, column=2, padx=10, pady=10)
        self.entry_x = ttk.Entry(self.tab, width=10)
        self.entry_x.grid(row=0, column=3, padx=10, pady=10)

        self.label_y = ttk.Label(self.tab, text="y:")
        self.label_y.grid(row=1, column=2, padx=10, pady=10)
        self.entry_y = ttk.Entry(self.tab, width=10)
        self.entry_y.grid(row=1, column=3, padx=10, pady=10)
        
        self.label_yaw = ttk.Label(self.tab, text="yaw:")
        self.label_yaw.grid(row=2, column=2, padx=10, pady=10)
        self.entry_yaw = ttk.Entry(self.tab, width=10)
        self.entry_yaw.grid(row=2, column=3, padx=10, pady=10)
        
        
        # # 创建输入框和按钮
        # self.label_a = ttk.Label(self.tab, text="编号A:")
        # self.label_a.grid(row=0, column=0, padx=10, pady=10)
        # self.entry_a = ttk.Entry(self.tab, width=50)
        # self.entry_a.grid(row=0, column=1, padx=10, pady=10)

        # self.label_b = ttk.Label(self.tab, text="编号B:")
        # self.label_b.grid(row=1, column=0, padx=10, pady=10)
        # self.entry_b = ttk.Entry(self.tab, width=50)
        # self.entry_b.grid(row=1, column=1, padx=10, pady=10)
        
        # self.button_a = ttk.Button(self.tab, text="查找: 编号A", command=self.search_string_a)
        # self.button_a.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        # self.button_b = ttk.Button(self.tab, text="替换: A->B", command=self.replace_string_a_with_b)
        # self.button_b.grid(row=0, column=3, rowspan=2, padx=10, pady=10)
        # self.button_c = ttk.Button(self.tab, text="重启二维码定位", command=self.reboot_qrcodeLoc)
        # self.button_c.grid(row=0, column=4, rowspan=2, padx=10, pady=10)

        # self.result_text = tk.Text(self.tab, height=21, width=150)
        # self.result_text.grid(row=2, column=0, columnspan=5, padx=10, pady=10)
        
        # 初始化文档内容
        self.document_lines = []
        self.document_lines_temp = []
        
        
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
            messagebox.showwarning("警告", "请输入编号A！")
            return

        if not search_string.isdigit():
            messagebox.showwarning("警告", "请输入数字！")
            return
        
        if not ((99999<int(search_string)) and (int(search_string) < 200000)):
            messagebox.showwarning("警告", "编号A在100000到199999之间！")
            return
        
        self.result_text.delete(1.0, tk.END)  # 请空结果框
        found = False
        
        self.load_document() #加载文件
        
        for i, line in enumerate(self.document_lines):
            if search_string in line:
                found = True
                start_line = max(0, i - 5)
                end_line = min(len(self.document_lines), i + 6)
                context_lines = self.document_lines[start_line:end_line]
                self.result_text.insert(tk.END, f"找到编号A所在的行（行号：{i + 1}）及其上下文：\n")
                self.result_text.insert(tk.END, "".join(context_lines))
                self.result_text.insert(tk.END, "\n\n")

        if not found:
            messagebox.showinfo("未找到", f"文档中未找到编号A '{search_string}'")
            
    def replace_string_a_with_b(self):
        # 输入数据与检查
        search_string = self.entry_a.get()
        replace_string = self.entry_b.get()
        if not search_string or not replace_string:
            messagebox.showwarning("警告", "请输入编号A和编号B！")
            return
        if not search_string.isdigit() or not replace_string.isdigit():
            messagebox.showwarning("警告", "编号A和编号B请输入数字！")
            return
        if not ((99999<int(search_string)) and (int(search_string) < 200000)):
            messagebox.showwarning("警告", "编号A在100000到199999之间！")
            return
        if not ((99999<int(replace_string)) and (int(replace_string) < 200000)):
            messagebox.showwarning("警告", "编号B在100000到199999之间！")
            return
        
        #查找编号A
        self.result_text.delete(1.0, tk.END)  # 请空结果框
        found = False
        self.load_document() #加载文件
        for i, line in enumerate(self.document_lines):
            if search_string in line:
                found = True
                start_line = max(0, i - 5)
                end_line = min(len(self.document_lines), i + 6)
                context_lines = self.document_lines[start_line:end_line]
                self.result_text.insert(tk.END, f"找到编号A所在的行（行号：{i + 1}）及其上下文：\n")
                self.result_text.insert(tk.END, "".join(context_lines))
                self.result_text.insert(tk.END, "\n\n")
        if not found:
            messagebox.showinfo("未找到", f"文档中未找到编号A '{search_string}'")
            return
        
        # 编号A替换为编号B
        self.document_lines = [line.replace(search_string, replace_string) for line in self.document_lines]
        
        # 方向角补偿值归零
        self.document_lines_temp = []
        for line in self.document_lines:
            if replace_string in line:
                # 找到最后一个逗号的位置
                last_comma_index = line.rfind(',')
                if last_comma_index != -1:
                    # 删除最后一个逗号后面的内容，并在末尾添加 "0"
                    line = line[:(last_comma_index+1)] + "0\n"
            #print(line)
            self.document_lines_temp.append(line)
        self.document_lines = self.document_lines_temp
        
        # 将修改后的内容写回文件
        with open(self.SiteTablepath, 'w', encoding='utf-8') as file:
            file.writelines(self.document_lines)

        # 显示替换后编号B的上下文
        self.result_text.delete(1.0, tk.END)  # 请空结果框
        found = False
        for i, line in enumerate(self.document_lines):
            if replace_string in line:
                found = True
                start_line = max(0, i - 5)
                end_line = min(len(self.document_lines), i + 6)
                context_lines = self.document_lines[start_line:end_line]
                self.result_text.insert(tk.END, f"替换后的编号B所在的行（行号：{i + 1}）及其上下文：\n")
                self.result_text.insert(tk.END, "".join(context_lines))
                self.result_text.insert(tk.END, "\n\n")
        if not found:
            messagebox.showinfo("未找到", f"修改后的文档中未找到编号B '{replace_string}'，请联系开发开发人员！")

        messagebox.showinfo("成功", f"编号B '{replace_string}'替换完成！文档已更新。")


def main():
    root = tk.Tk()#tinker
    
    app = topFrame(root)#顶层窗体
    
    tab1 = ChangeIndexTab(app)#标签页1
    # tab2 = SearchJumpLogTab(app)#标签页2
    # tab3 = SearchYawTab(app)#标签页3
    # tab4 = ReadmeTab(app)#标签页4
    default_bg_color = root.cget("bg")  # 获取窗口的默认背景颜色
    print("默认窗口背景颜色:", default_bg_color)
       
    # app.backup_file(app.SiteTableName, app.paramFolder)# 执行文档备份操作
    root.mainloop()# 主循环
    

#main函数
if __name__ == "__main__":
   main()