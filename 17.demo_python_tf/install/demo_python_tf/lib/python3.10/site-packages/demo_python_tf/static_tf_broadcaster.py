# 手眼坐标转换
import rclpy
import math
# 导入 math 库用于提供角度和弧度转换函数
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
# 作用: 静态变换广播器，用于发布两个坐标系之间的固定变换关系
# 用途: 当坐标系之间的相对位置不会改变时使用，比如机器人底座到激光雷达的固定偏移
from geometry_msgs.msg import TransformStamped
# 作用: 定义坐标变换的消息类型
# ros2 interface show geometry_msgs/msg/TransformStamped
# 这个消息描述了在stamp时刻，从frame_id坐标系到child_frame_id坐标系的3D变换关系。变换包含了平移和旋转两个部分。
# 与Transform的区别：
#     Transform: 只包含变换数据（平移+旋转）
#     TransformStamped: 包含变换数据 + 时间戳 + 坐标系信息

# 欧拉角转四元数的函数（替代tf_transformations）
def euler_to_quaternion(roll, pitch, yaw):
    """
    将欧拉角转换为四元数
    参数: roll, pitch, yaw (弧度)
    返回: [x, y, z, w] 四元数
    """
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    return [x, y, z, w]


class StaticTFBroadcaster(Node):
# StaticTFBroadcaster(Node): 表示StaticTFBroadcaster类继承自Node类
# Node是父类（超类/基类）
# StaticTFBroadcaster是子类（派生类）
# super().__init__('static_tf2_broadcaster'):
# 调用父类Node的__init__方法
# 传递节点名称'static_tf2_broadcaster'
    def __init__(self):
        super().__init__('static_tf2_broadcaster')
        # super(): Python的内置函数，用于访问父类
            # 返回一个代理对象，允许你调用父类的方法
            # 在多重继承中特别有用
        # __init__(): 构造函数/初始化方法
            # 每个Python类都有的特殊方法
            # 创建对象实例时自动调用
        # 相当于访问Node类的__init__，static_tf2_broadcaster为节点名

        self.static_broadcaster_ = StaticTransformBroadcaster(self)
        # StaticTransformBroadcaster(self): 创建静态变换广播器对象
        # StaticTransformBroadcaster: 从tf2_ros导入的类
        # (self): 将当前节点对象作为参数传递

        self.publish_static_tf()
         
    def publish_static_tf(self):
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "base_link"
        transform.child_frame_id = "camera_link"
        transform.transform.translation.x = 0.5
        transform.transform.translation.y = 0.3  # 修正：这里应该是y坐标
        transform.transform.translation.z = 0.6  # 修正：这里应该是z坐标

        # 欧拉角转化为四元数（使用自定义函数）
        rotation_quart = euler_to_quaternion(math.radians(180), 0, 0)

        transform.transform.rotation.x = rotation_quart[0]
        transform.transform.rotation.y = rotation_quart[1]
        transform.transform.rotation.z = rotation_quart[2]
        transform.transform.rotation.w = rotation_quart[3]

        # 发布静态坐标转换
        # 转换并且发布
        self.static_broadcaster_.sendTransform(transform)
        self.get_logger().info(f' 发布 TF:{transform}')



def main():
    rclpy.init()
    static_tf_broadcaster = StaticTFBroadcaster()  # 修正变量名
    rclpy.spin(static_tf_broadcaster)  # 修正变量名
    rclpy.shutdown()


if __name__ == '__main__':
    main()
