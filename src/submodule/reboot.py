from tkinter import messagebox
import subprocess


class reboot:
    def reboot_qrcodeLoc(self):
        #执行命令
        command = ["systemctl","restart","ep-qrcode-loc"]
        result = subprocess.run(command, text=True, capture_output=True)

        print("Output:", result.stdout)
        print("Error:", result.stderr)
        
        #输出提示框
        if '' == result.stderr:
            messagebox.showinfo("成功", "成功！二维码定位程序已重启。")
        else:
            messagebox.showerror("失败", "失败！二维码定位程序未重启，请联系开发人员。")