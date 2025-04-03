import tkinter as tk
from tkinter import ttk

# 创建主窗口
root = tk.Tk()
root.title("Tkinter 表格示例")
root.geometry("600x400")

# 定义表格数据
data = [
    {"id": 1, "name": "张三", "age": 25, "city": "北京"},
    {"id": 2, "name": "李四", "age": 30, "city": "上海"},
    {"id": 3, "name": "王五", "age": 28, "city": "广州"},
    {"id": 4, "name": "赵六", "age": 22, "city": "深圳"}
]

# 创建 Treeview 组件
columns = ("id", "name", "age", "city")
treeview = ttk.Treeview(root, columns=columns, show="headings")

# 设置列标题
for col in columns:
    treeview.heading(col, text=col.capitalize())
    treeview.column(col, width=100)

# 插入数据到表格
for row in data:
    treeview.insert("", "end", values=(row["id"], row["name"], row["age"], row["city"]))

# 将 Treeview 放置到窗口中
treeview.pack(fill="both", expand=True)

# 启动主循环
root.mainloop()