import tkinter as tk
import threading
import rospy

from submodule.topFrame import topFrame
from submodule.CalibrationTab import CalibrationTab
from submodule.ReadmeTab import ReadmeTab


def ros_thread():
    """
    ROS线程
    """
    rospy.spin()# 保持节点运行，直到被手动停止
    
def main():
    root = tk.Tk()#tinker
    app = topFrame(root)#顶层窗体
    
    # 初始化ROS节点
    rospy.init_node('odometry_subscriber', anonymous=True)
    thread_ros = threading.Thread(target=ros_thread)
    thread_ros.daemon = True  # 设置为守护线程
    thread_ros.start()
    
    tab1 = CalibrationTab(app)#标签页1
    thread_odom = threading.Thread(target=tab1.odom_monitor)
    thread_odom.daemon = True  # 设置为守护线程
    thread_odom.start()
    
    tab2 = ReadmeTab(app)#标签页4
    root.mainloop()# 主循环
    
#main函数
if __name__ == "__main__":
   main()