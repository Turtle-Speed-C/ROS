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

from rcl_interfaces.msg import SetParametersResult


class FaceDetectorionNode(Node):
    def __init__(self):
        super().__init__("face_detection_node")     # 创建一个名为"face_detection_node"的ROS2节点

        self.bridge = CvBridge()    # 创建图片格式转换器（ROS2格式 ↔ OpenCV格式）

        self.service = self.create_service(
            FaceDetector,               # 服务的接口类型
            "/face_detect",             # 服务的名称（客户端通过这个名字调用）
            self.detec_face_callbask    # 当有请求是执行回调函数
        )

        # 获取默认测试图片的路径（当客户端没有发送图片时使用）
        self.default_image_path = (
            get_package_share_directory("demo_python_service")
            + "/resource/default.jpg"
            # demo_python_service是这个功能包
            # 这个/resource/default.jpg是在安装目录下的目录
            # 的意思是，获取demo_python_service功能包下的/resource/default.jpg
            # For example, if you install the package 'foo' into
            # '/home/user/ros2_ws/install' and you called this function with 'foo' as the
            # argument, then it will return '/home/user/ros2_ws/install/share/foo' as
            # the package's share directory.
        )

        self.get_logger().info(f"默认图片路径:{get_package_share_directory}")
        # self.number_of_times_to_upsample = 1
        # self.model = "hog"

        self.declare_parameter("face_location_upsample_times", 1)
        # 定义节点可以使用的参数及其默认值
        # 第一个参数是参数名，第二个是默认值
        self.declare_parameter("face_location_model", "hog")
        self.model_ = self.get_parameter("face_location_model").value
        # 从节点参数中读取参数值
        # 返回一个参数对象，需要用 .value 来获取实际值
        self.upsample_times_ = self.get_parameter("face_location_upsample_times").value

    def detec_face_callbask(self, request, response):
        # 处理输入图片
        if request.image.data:
            cv_image = self.bridge.imgmsg_to_cv2(request.image)
            # 如果请求中包含图片，则转换ROS2格式为OpenCV格式
        else:
            cv_image = cv2.imread(self.default_image_path)
            # 否则使用默认图片

        start_time = time.time()
        self.get_logger().info("加载完毕，开始检测")

        # 执行人脸检测
        # 返回值：[(top, right, bottom, left), ...]
        face_locations = face_recognition.face_locations(
            cv_image,                          # 输入图片
            self.number_of_times_to_upsample,  # 图像放大次数,值越大，能检测到更小的人脸，但速度越慢.默认值为1，适合一般场景
            self.model,                        # 检测算法选择
        )

        end_time = time.time()
        self.get_logger().info(f" 检测完成，耗时 {end_time-start_time}")

        # for top, right, bottom, left in face_locations:
        #         cv2.rectangle(cv_image, (left, top), (right, bottom), (255, 0, 0), 4)

        # cv2.imshow("face detector display",cv_image)
        # # 名字在窗口标题栏
        # cv2.waitKey(0)

        # response是我们自定义的消息接口的
        response.number = len(face_locations)       # 检测到人脸的数量
        response.use_time = end_time - start_time   # 检测耗时

        for top, right, bottom, left in face_locations:
            response.top.append(top)            
            response.right.append(right)
            response.left.append(left)
            response.bottom.append(bottom)
        '''
        append 是 Python 列表的一个方法，用于向列表末尾添加一个元素。
        人脸1：上=10，右=50，左=5，下=40
        人脸2：上=20，右=100，左=15，下=90
        response.top    = [10, 20]
        response.right  = [50, 100]
        response.left   = [5, 15]
        response.bottom = [40, 90]
        '''

        return response


def main(arg=None):
    rclpy.init(args=None)
    node = FaceDetectorionNode()
    rclpy.spin(node)
    rclpy.shutdown()
