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
        self.client_ = self.create_client(
            FaceDetector,       # 自定义的服务接口类型
            "/face_detect"      # 服务的话题名
        )
        self.bridge_ = CvBridge()
        self.test1_image_path_ = (
            get_package_share_directory("demo_python_service") + "/resource/test1.jpg"
        )
        self.image_ = cv2.imread(self.test1_image_path_)

    def send_request(self):
        # 等待服务是否上线
        while self.client_.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info(f"等待服务端上线...")
        # 构造Request
        request_ = FaceDetector.Request()
        request_.image = self.bridge_.cv2_to_imgmsg(self.image_)
        # 发送并 spin 等待服务处理完成
        # 现在的future波嗯灭有包含结果，需要等待服务端完成才会把数据放入future中
        future = self.client_.call_async(request_)

        # 等待服务端相应，等待future中有了数据
        rclpy.spin_until_future_complete(self, future)

        # 根据处理结果
        response = future.result()
        self.get_logger().info(
            f" 接收到响应 : 图像中共有：{response.number} 张脸，耗时 {response.use_time}"
        )
        self.show_face_locations(response)

    def show_face_locations(self, response):
        for i in range(response.number):
            top = response.top[i]
            left = response.left[i]
            right = response.right[i]
            bottom = response.bottom[i]
            cv2.rectangle(self.image_, (left, top), (right, bottom), (255, 0, 0), 2)
        cv2.imshow("Face Detection Result", self.image_)
        cv2.waitKey(0)


def main(args=None):
    rclpy.init(args=None)
    face_detect_client_ = FaceDetectorClient()
    face_detect_client_.send_request()
    rclpy.shutdown()
