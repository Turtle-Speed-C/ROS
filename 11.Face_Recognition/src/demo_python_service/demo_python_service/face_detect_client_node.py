import rclpy

# 提供ROS节点的初始化、创建、通信等基础通信
from rclpy.node import Node

# 导入ROS2节点的基类
from face_interfaces.srv import FaceDetector

# 导入自定义的服务接口FaceDetector
from sensor_msgs.msg import Image

# ROS2用于传输图片的包
from ament_index_python.packages import get_package_share_directory

# ROS2用于获取共享目录的包
import cv2
from cv_bridge import CvBridge

# 用于ROS2和OpenCv格式转换


class FaceDetectorClient(Node):
    def __init__(self):
        super().__init__("face_detect_client")
        self.client_ = self.create_client(FaceDetector, "/face_detect")
        self.bridge_ = CvBridge()
        self.test1_image_path_ = (
            get_package_share_directory("demo_python_service") + "/resource/test1.jpg"
        )
        self.image_ = cv2.imread(self.test1_image_path_)

    def send_request(self):
        pass

    