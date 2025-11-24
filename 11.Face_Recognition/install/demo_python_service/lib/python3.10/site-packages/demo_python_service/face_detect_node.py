import time
import rclpy
from rclpy.node import Node
from face_interfaces.srv import FaceDetector
import face_recognition  # 人脸识别库，基于dlib
import cv2  # OpenC库，用于处理图片

# ROS2 的工具函数，用于获取功能包的共享目录路径（通常存放配置、资源文件）。
from ament_index_python.packages import get_package_share_directory

# 由于ROS2和OpenCv的图片格式并不兼容，所以用CvBridge进行格式转换
from cv_bridge import CvBridge  # 用于格式转换


class FaceDetectorionNode(Node):
    def __init__(self):
        super().__init__("face_detection_node")
        self.bridge = CvBridge()
        self.service = self.create_service(
            FaceDetector, "/face_detect", self.detec_face_callbask
        )
        self.default_image_path = (
            get_package_share_directory("demo_python_service") + "/resource/default.jpg"

            # 这个/resource/default.jpg是在安装目录下的目录
            # For example, if you install the package 'foo' into
            # '/home/user/ros2_ws/install' and you called this function with 'foo' as the
            # argument, then it will return '/home/user/ros2_ws/install/share/foo' as
            # the package's share directory.
        )
        self.get_logger().info(f"默认图片路径:{get_package_share_directory}")
        self.number_of_times_to_upsample = 2
        self.model = "cnn"

    def detec_face_callbask(self, request, response):
        if request.image.data:
            cv_image=self.bridge.imgmsg_to_cv2(request.image)
        else:
            cv_image=cv2.imread(self.default_image_path)

        start_time=time.time()
        self.get_logger().info('加载完毕，开始检测')

        face_locations = face_recognition.face_locations(
            cv_image,
            self.number_of_times_to_upsample,  # 图像放大次数,值越大，能检测到更小的人脸，但速度越慢.默认值为1，适合一般场景
            self.model,  # 检测算法选择
        )

        end_time = time.time()
        self.get_logger().info(f' 检测完成，耗时 {end_time-start_time}')

        for top, right, bottom, left in face_locations:
                cv2.rectangle(cv_image, (left, top), (right, bottom), (255, 0, 0), 4)
        
        cv2.imshow("face detector display",cv_image)
        cv2.waitKey(0)

        # response是我们自定义的消息接口的
        response.number=len(face_locations)
        response.use_time=end_time-start_time
        for top, right, bottom, left in face_locations:
             response.top.append(top)
             response.right.append(right)
             response.left.append(left)
             response.bottom.append(bottom)

        return response


def main(arg=None):
    rclpy.init(args=None)
    node = FaceDetectorionNode()
    rclpy.spin(node)
    rclpy.shutdown()