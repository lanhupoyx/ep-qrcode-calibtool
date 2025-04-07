import tkinter as tk
from tkinter import ttk

def on_treeview_select(event):
    # 获取当前选中的行
    selected_items = tree.selection()
    if selected_items:
        for item in selected_items:
            # 获取选中行的值
            item_values = tree.item(item, "values")
            print(f"Selected item: {item_values}")
    else:
        print("No item selected")

# 创建主窗口
root = tk.Tk()
root.title("Treeview Example")
root.geometry("300x200")

# 创建 Treeview 控件
tree = ttk.Treeview(root, columns=("ID", "Name", "Age"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.column("ID", width=50)
tree.column("Name", width=100)
tree.column("Age", width=50)

# 插入一些示例数据
tree.insert("", "end", values=("1", "Alice", "25"))
tree.insert("", "end", values=("2", "Bob", "30"))
tree.insert("", "end", values=("3", "Charlie", "35"))

# 绑定选中事件
tree.bind("<<TreeviewSelect>>", on_treeview_select)

# 将 Treeview 控件放置到窗口中
tree.pack(fill="both", expand=True)

# 运行主循环
root.mainloop()