import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("Grid 3行平分成2行示例")
root.geometry("400x300")  # 设置窗口大小

# 创建 3 个控件
label1 = tk.Label(root, text="控件1", bg="red", fg="white")
label2 = tk.Label(root, text="控件2", bg="green", fg="white")
label3 = tk.Label(root, text="控件3", bg="blue", fg="white")

# 使用 grid 布局
# 将窗口分为 2 行 1 列
label1.grid(row=0, column=0, rowspan=2, sticky="nsew")  # 控件1跨越2行
label2.grid(row=2, column=0, sticky="nsew")             # 控件2占据第3行
label3.grid(row=3, column=0, sticky="nsew")             # 控件3占据第4行

# 配置行和列的权重，以便它们可以动态调整大小
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# 运行主循环
root.mainloop()