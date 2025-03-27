import tkinter as tk
from tkinter import messagebox


#查看跳变
class ReadmeTab:
    def __init__(self, app):
        self.tab = app.tab4
        # 定义要备份的文件和备份文件夹
        self.readmePath = app.readmePath
        self.notebook = app.notebook
        self.notebook.add(self.tab, text=' 教程 ')

        self.result_text2 = tk.Text(self.tab, height=26, width=150)
        self.result_text2.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.showReadme()


    def showReadme(self):
        readme_lines = []
        try:
            with open(self.readmePath, "r", encoding="utf-8") as file:
                readme_lines = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("错误", "文档" + self.readmePath +"未找到！")
            return

        self.result_text2.insert(tk.END, "".join(readme_lines))
        self.result_text2.insert(tk.END, "\n\n")
