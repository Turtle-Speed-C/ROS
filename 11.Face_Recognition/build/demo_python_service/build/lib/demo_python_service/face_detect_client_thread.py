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
        # 添加用于存储结果的变量
        self.results = {}
        # 初始化一个空字典，作为共享数据容器，用于存储以image_name为键、任务结果（响应 + 图像）为值的键值对。
        # 因为是类的实例属性，多线程操作同一个类实例时，所有线程都会访问这个共享字典。
        self.results_lock = threading.Lock()
        # image_1_和image_2_是OpenCv格式的图片
        # 创建一个 ** 线程互斥锁（Mutex）** 实例。
        # threading.Lock()是 Python 标准库中最基础的线程同步原语。
        # 它的核心特性是：同一时间只能有一个线程获取到这个锁，其他线程必须等待锁被释放后才能继续。这是保证后续字典操作线程安全的关键。

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

    def process_request(self, image, image_name, image_num):
        # image: OpenCv格式的图片, image_name: 图片名称字符串, image_num: 图片编号（用于日志）
        # 在独立的线程内处理单张图片
        # 构造Request
        request = FaceDetector.Request()
        request.image = self.bridge_.cv2_to_imgmsg(image)
        # 发送并 spin 等待服务处理完成
        # 现在的future包没有包含结果，需要等待服务端完成才会把数据放入future中
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
        # with是一个上下文管理器，能够自动加锁和释放锁
        # 它会自动在进入代码块时调用 results_lock.acquire()（获取锁），退出时调用 results_lock.release()（释放锁）。
        # 进入代码块时：调用self.results_lock.acquire()—— 尝试获取锁，如果锁已被其他线程占用，则当前线程阻塞等待。
        # 退出代码块时（即使发生异常）：自动调用self.results_lock.release()—— 释放锁，让其他等待的线程可以获取。
        with self.results_lock:
            # image_name作为唯一标识（比如图像文件名、任务 ID），确保每个结果有对应的索引。
            # 这里确定了该字典有两个值：response和image
            # 存入的值是一个包含两个字段的字典：
            # 'response'：存储任务的处理结果（比如图像识别的标签、检测的坐标、API 返回的数据等）。
            # 'image': image.copy()：关键细节—— 这里不是直接存image对象本身，而是调用copy()方法创建副本。因为 Python 中对象是引用传递，如果直接存image，后续其他线程对原image对象的修改（比如像素调整、裁剪）会同步影响字典中已存储的值；而copy()能保证存入的是独立的 “快照”，避免数据被意外篡改。
            self.results[image_name] = {"response": response, "image": image.copy()}

    def show_all_results(self):
        # 在主线程中显示所有结果
        with self.results_lock:
            # data：self.results 对应键的值 —— 一个字典，结构为 {"response": response, "image": image.copy()}，由 process_request() 写入。
            # item（如果你指的是 for ... in self.results.items() 中的项）：每一项是 (键, 值) 二元组，也就是 (image_name, data)。
            for image_name, data in self.results.items():
                display_image = data["image"]
                response = data["response"]
                # range(n) 是一个内置函数，用于生成从 0 到 n-1 的整数序列。
                for i in range(response.number):
                    top = response.top[i]
                    left = response.left[i]
                    right = response.right[i]
                    bottom = response.bottom[i]
                    cv2.rectangle(
                        display_image, (left, top), (right, bottom), (255, 0, 0), 2
                    )
                cv2.imshow(image_name, display_image)
        cv2.waitKey(0)
        # waitkey只能在主线程中使用,否则会导致线程阻塞
        # 如果在子线程中调用waitKey(0)，该子线程会永远阻塞
        # 会导致thread.join()永远无法返回，程序无法正常退出
        # OpenCV的GUI必须在主线程中执行，这是GUI框架的限制
        
        cv2.destroyAllWindows() #关闭所有的OpenCV窗口
        self.get_logger().info("所有窗口已关闭")


def main(args=None):
    rclpy.init(args=args)
    face_detect_client_ = FaceDetectorClient()

    # 在单独线程中执行send_request
    thread = threading.Thread(target=face_detect_client_.send_request)
    thread.start()

    # 在主线程中使用spin
    try:
        while rclpy.ok() and thread.is_alive():
            rclpy.spin_once(face_detect_client_, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        thread.join()  # 等待子线程
        face_detect_client_.show_all_results()  # 在主线程中显示图片
        face_detect_client_.destroy_node()
        rclpy.shutdown()
