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
import threading
import requests
import time


class FaceDetectorClient(Node):
    def __init__(self):
        super().__init__("face_detect_client")
        self.client_ = self.create_client(FaceDetector, "/face_detect")
        self.bridge_ = CvBridge()
        self.test1_image_path_ = (
            get_package_share_directory("demo_python_service") + "/resource/test1.jpg"
        )
        self.test2_image_path_ = (
            get_package_share_directory("demo_python_service") + "/resource/test2.jpg"
        )
        self.image_1_ = cv2.imread(self.test1_image_path_)
        self.image_2_ = cv2.imread(self.test2_image_path_)
        # image_1_和image_2_是OpenCv格式的图片

    # 想要改称多线程最重要的就是加一个多线程的函数
    def send_request(self):
        # 等待服务是否上线
        while self.client_.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info(f"等待服务端上线...")
        thread_1_ = threading.Thread(
            target=self.process_request, args=(self.image_1_, "image_1", 1)
        )
        thread_2_ = threading.Thread(
            target=self.process_request, args=(self.image_2_, "image_2", 2)
        )
        thread_1_.start()
        thread_2_.start()

        # 等待两个线程都处理完成
        thread_1_.join()
        thread_2_.join()

        self.get_logger().info("所有窗口已关闭")

    def process_request(self, image, image_name, image_num):
        # 在独立的线程内处理单张图片
        # 构造Request
        request = FaceDetector.Request()
        request.image = self.bridge_.cv2_to_imgmsg(image)
        # 发送并 spin 等待服务处理完成
        # 现在的future波嗯灭有包含结果，需要等待服务端完成才会把数据放入future中
        future = self.client_.call_async(request)

        # 等待服务端相应，等待future中有了数据
        # rclpy.spin_until_future_complete(self, future)
        while not future.done():
            time.sleep(0.1)
            self.get_logger().info(f"等待")

        # 根据处理结果
        response = future.result()
        self.get_logger().info(
            f" 接收到响应 : 图像中共有：{response.number} 张脸，耗时 {response.use_time}"
        )
        # 存储结果而不是直接显示图片
        with self.results_lock:
            self.results[image_name] = {'response': response, 'image': image.copy()}

    def show_all_results(self, response, image, image_name, image_num):
        # 复制图像避免修改原始图像
        # display_image = image.copy()
        # for i in range(response.number):
        #     top = response.top[i]
        #     left = response.left[i]
        #     right = response.right[i]
        #     bottom = response.bottom[i]
        #     cv2.rectangle(display_image, (left, top), (right, bottom), (255, 0, 0), 2)
        # cv2.imshow(image_name, display_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 在主线程中显示所有结果
        with self.results_lock:
            for image_name, data in self.results.items():
                display_image = data['image']
                response = data['response']
                for i in range(response.number):
                    top = response.top[i]
                    left = response.left[i]
                    right = response.right[i]
                    bottom = response.bottom[i]
                    cv2.rectangle(display_image, (left, top), (right, bottom), (255, 0, 0), 2)
                cv2.imshow(image_name, display_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



def main(args=None):
    rclpy.init(args=None)
    face_detect_client_ = FaceDetectorClient()

    # 在单独线程中执行send_request
    thread=threading.Thread(target=face_detect_client_.send_request)
    thread.start()

    # 在主线程中使用spin
    try:
        while rclpy.ok() and thread.is_alive():
            rclpy.spin_once(face_detect_client_,timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        thread.join()   # 等待子线程
        face_detect_client_.show_all_results()  # 在主线程中显示图片
        face_detect_client_.destroy_node()
        rclpy.shutdown()
