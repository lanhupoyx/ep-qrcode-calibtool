import tkinter as tk

class IndicatorLight:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter 指示灯示例")

        # 创建画布
        self.canvas = tk.Canvas(root, width=200, height=200, bg="white")
        self.canvas.pack(pady=20)

        # 绘制圆形指示灯
        self.light = self.canvas.create_oval(70, 70, 130, 130, fill="gray")  # 默认灰色

        # 添加按钮来改变指示灯颜色
        self.button = tk.Button(root, text="变红", command=self.turn_red)
        self.button.pack(side=tk.LEFT, padx=10)

        self.button = tk.Button(root, text="变绿", command=self.turn_green)
        self.button.pack(side=tk.LEFT, padx=10)

        self.button = tk.Button(root, text="变黄", command=self.turn_yellow)
        self.button.pack(side=tk.LEFT, padx=10)

    def turn_red(self):
        self.canvas.itemconfig(self.light, fill="red")

    def turn_green(self):
        self.canvas.itemconfig(self.light, fill="green")

    def turn_yellow(self):
        self.canvas.itemconfig(self.light, fill="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    app = IndicatorLight(root)
    root.mainloop()