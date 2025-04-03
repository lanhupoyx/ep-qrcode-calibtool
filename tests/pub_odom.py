import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import tf
import math  # 确保导入了 math 模块

def publish_odometry():
    rospy.init_node('odometry_publisher')
    pub = rospy.Publisher('/base', Odometry, queue_size=50)
    rate = rospy.Rate(10)  # 10 Hz

    x = 0.0
    y = 0.0
    th = 0.0

    vx = 0.1
    vy = 0.0
    vth = 0.1

    last_time = rospy.Time.now()

    while not rospy.is_shutdown():
        current_time = rospy.Time.now()
        dt = (current_time - last_time).to_sec()

        delta_x = (vx * math.cos(th) - vy * math.sin(th)) * dt
        delta_y = (vx * math.sin(th) + vy * math.cos(th)) * dt
        delta_th = vth * dt

        x += delta_x
        y += delta_y
        th += delta_th

        odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)

        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        odom.pose.pose.position = Point(x, y, 0.0)
        odom.pose.pose.orientation = Quaternion(*odom_quat)

        odom.twist.twist.linear = Vector3(vx, vy, 0.0)
        odom.twist.twist.angular = Vector3(0.0, 0.0, vth)
        
        odom.pose.covariance[7] = 1

        pub.publish(odom)

        last_time = current_time
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_odometry()
    except rospy.ROSInterruptException:
        pass