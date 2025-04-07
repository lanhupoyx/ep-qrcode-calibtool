import threading
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from src.lib.Calibration import Calibration
# from reboot import reboot
# from topFrame import topFrame

import rospy
import tf.transformations
from nav_msgs.msg import Odometry


# 创建一个锁对象
lock = threading.Lock()

class CalibrationTab(): 
    def __init__(self, app):
        self.tab = app.tab1
        
        # 添加标签页到 Notebook
        self.notebook = app.notebook
        self.notebook.add(self.tab, text=' 相机标定 ')
        
        # 雷达定位状态指示
        self.label_lidar = ttk.Label(self.tab, text="Lidar loc:")
        self.label_lidar.grid(row=0, column=0, rowspan=1, padx=10, pady=10)
        self.canvas_lidar = tk.Canvas(self.tab, width=60, height=30, bg="#d9d9d9")
        self.canvas_lidar.grid(row=0, column=1, rowspan=1, padx=10, pady=10)
        self.light_lidar = self.canvas_lidar.create_rectangle(0, 0, 60, 30, fill="red")  # 默认灰色
        # 二维码扫码状态指示
        self.label_qrcode = ttk.Label(self.tab, text="QR-code:")
        self.label_qrcode.grid(row=1, column=0, rowspan=1, padx=10, pady=10)
        self.canvas_qrcode = tk.Canvas(self.tab, width=60, height=30, bg="#d9d9d9")
        self.canvas_qrcode.grid(row=1, column=1, rowspan=1, padx=10, pady=10)
        self.light_qrcode = self.canvas_qrcode.create_rectangle(0, 0, 60, 30, fill="red")  # 默认灰色
        # # x初始值
        # self.label_x = ttk.Label(self.tab, text="x:")
        # self.label_x.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        # self.entry_x = ttk.Entry(self.tab, width=10)
        # self.entry_x.grid(row=0, column=3, rowspan=2, padx=10, pady=10)
        # # y初始值
        # self.label_y = ttk.Label(self.tab, text="y:")
        # self.label_y.grid(row=2, column=2, rowspan=2, padx=10, pady=10)
        # self.entry_y = ttk.Entry(self.tab, width=10)
        # self.entry_y.grid(row=2, column=3, rowspan=2, padx=10, pady=10)
        # yaw初始值
        self.label_yaw = ttk.Label(self.tab, text="yaw(deg):")
        self.label_yaw.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        self.entry_yaw = ttk.Entry(self.tab, width=10)
        self.entry_yaw.grid(row=0, column=3, rowspan=2, padx=10, pady=10)
        # 固定值选择
        # self.selected_option = tk.StringVar()
        # self.option1 = tk.Radiobutton(self.tab, text="固定x-y", variable=self.selected_option, value="x-y")
        # self.option2 = tk.Radiobutton(self.tab, text="固定yaw", variable=self.selected_option, value="yaw")
        # self.option1.grid(row=0, column=4, rowspan=3, padx=10, pady=10)
        # self.option2.grid(row=3, column=4, rowspan=3, padx=10, pady=10)
        # self.selected_option.set("yaw")  # 默认选中
        # 功能按钮
        self.button_del = ttk.Button(self.tab, text="删除", command=self.acktionDelete)
        self.button_del.grid(row=0, column=4, rowspan=1, padx=10, pady=10)
        self.button_cal = ttk.Button(self.tab, text="添加", command=self.acktionAdd)
        self.button_cal.grid(row=1, column=4, rowspan=1, padx=10, pady=10)
        
        self.button_add = ttk.Button(self.tab, text="计算", command=self.acktionCal)
        self.button_add.grid(row=0, column=5, rowspan=2, padx=10, pady=10)
        # 数据展示
        columns = ("index", "c_x", "c_y", "c_yaw", "m_x", "m_y", "m_yaw")
        self.dataShow = ttk.Treeview(self.tab, columns=columns, show="headings")
        self.dataShow.grid(row=6, column=0, columnspan=6, padx=10, pady=10)

        # 设置列标题
        for col in columns:
            self.dataShow.heading(col, text=col.capitalize())
            self.dataShow.column(col, width=100, anchor="center")
        self.data = []
                
        # 初始化文档内容
        self.document_lines = []
        self.document_lines_temp = []

        self.lidarOK = False
        self.qrcodeOK = False
        self.msg = Odometry()
        self.addIndex = 0
        
        rospy.Subscriber("/base", Odometry, self.odom_callback)
        
        # self.initDataTest()
        
    def acktionAdd(self):
        if not (self.lidarOK and self.qrcodeOK):
            messagebox.showwarning("警告", "Lidar或二维码无数据！")
            return
        else:
            lock.acquire()
            msg = self.msg
            lock.release()
            
            self.addIndex  = self.addIndex + 1
            self.data.append({"index":self.addIndex, 
                              "c_x":msg.pose.covariance[7], 
                              "c_y":msg.pose.covariance[8], 
                              "c_yaw":msg.pose.covariance[9],
                              "m_x":msg.pose.pose.position.x,
                              "m_y":msg.pose.pose.position.y, 
                              "m_yaw":tf.transformations.euler_from_quaternion([msg.pose.pose.orientation.x,
                                                                                msg.pose.pose.orientation.y,
                                                                                msg.pose.pose.orientation.z,
                                                                                msg.pose.pose.orientation.w])[2]})
            self.updateDataShow()
        
    def acktionDelete(self):
        # 获取当前选中的行
        selected_items = self.dataShow.selection()
        if selected_items:
            response = messagebox.askyesno("确认操作", "你确定要删除选中的数据吗？")
            if not response:
                print("用户点击了'否'，取消操作")
                return
            else:
                for item in selected_items:
                    # 获取选中行的值
                    item_values = self.dataShow.item(item, "values")
                    print(f"Delete item: {item_values}")
                    
                    for row in self.data:
                        if(row["index"] == int(item_values[0])):
                            self.data.remove(row)
        else:
            messagebox.showwarning("警告", "未选择数据")
            return

        self.updateDataShow()
            
    def acktionCal(self):
        # init_x = 0.0
        # try:
        #     init_x = float(self.entry_x.get())
        # except ValueError:
        #     messagebox.showerror("错误", "x初始值错误！")
        #     return
            
        # init_y = 0.0
        # try:
        #     init_y = float(self.entry_y.get())
        # except ValueError:
        #     messagebox.showerror("错误", "y初始值错误！")
        #     return
        
        init_yaw = 0.0
        try:
            init_yaw = float(self.entry_yaw.get())*math.pi/180.0 #转换成rad
        except ValueError:
            messagebox.showerror("错误", "yaw初始值错误！")
            return
            
        if len(self.data) < 4:
            messagebox.showwarning("警告", "采集数据量少于4")
            return
        else:
            response = messagebox.askyesno("确认操作", "你确定要计算吗？")
            if not response:
                return
            else:
                calib = Calibration(init_yaw, self.data)
                searchRange = 10
                while searchRange > 0.001:
                    calib.calErrorRadius(searchRange)
                    searchRange = searchRange/5.0
                    print(searchRange)
                print(calib.result)
                # 使用格式化字符串将数据嵌入到提示信息中
                x = round(calib.result[0], 4)
                y = round(calib.result[1], 4)
                yaw = round(calib.result[2]*180.0/math.pi, 4)
                radius = round(calib.result[3], 4)
                info_message = f"x: {x}(m)\ny: {y}(m)\nyaw: {yaw}(deg)\nradius: {radius}(m)"
                # 显示信息提示框
                messagebox.showinfo("标定结果", info_message)
                calib.showArray()
                
                
        
    def odom_callback(self, msg):
        lock.acquire()
        self.msg = msg
        self.msg.header.stamp = rospy.Time.now()
        lock.release()

    def odom_monitor(self):
        rate = rospy.Rate(10)  # 设置循环频率为 10 Hz
        while not rospy.is_shutdown():  # 检查是否接收到关闭信号
            lock.acquire()
            msg = self.msg
            lock.release()
            
            current_time = rospy.Time.now()
            elapsed_time = current_time - msg.header.stamp
            
            if elapsed_time.to_sec() > 0.2:
                self.canvas_lidar.itemconfig(self.light_lidar, fill="red")
                self.lidarOK = False
                self.canvas_qrcode.itemconfig(self.light_qrcode, fill="red")
                self.qrcodeOK = False
            else:              
                if((0 == msg.pose.pose.position.x) and (0 == msg.pose.pose.position.y) and(0 == msg.pose.pose.position.z)):
                    self.canvas_lidar.itemconfig(self.light_lidar, fill="red")
                    self.lidarOK = False
                else:
                    self.canvas_lidar.itemconfig(self.light_lidar, fill="green")
                    self.lidarOK = True

                if((0 == msg.pose.covariance[7]) and (0 == msg.pose.covariance[8]) and(0 == msg.pose.covariance[9])):
                    self.canvas_qrcode.itemconfig(self.light_qrcode, fill="red")
                    self.qrcodeOK = False
                else:
                    self.canvas_qrcode.itemconfig(self.light_qrcode, fill="green")
                    self.qrcodeOK = True
            # 等待直到下一个循环周期
            rate.sleep()

    def initDataTest(self):
        # self.entry_x.insert(0, "0.592")
        # self.entry_y.insert(0, "0.3405")  # 0 表示从第 0 个字符位置开始插入
        self.entry_yaw.insert(0, "91.96")

        self.addIndex  = self.addIndex + 1
        self.data.append({"index":self.addIndex, 
                          "c_x":-0.85, 
                          "c_y":-5.63333, 
                          "c_yaw":-0.691, 
                          "m_x":299.556671143, 
                          "m_y":-200.383224487, 
                          "m_yaw":tf.transformations.euler_from_quaternion([0.0114864693713, -0.00902685350151, 0.6871994298, 0.726321912529])[2]})
        self.addIndex  = self.addIndex + 1
        self.data.append({"index":self.addIndex, 
                          "c_x":-18.4875, 
                          "c_y":-2.38333, 
                          "c_yaw":-179.35, 
                          "m_x":298.95199585, 
                          "m_y":-199.180801392, 
                          "m_yaw":tf.transformations.euler_from_quaternion([-0.00377531411797, -0.0058065311229, -0.720298283292, 0.693629882781])[2]})
        self.addIndex  = self.addIndex + 1
        self.data.append({"index":self.addIndex, 
                          "c_x":-9.5625, 
                          "c_y":-0.433333, 
                          "c_yaw":91.272, 
                          "m_x":299.844390869, 
                          "m_y":-199.456756592, 
                          "m_yaw":tf.transformations.euler_from_quaternion([0.0102060148347, -0.00411991100218, 0.999882476137, 0.010672277564])[2]})
        self.addIndex  = self.addIndex + 1
        self.data.append({"index":self.addIndex, 
                          "c_x":-17.85, 
                          "c_y":17.55, 
                          "c_yaw":-88.757, 
                          "m_x":298.646606445, 
                          "m_y":-200.090820312, 
                          "m_yaw":tf.transformations.euler_from_quaternion([0.00507920435218, -0.00997282823702, -0.00909543239073, 0.999896003337])[2]})
        self.updateDataShow()

    def updateDataShow(self):
        for item in self.dataShow.get_children():
            self.dataShow.delete(item)
        for row in self.data:
            self.dataShow.insert("", "end", values=(round(row["index"], 3), 
                                                    round(row["c_x"], 3), round(row["c_y"], 3), 
                                                    round(row["c_yaw"], 3), 
                                                    round(row["m_x"], 3), round(row["m_y"], 3), 
                                                    round(row["m_yaw"]*180.0/math.pi, 3)))


# def ros_thread():
#     """
#     ROS线程
#     """
#     rospy.spin()# 保持节点运行，直到被手动停止
    
# def main():
#     root = tk.Tk()#tinker
#     app = topFrame(root)#顶层窗体
    
#     # 初始化ROS节点
#     rospy.init_node('odometry_subscriber', anonymous=True)
#     thread_ros = threading.Thread(target=ros_thread)
#     thread_ros.daemon = True  # 设置为守护线程
#     thread_ros.start()
    
#     tab1 = Calibration(app)#标签页1
#     thread_odom = threading.Thread(target=tab1.odom_monitor)
#     thread_odom.daemon = True  # 设置为守护线程
#     thread_odom.start()
       
#     root.mainloop()# 主循环
    
# #main函数
# if __name__ == "__main__":
#    main()