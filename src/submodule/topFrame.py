from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import os
import shutil



#顶层框架
class topFrame:
    
    def __init__(self, root):
        # 定义要备份的文件和备份文件夹
        self.SiteTableName = "SiteTable.txt" 
        self.paramFolder = "/var/xmover/params/ep-qrcode-loc/" 
        self.SiteTablepath = self.paramFolder + self.SiteTableName
        self.readmePath = "/opt/xmover/app/ep-qrcode-calibtool/readme.txt" 
        
        self.root = root
        self.root.title("中力-定位相机标定工具 v0.1.0")
        
        # 创建 Notebook 控件
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10)

        # 创建标签页
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)


    def backup_file(self,source_file, param_folder):
        # 确保备份文件夹存在
        backup_folder = param_folder + "backup/"
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
            print(f"创建备份文件夹：{backup_folder}")

        # 生成唯一的备份文件名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = os.path.basename(source_file)
        backup_file_name = f"{timestamp}_{file_name}"
        backup_file_path = os.path.join(backup_folder, backup_file_name)

        # 复制文件到备份文件夹
        shutil.copy2(param_folder + source_file, backup_file_path)
        print(f"文件已备份到：{backup_file_path}")
        messagebox.showinfo("成功", "文档" + param_folder + source_file +"已备份！")
