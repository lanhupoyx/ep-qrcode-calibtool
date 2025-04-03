import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("二选一按钮示例")

# 创建一个变量用于存储选中的选项
selected_option = tk.StringVar()

# 定义选项
option1 = tk.Radiobutton(root, text="选项A", variable=selected_option, value="A")
option2 = tk.Radiobutton(root, text="选项B", variable=selected_option, value="B")

# 将选项放置到窗口中
option1.pack()
option2.pack()

# 创建一个按钮，点击后显示选中的选项
def show_selection():
    selection = selected_option.get()
    if selection == "A":
        print("你选择了选项A")
    elif selection == "B":
        print("你选择了选项B")
    else:
        print("没有选择任何选项")

show_button = tk.Button(root, text="显示选择", command=show_selection)
show_button.pack()

# 运行主循环
root.mainloop()