import rclpy
from rclpy.node import Node

# ROS2用于传输图片的包
from sensor_msgs.msg import Image

# 用于格式转化的包
from cv_bridge import CvBridge

# OpenCv包
import cv2
from face_interfaces.srv import FaceDetect

# 用于获取共享目录的包
from ament_index_python.packages import get_package_share_directory
import threading
import time


def show_result(results: dict):
    # dict是Python内置的字典（Dictinary）类型
    # 在主线程中显示所有检测结果（独立于ROS节点）
    for image_name, data in results.items():
        display_image_ = data["image"]
        response_ = data["respomnse"]
        # 在图像上绘制人脸
        for i in range(response_.number):
            top_ = response_.top[i]
            left_ = response_.left[i]
            bottom_ = response_.bottom[i]
            right_ = response_.right[i]
            cv2.rectangle(
                display_image_, (left_, top_), (right_, bottom_), (255, 255, 0), 2
            )
        cv2.imshow(image_name, display_image_)
        # 第一个参数 image_name：字符串（窗口名称），每个窗口的名称唯一，用于区分不同图片的窗口；
        # 第二个参数 display_image：要显示的图像对象（numpy 数组）。

    cv2.waitKey(0)
    cv2.destoryAllWindows()
    print("所有结果已展示并关闭窗口")


class FaceDetectorClient(Node):
    def __init__(self):
        super().__init__("face_detector_client")
        self.client_ = self.create_client(FaceDetect, "/face_detect")
        self.bridge_ = CvBridge()

        # 获取图片路径
        self.test1_image_path_ = (
            get_package_share_directory("demo_python_service") + "/resource/test1.jpg"
        )
        self.test2_image_path_ = (
            get_package_share_directory("demo_python_service") + "/resource/test2.jpg"
        )

        # 加载图片（OpenCv格式）
        self.image_1_ = cv2.imread(self.test1_image_path_)
        self.image_2_ = cv2.imread(self.test2_image_path_)

        # 结果存储
        self.result_ = {}
        self.result_lock_ = threading.Lock()

    def send_request(self):
        # 发送等待请求
        # 等待服务上线
        while not self.client_.wait_for_service(timeout_sec=0.1):
            self.get_logger().info("等待服务端上线...")

        # 创建两个线程
        thread_1_ = threading.Thread(
            target=self.process_request, args=(self.image_1_, "image_1", 1)
        )
        thread_2_ = threading.Thread(
            target=self.process_request, args=(self.image_2_, "image_2", 2)
        )
        thread_1_.start()
        thread_2_.start()
        thread_1_.join()
        thread_2_.join()

    def process_request(self, image, image_name, image_num):
        # 处理单张图片（单线程执行）
        # 构造请求
        request = FaceDetect.Request()
        request.image = self.bridge_.cv2_to_imgmsg(image)

        # 发送异步请求
        future = self.client_.call_async(request)

        # 等待服务响应（非阻塞式的）
        while not future.done():
            time.sleep(0.1)

        # 获取任务的最终结果
        response = future.result()
        self.get_logger.info(
            f"图像 {image_name} 检测完成: {response.number} 张脸, 耗时 {response.use_time:.2f}s"
        )

        with self.result_lock_:
            self.result_[image_name] = {"response": response, "image": image.copy()}


def main(args=None):
    rclpy.init()
    client_ = FaceDetectorClient()

    # 启动分线程
    request_thread = threading.Thread(target=client_.send_request)

    # 主线程显示结果
    try:
        while (rclpy.ok) and request_thread.is_alive():
            rclpy.spin_once(client_, timeout_sec=0.1)
    finally:
        # 等待请求完成
        request_thread.join()
        print("所有请求已处理，正在展示结果...")
        show_result(client_.result_)
        client_.destroy_node()
        rclpy.shutdown()


if __name__ == "__mian__":
    main()
