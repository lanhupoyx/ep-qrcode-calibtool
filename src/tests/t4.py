import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("数据展示示例")
root.geometry("400x300")

# 展示列表数据
data_listbox = tk.Listbox(root, font=("Arial", 12), width=30)
data_listbox.pack(pady=20)

# 添加数据到 Listbox
data_list = ["数据1", "数据2", "数据3", "数据4"]
for item in data_list:
    data_listbox.insert(tk.END, item)

# 运行主循环
root.mainloop()