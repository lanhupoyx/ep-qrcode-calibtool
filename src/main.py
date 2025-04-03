import tkinter as tk

from submodule.topFrame import topFrame
from submodule.ChangeIndexTab import ChangeIndexTab
from submodule.SearchJumpLogTab import SearchJumpLogTab
from submodule.SearchYawTab import SearchYawTab
from submodule.ReadmeTab import ReadmeTab


def main():
    root = tk.Tk()#tinker
    
    app = topFrame(root)#顶层窗体
    
    tab1 = ChangeIndexTab(app)#标签页1
    tab2 = SearchJumpLogTab(app)#标签页2
    tab3 = SearchYawTab(app)#标签页3
    tab4 = ReadmeTab(app)#标签页4
       
    # app.backup_file(app.SiteTableName, app.paramFolder)# 执行文档备份操作
    root.mainloop()# 主循环
    

#main函数
if __name__ == "__main__":
   main()
