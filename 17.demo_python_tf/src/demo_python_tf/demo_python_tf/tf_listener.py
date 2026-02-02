import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer

# from tf_transformations import euler_from_quaternion
from transforms3d.euler import quat2euler


class TFListener(Node):
    def __init__(self):
        super().__init__("tf2_listener")
        self.buffer_ = Buffer()
        # 它订阅TF话题并将坐标变换更新传播到缓冲区对象中
        self.listener_ = TransformListener(self.buffer_, self)
        self.timer_ = self.create_timer(1, self.get_transform)

    def get_transform(self):
        try:
            result = self.buffer_.lookup_transform(
                "base_link",
                "bottle_link",
                rclpy.time.Time(seconds=0),
                rclpy.time.Duration(seconds=1),
            )
            transform = result.transform
            rotation_euler = quat2euler(
                [
                    transform.rotation.x,
                    transform.rotation.y,
                    transform.rotation.z,
                    transform.rotation.w,
                ]
            )

            # 优化日志输出格式，更易读
            self.get_logger().info(
                f"平移: x={transform.translation.x:.2f}, y={transform.translation.y:.2f}, z={transform.translation.z:.2f}\n"
                f"旋转四元数: x={transform.rotation.x:.2f}, y={transform.rotation.y:.2f}, z={transform.rotation.z:.2f}, w={transform.rotation.w:.2f}\n"
                f"旋转欧拉角(弧度): roll={rotation_euler[0]:.2f}, pitch={rotation_euler[1]:.2f}, yaw={rotation_euler[2]:.2f}"
            )
        except Exception as e:
            self.get_logger().warn(f"不能够获取坐标变换，原因: {str(e)}")


def main():
    rclpy.init()
    node = TFListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "main":
    main()
