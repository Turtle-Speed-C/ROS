import face_recognition  # 人脸识别库，基于dlib
import cv2  # OpenC库，用于处理图片
from ament_index_python.packages import get_package_share_directory
# ROS2 的工具函数，用于获取功能包的共享目录路径（通常存放配置、资源文件）。


def main():
    # 获取图片的真实路径，get_package_share_directory是ROS2的功能包，返回值是路径
    # 这里的参数是包名
    default_image_path = (
        get_package_share_directory("demo_python_service") + "/resource/default.jpg"
    )

    # 使用OpenCv加载图片
    # 返回 NumPy 数组格式的 BGR 彩色图像
    image = cv2.imread(default_image_path)

    # 查找图片中的人脸
    face_locations = face_recognition.face_locations(
        image,
        number_of_times_to_upsample=2,  # 图像放大次数,值越大，能检测到更小的人脸，但速度越慢.默认值为1，适合一般场景
        model="cnn",  # 检测算法选择
    )
    # 'hog'：方向梯度直方图，速度快但精度稍低，适合CPU
    # 'cnn'：卷积神经网络，精度高但需要GPU加速
    # 返回一个列表，每个元素是一个元组 (top, right, bottom, left)
    # 代表每个检测到的人脸的矩形边界坐标

    # 绘制每个人的人脸边框
    for top, right, bottom, left in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 4)

    # 遍历每个检测到的人脸位置
    # cv2.rectangle() 参数：
    # image：目标图像
    # (left, top)：矩形左上角坐标
    # (right, bottom)：矩形右下角坐标
    # (255, 0, 0)：BGR格式颜色（蓝色）
    # 4：线条粗细（像素）

    # 显示结果图像
    cv2.imshow("Face Detector Result", image)
    # imshow()：创建窗口显示图像

    cv2.waitKey(0)
    # waitKey(0)：等待按键，0表示无限等待
