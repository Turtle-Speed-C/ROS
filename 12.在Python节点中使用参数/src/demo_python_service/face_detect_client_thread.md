# 1.spin机制和spin_once机制
## 1.1.spin() - 阻塞式消息循环
    rclpy.spin(node)
    核心作用：
        进入无限循环，持续处理ROS2消息队列中的回调函数
    特点：
        会一直阻塞，直到ros::ok()返回false（即节点被关闭）
        会尽可能快地处理消息，但"没事干的时候不会占用太多CPU资源"
        适合简单的ROS2节点，无需其他业务逻辑

## 1.2.spin_once() - 非阻塞式处理
    rclpy.spin_once(node, timeout_sec=0.1)
    核心作用：处理一次消息队列中的回调，然后立即返回
    特点：
        不会阻塞主线程，可以在循环中反复调用
        适合需要同时执行其他业务逻辑的场景
        需要自己控制循环频率（如设置timeout_sec）

## 1.3.为什么在主线程中使用spin_once？
    在我们的客户端代码中，我们使用rclpy.spin_once(face_detect_client_, timeout_sec=0.1)，因为：

    我们需要同时处理ROS2消息和等待子线程完成
    如果使用rclpy.spin()，主线程会一直阻塞，无法执行thread.join()和后续的GUI操作
    通过spin_once()，我们可以在主线程中保持ROS2节点活跃，同时检查子线程状态

# 2.为什么需要这样设计？（核心问题：多个阻塞机制的协调）
根本问题：
    ROS2的spin()阻塞、OpenCV的waitKey()阻塞、线程的join()阻塞，这三者交织在一起，容易导致程序无法正常退出。

                    解决方案设计思路
    机制	        位置	    作用	        为什么这样设计
    ROS2 spin      主线程	 处理ROS2消息	    确保节点能接收和处理消息
    spin_once     主线程循环  非阻塞式处理消息	  避免主线程被spin()完全阻塞
    子线程	        子线程	 处理ROS2请求和数据	  保持主线程自由处理GUI
    waitKey	       主线程	显示图片并等待用户输入 保证GUI在主线程中执行
destroyAllWindows  主线程	清理窗口资源	     确保程序退出时资源被释放

# 3.为什么这样设计最合理？
    主线程：负责ROS2消息循环和GUI显示（符合ROS2和GUI框架的要求）
    子线程：负责业务逻辑（发送请求、处理结果）
    数据共享：使用线程锁安全地在子线程和主线程之间传递数据
    退出顺序：
        等待子线程完成
        在主线程中显示所有结果
        等待用户按键
        清理窗口资源
        销毁ROS2节点
# 4.face_detect_client_.destroy_node()
1. 作用：清理ROS2节点资源
2. 为什么在finally中调用：
      finally:
        thread.join()
        face_detect_client_.show_all_results()
        face_detect_client_.destroy_node()
        rclpy.shutdown()
3. 确保无论程序如何退出（正常或异常），节点资源都能被正确释放
这是ROS2节点生命周期管理的标准做法

# 5.try except finally
1. try：包含可能引发异常的代码（如ROS2通信）
2. except：捕获并处理异常（如用户按Ctrl+C）
3. finally：无论是否发生异常，都会执行的代码
   1. 确保资源被正确清理（节点销毁、窗口关闭）
   2. 避免因异常导致资源泄漏

# 6.self.results_lock = threading.Lock()
1. 作用：保护共享数据结构（self.results）的线程安全
2. 为什么需要：
   1. 子线程和主线程同时访问self.results
   2. 没有锁保护，会导致数据竞争（如一个线程正在写，另一个线程正在读）
3. 使用方式：
with self.results_lock:
    self.results[image_name] = {'response': response, 'image': image.copy()}
用with语句确保锁的正确获取和释放
即使发生异常，锁也会被释放

# 7.future的方法详解
1. get()	获取结果（会阻塞等待）	response = future.result()
2. get(timeout, unit)	在指定时间内获取结果	response = future.result(timeout=5)
3. cancel(mayInterrupt)	尝试取消任务	future.cancel(mayInterrupt=True)
4. isCancelled()	判断任务是否已取消	if future.is_cancelled(): ...
5. isDone()	判断任务是否已完成	if future.done(): ...
6. result() 获取结果    while not future.done()