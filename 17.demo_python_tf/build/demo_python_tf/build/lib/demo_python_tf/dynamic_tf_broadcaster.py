import rclpy
import math
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


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

class DynamicTFBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_tf_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        # 动态 TF 需要持续发布，这里发布频率设置为 100 Hz
        self.timer_ = self.create_timer(0.01, self.publish_transform)
        self.angle = 0.0  # 用于动态旋转

    def publish_transform(self):
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "camera_link"
        transform.child_frame_id = "bottle_link"
        
        # 动态位置（可以让相机绕圆运动）
        transform.transform.translation.x = 0.5 + 0.2 * math.cos(self.angle)
        transform.transform.translation.y = 0.3 + 0.2 * math.sin(self.angle)
        transform.transform.translation.z = 0.6

        # 动态旋转（绕Z轴旋转）
        rotation_quart = euler_to_quaternion(0, 0, self.angle)

        transform.transform.rotation.x = rotation_quart[0]
        transform.transform.rotation.y = rotation_quart[1]
        transform.transform.rotation.z = rotation_quart[2]
        transform.transform.rotation.w = rotation_quart[3]

        self.tf_broadcaster.sendTransform(transform)
        self.get_logger().info(f'发布动态TF，角度: {math.degrees(self.angle):.1f}°')
        
        # 更新角度，实现动态效果
        self.angle += 0.05  # 每次增加约3度
        if self.angle > 2 * math.pi:
            self.angle = 0.0


def main():
    rclpy.init()
    tf_node = DynamicTFBroadcaster()
    rclpy.spin(tf_node)
    rclpy.shutdown()
    