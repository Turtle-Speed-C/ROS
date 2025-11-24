1. 包含的库：

   1. 人脸识别库：face_recongnition
   2. OpenCv库，用于处理图片：cv2
   3. ament_index_python.package中的get_package_share_directory：用于获取功能包的共享目录（ROS2包）。
   4. cv_bridge中的CvBridge：用于格式转换

2. 创建一个类FaceDetectorionNode，用于检测人脸：

   1. 初始化：

      1. ```python
         self.bridge = CvBridge()
         ```

         创建CvBridge实例，用于图片格式转换

      2. ```python
         self.service = self.create_service(
             FaceDetector, "/face_detect", self.detec_face_callbask
         )
         ```

         创建服务。

         参数：

         	1. 服务的消息格式
         	1. 服务名称
         	1. 回调函数

      3. ```python
         self.default_image_path = (
         get_package_share_directory("demo_python_service")+"/resource/default.jpg"
         )
         ```

         这个/resource/default.jpg是在安装目录下的目录

         For example, if you install the package 'foo' into

         '/home/user/ros2_ws/install' and you called this function with 'foo' as the

         argument, then it will return **'/home/user/ros2_ws/install/share/foo'** as

         the package's share directory.

   2. detec_face_callbask(self, request, response):

      1. ```python
         if request.image.data:
         	cv_image=self.bridge.imgmsg_to_cv2(request.image)
         else:
             cv_image=cv2.imread(self.default_image_path)
         ```

         如果request.image.data（图像数据）不为空，则直接使用imgmsg_to_cv2，将图像接口消息格式转换成 opencv 的格式。

         如果为空，则直接从默认文件路径读取图像

      2. ```python
         response.number=len(face_locations)
         response.use_time=end_time-start_time
         for top, right, bottom, left in face_locations:
              response.top.append(top)
              response.right.append(right)
              response.left.append(left)
              response.bottom.append(bottom)
         
         return response
         ```

         最后对 response 各个数据分别赋值后返回。

   3. main

      1. `arg=None`是 Python 中为函数参数设置**默认值**的写法：
         1. **不传参数**：直接用`main()`调用时，`arg`会自动取默认值`None`。
         2. **传参数**：如果用`main("some_value")`调用，`arg`就会被赋值为传入的`"some_value"`。

