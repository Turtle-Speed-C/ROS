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

# 用于ROS2和OpenCv格式转换
from cv_bridge import CvBridge

from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType


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
        # 等待服务是否上线
        while self.client_.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info(f"等待服务端上线...")
        # 构造Request
        request_ = FaceDetector.Request()
        request_.image = self.bridge_.cv2_to_imgmsg(self.image_)
        # 发送并 spin 等待服务处理完成
        # 现在的future中没有包含结果，需要等待服务端完成才会把数据放入future中
        future = self.client_.call_async(request_)

        # 等待服务端相应，等待future中有了数据
        rclpy.spin_until_future_complete(self, future)

        # 根据处理结果
        response = future.result()
        self.get_logger().info(
            f" 接收到响应 : 图像中共有：{response.number} 张脸，耗时 {response.use_time}"
        )
        # 注释show_face_loaction，防止显示阻塞无法多次请求
        # self.show_face_locations(response)

    def update_detect_model(self, model):
        # 1.创建一个参数对象
        param = Parameter()
        # param = Parameter() 是创建 ROS2 标准参数描述对象 的核心语句，用于实例化 rcl_interfaces.msg.Parameter 类（ROS2 官方定义的参数消息类型），目的是封装「单个参数的名称 + 类型 + 值」，作为 SetParameters 服务请求的最小单元 —— 因为 SetParameters 服务的请求字段 parameters 是 Parameter 对象列表，每个要修改的参数都必须先封装成这个对象才能被服务端识别。
        param.name = "face_location_model"

        # 2.创建参数对象并赋值
        new_model_value = ParameterValue()
        # 来源：from rcl_interfaces.msg import ParameterValue；
        # 本质：ROS2 官方定义的「参数值描述消息类」，专门用于封装 “参数类型 + 具体值”，是 Parameter 对象 value 字段的唯一合法类型（不能用普通字符串 / 数字替代）。
        new_model_value.type = ParameterType.PARAMETER_STRING
        new_model_value.string_value = model
        param.value = new_model_value  # 将「参数名（param.name）」和「参数类型 + 值（param.value）」绑定，让 param 成为一个完整的、可被服务端解析的参数对象。

        # 3.请求更新参数并处理
        response = self.call_set_parameters([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f" 参数 {param.name} 设置为 {model}")
            else:
                self.get_logger().info(f" 参数设置失败，原因为：{result.reason}")

    def call_set_parameters(self, parameters):
        # 1.创建一个客户端，并等待服务上线
        client = self.create_client(
            SetParameters,  # 服务的数据类型，- SetParameters 是 ROS2 官方定义的 “设置节点参数” 的标准服务类型，包含 Request（要设置的参数列表）和 Response（设置结果）两个部分；
            "/face_detection_node/set_parameters",  # 服务的路径 目标节点的名称（要修改参数的节点）/ 该节点提供的 “设置参数” 服务的默认名称
            # 在正常的服务中，这个是服务的话题名
        )
        while not client.wait_for_service(timeout_sec=0.1):
            self.get_logger().info(" 等待参数设置服务端上线 ...")

        # 2.创建请求对象
        request = SetParameters.Request()
        request.parameters = parameters

        # 3. 异步调用、等待并返回响应结果
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        return response

    def show_face_locations(self, response):
        """
        在这个代码中，使用了rectanle在self.image_（OpenCv形式的图片），接着会使用cv2.imshow显示在屏幕上。
        cv2.waitKey(0)是一直等待，
        阻塞主线程直到用户按键，这时节点不会继续执行后续代码（包括再次发送请求或退出），所以如果想在一次程序运行中多次发起请求并处理响应，就不能用 waitKey(0)。
        """
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
    face_detect_client_.update_detect_model("hog")
    face_detect_client_.send_request()
    face_detect_client_.update_detect_model("cnn")
    face_detect_client_.send_request()
    rclpy.spin(face_detect_client_)
    rclpy.shutdown()
