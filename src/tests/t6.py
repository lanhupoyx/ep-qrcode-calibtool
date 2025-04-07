
import tkinter as tk
from tkinter import ttk

def on_submit():
    try:
        user_input = int(entry_var.get())  # 将输入转换为整数
        print(f"User input: {user_input}")
    except ValueError:
        print("Invalid input. Please enter an integer.")

# 创建主窗口
root = tk.Tk()
root.title("Entry with Integer Default Value")
root.geometry("300x200")

# 创建 StringVar 变量
entry_var = tk.StringVar()
entry_var.set("10")  # 设置默认值为整数 10

# 创建 Entry 控件
entry = ttk.Entry(root, textvariable=entry_var)
entry.pack(pady=20)

# 创建提交按钮
submit_button = ttk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# 运行主循环
root.mainloop()