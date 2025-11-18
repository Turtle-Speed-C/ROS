import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus
import psutil  # psutil可以获取系统的CPU、内存以及网络信息
import platform


class SysStatusPub(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.status_publisher_ = self.create_publisher(SystemStatus, "sys_status", 10)
        self.timer_ = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        cpu_percent_ = psutil.cpu_percent()  # 获取CPU使用率的百分比
        memory_info_ = psutil.virtual_memory()  # 获取系统内存信息
        net_io_counters_ = psutil.net_io_counters()  # 获取网络IO统计信息

        msg_ = SystemStatus()
        msg_.stamp = self.get_clock().now().to_msg()
        # self.get_clock()：获取ROS2时钟对象
        # now()：获取当前时间
        # to_msg()：改变为msg格式
        msg_.host_name = platform.node()  # 获取计算机的主机名称
        msg_.cpu_percent = cpu_percent_
        msg_.memory_percent = memory_info_.percent
        msg_.memory_total = memory_info_.total / 1024 / 1024
        msg_.memory_available = memory_info_.available / 1024 / 1024
        msg_.net_sent = net_io_counters_.bytes_sent / 1024 / 1024
        msg_.net_recv = net_io_counters_.bytes_recv / 1024 / 1024

        self.get_logger().info(f"发布{str(msg_)}")
        self.status_publisher_.publish(msg_)


def main():
    rclpy.init()
    node = SysStatusPub("sys_status_pub")
    rclpy.spin(node)
    rclpy.shutdown()
