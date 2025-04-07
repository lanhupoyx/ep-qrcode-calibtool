# import rospy
import tf.transformations
import numpy as np
import math
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TransformStamped
from tf2_geometry_msgs import do_transform_pose
from lib.minimum_enclosing_circle import Point
from lib.minimum_enclosing_circle import minimum_enclosing_circle

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class oneTrans:
    # 类属性
    x = 0.0
    y = 0.0
    yaw = 0.0
    center = 0.0
    radius = 0.0

    def __init__(self, x, y,yaw, center, radius):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.center = center
        self.radius = radius

class Calibration(): 
    def __init__(self, yaw_init,source_data):
        self.x_init = 0.0
        self.y_init = 0.0
        self.yaw_init = yaw_init
        self.baseData = self.getBaseData(source_data)
        
        self.listX = []
        self.result = []
  
    def calErrorRadius(self, searchRange):
        step = searchRange/10.0
        radiusMin = 100.0
        betterTrans = oneTrans(0,0,0,0,0)
        self.listX.clear()
        for x in np.arange(self.x_init-searchRange/2, self.x_init+searchRange/2, step):
            listY = []
            for y in np.arange(self.y_init-searchRange/2, self.y_init+searchRange/2, step):
                #计算二维码坐标
                trans_camera2base = self.inputTrans(x, y, self.yaw_init)
                pose_code2map_s = self.calPoseCode2Map(trans_camera2base, self.baseData)
                
                #计算外切圆
                points = []
                for pose in pose_code2map_s:
                    points.append(Point(pose.pose.position.x, pose.pose.position.y))
                center, radius = minimum_enclosing_circle(points)
                
                #筛选最优
                if radius < radiusMin:
                    radiusMin = radius
                    betterTrans = oneTrans(x, y, self.yaw_init, center, radius)
                listY.append(radius)
            self.listX.append(listY)
            
        print(f"betterTrans: {betterTrans.x}, {betterTrans.y}, {betterTrans.yaw}, {betterTrans.center}, {betterTrans.radius}")
        
        self.x_init = betterTrans.x
        self.y_init = betterTrans.y
        self.yaw_init = betterTrans.yaw
        self.result= [betterTrans.x, betterTrans.y, betterTrans.yaw, betterTrans.radius]

        return self.result

    def showArray(self):
        data = self.listX
        matrix = np.array(data)
        # 获取矩阵的大小
        rows, cols = matrix.shape

        # 创建一个网格
        x, y = np.meshgrid(np.arange(cols), np.arange(rows))

        # 将网格数据展平
        x = x.flatten()
        y = y.flatten()
        z = matrix.flatten()

        # 创建图形
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 绘制三维散点图
        ax.scatter(x, y, z, c=z, cmap='viridis')

        # 设置标签
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # 显示图形
        plt.show()
     
      
    def inputPose(self,x,y,yaw):
        pose_new = PoseStamped()
        pose_new.pose.position.x = x
        pose_new.pose.position.y = y
        pose_new.pose.position.z = 0
        q = tf.transformations.quaternion_from_euler(0, 0, yaw)
        pose_new.pose.orientation.x = q[0]
        pose_new.pose.orientation.y = q[1]
        pose_new.pose.orientation.z = q[2]
        pose_new.pose.orientation.w = q[3]
        return pose_new

    def inputTrans(self,x,y,yaw):
        trans_new = TransformStamped()
        trans_new.transform.translation.x =x
        trans_new.transform.translation.y =y
        trans_new.transform.translation.z =0
        q = tf.transformations.quaternion_from_euler(0, 0, yaw)
        trans_new.transform.rotation.x = q[0]
        trans_new.transform.rotation.y = q[1]
        trans_new.transform.rotation.z = q[2]
        trans_new.transform.rotation.w = q[3]
        return trans_new

    def inputTransQ(self,tx,ty,rx,ry,rz,rw):
        trans_new = TransformStamped()
        trans_new.transform.translation.x =tx
        trans_new.transform.translation.y =ty
        trans_new.transform.translation.z =0
        trans_new.transform.rotation.x = rx
        trans_new.transform.rotation.y = ry
        trans_new.transform.rotation.z = rz
        trans_new.transform.rotation.w = rw
        return trans_new

    def calPoseCode2Map(self,trans_camera2base, baseData):
        output = list()
        for data in baseData:
            pose_code2camera = self.inputPose(data[0], data[1], data[2])
            pose_code2base = do_transform_pose(pose_code2camera, trans_camera2base)
            trans_base2map = self.inputTransQ(data[3], data[4], data[5],data[6], data[7], data[8])
            pose_code2map = do_transform_pose(pose_code2base, trans_base2map)
            output.append(pose_code2map)
        return output

    def getBaseData1(self):
        baseData = list()
        baseData.append([-0.85, -5.63333, -0.691,  299.556671143, -200.383224487, 0.0114864693713, -0.00902685350151, 0.6871994298, 0.726321912529])
        baseData.append([-18.4875, -2.38333, -179.35,  298.95199585, -199.180801392, -0.00377531411797, -0.0058065311229, -0.720298283292, 0.693629882781])
        baseData.append([-9.5625, -0.433333, 91.272,  299.844390869, -199.456756592, 0.0102060148347, -0.00411991100218, 0.999882476137, 0.010672277564])
        baseData.append([-17.85, 17.55, -88.757,  298.646606445, -200.090820312, 0.00507920435218, -0.00997282823702, -0.00909543239073, 0.999896003337])
        
        for data in baseData:
            data[0] = data[0]/1000.0
            data[1] = data[1]/1000.0
            data[2] = data[2] * math.pi / -180.0
        
        return baseData
    
    def getBaseData(self,source_data):
        
        baseData = list()
        for row in source_data:
            q = tf.transformations.quaternion_from_euler(0, 0, row["m_yaw"])
            baseData.append([row["c_x"], row["c_y"], row["c_yaw"], row["m_x"], row["m_y"], q[0], q[1], q[2], q[3]])

        for data in baseData:
            data[0] = data[0]/1000.0
            data[1] = data[1]/1000.0
            data[2] = data[2] * math.pi / -180.0
        
        return baseData
        
        
if __name__ == "__main__": 
    calib = Calibration()