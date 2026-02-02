import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String  # 消息接口的头文件
from queue import Queue
import threading
import time


class NovelSubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name}启动！")
        self.novel_queue_ = Queue()
        novel_subscriber_ = self.create_subscription(String, "novel", self.Callback, 10)
        self.speech_thread_ = threading.Thread(target=self.speak_thread)
        self.speech_thread_.start()

    def Callback(self, msg):
        self.novel_queue_.put(msg.data)

    def speak_thread(self):
        speaker = espeakng.Speaker()
        speaker.voice = "zh"
        while rclpy.ok():
            if self.novel_queue_.qsize() > 0:
                text = self.novel_queue_.get()
                self.get_logger().info(f"正在朗读{text}")
                speaker.say(text)       #说
                speaker.wait()          #等他说完
            else:
                time.sleep(1)


def main():
    rclpy.init()
    node = NovelSubNode("novel_sub")
    rclpy.spin(node)
    rclpy.shutdown()


"""
注意点：
    1. create_subscription中的第二个参数“topic（参数名称）”,需要根发布节点的名称一样
    2.在Callback中的msg，在不考虑地址之类的因素下，就是同一个数据。那边发一个，这边就收到一个。
        不需要在一个进程里，甚至不需要在一个电脑里。（分布式思想）
"""
