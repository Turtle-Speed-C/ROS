1. 包含的库：
   1. 人脸识别库：face_recongnition
   2. OpenCv库，用于处理图片：cv2
   3. from face_interfaces.srv import FaceDetector
   4. ament_index_python.package中的get_package_share_directory：用于获取功能包的共享目录（ROS2包）。

2. 先获取图片的真实路径：

   1. `default_image_path=(get_package_share_directory("demo_python_service") + "/resource/default.jpg")`

      用于获取真实的路径。返回值是路径。

3. 使用`OpenCv`加载图片:

   1. `image=cv2.imread(default_image_path)`
   2. 参数的是图片的真实路径
   3. 返回值是`Numpy`格式的BGR彩色图片

4. 查找图片中人脸

   1. `face_locations=face_recognition.face_locations(image,number_of_times_to_spsample=2,model='cnn')`

      这个是用来查找人脸的函数。

      `image`是用`OpenCv`检测完之后，返回的BGR数据。

      `number_of_times_to_spsample=2`是图片放大的次数，图像放大次数,值越大，能检测到更小的人脸，但速度越慢.默认值为1，适合一般场景。

      `model="cnn"`是选择的检测算法选择，'hog'：方向梯度直方图，速度快但精度稍低，适合CPU。'cnn'：卷积神经网络，精度高但需要GPU加速

      返回一个列表，每个元素是一个元组 `(top, right, bottom, left)`

5. 绘制人脸边框：

   1. ```python
      for top, right, bottom, left in face_locations:
          cv2.rectangle(image, (left,top), (right,bottom), (255,0,0), 4)
      ```

      使用face_location中的top, right, bottom, left

      image是cv2.imread中来的BGR信息

       image：目标图像

      (left, top)：矩形左上角坐标

      (right, bottom)：矩形右下角坐标

      (255, 0, 0)：BGR格式颜色（蓝色）

      4：线条粗细（像素）

6. 显示结果：

   ```python
   cv2.imshow("Face Detector Result",image)
   ```

   imshow()：创建窗口显示图像

7.   等待按键

   ```
   cv2.waitKey(0)
   ```

   ​    waitKey(0)：等待按键，0表示无限等待