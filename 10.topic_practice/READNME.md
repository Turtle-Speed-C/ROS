这个工程中，需要：
    1.获取系统状态（python）
    2.显示界面（QT）
    3.把系统消息当作话题发布出来

一.自定义消息接口
    需要有builtin_interfaces和rosidl_default_generators两个包。
    builtin_interfaces：
        是一个ROS2中已有的消息接口功能包，可以使用时间接口Time，表示记录时间。
    rosidl_default_generators:
        用于将自定义的消息文件转化为C++、python源码模块



这里这段内容其实就干了三件事：**创建接口包、写消息文件、让 CMake/ROS2 知道它的存在**。你学 ROS2，要把这套流程背成肌肉记忆——以后写自定义 msg、srv、action 都一样的套路。

---

## **【重点总结｜自定义 ROS2 消息接口的全过程】**

### **1. 创建接口功能包（ament_cmake + rosidl_default_generators）**

核心命令：

```
ros2 pkg create status_interfaces \
  --build-type ament_cmake \
  --dependencies rosidl_default_generators builtin_interfaces
```

要点：

* **消息接口包必须用 ament_cmake**
* builtin_interfaces 用来提供 **Time** 类型
* rosidl_default_generators 用来生成 C++/Python 接口代码

---

### **2. 创建 msg 文件**

放在：`status_interfaces/msg/SystemStatus.msg`

内容格式：

* 类型 + 字段名
* `#` 为注释
* 类型可以是 builtin_interfaces/Time 或 ROS2 内置基本类型

你这个 msg 主要字段：

```
builtin_interfaces/Time stamp
string host_name
float32 cpu_percent
float32 memory_percent
float32 memory_total
float32 memory_available
float64 net_sent
float64 net_recv
```

核心记忆点：**ROS2 的 msg 类型必须首字母大写，文件放 msg/ 下**

---

### **3. 修改 CMakeLists.txt —— 注册消息接口**

关键部分：

```
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/SystemStatus.msg"
  DEPENDENCIES builtin_interfaces
)
```

你必须记住：

* **使用了 Time → CMake 中一定要 find builtin_interfaces**
* **所有 msg、srv、action 都必须写在 rosidl_generate_interfaces 中**

---

### **4. 修改 package.xml**

必须声明这是一个接口包：

```
<member_of_group>rosidl_interface_packages</member_of_group>
```

这个声明能让 ROS2 在构建时对它做特殊处理。

---

### **5. 构建并验证接口是否生成成功**

构建后：

```
source install/setup.bash
ros2 interface show status_interfaces/msg/SystemStatus
```

检查是否生成 C++ 和 Python 文件：

* C++：`install/status_interfaces/include/`
* Python：`install/status_interfaces/local/lib/python3.x/dist-packages/`

---

## **一句话总结**

你需要记住的只有一条：
**自定义消息 = 创建接口包 + 写 msg + 在 CMakeLists 注册 + package.xml 声明接口包 + 构建后查看是否生成成功。**

以后你写服务 srv、动作 action，也是这一条公式，只不过目录和生成宏稍有不同。

---

如果你愿意，我可以帮你做一个 **“ROS2 自定义接口流程模板”**，你以后只需要复制、改名、直接用，不用再查这堆步骤了。
