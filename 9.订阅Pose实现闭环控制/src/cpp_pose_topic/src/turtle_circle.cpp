#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"

using namespace std::chrono_literals;   //时间相关的命名空间

class TurtleCircle : public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    // rclcpp::Publisher<geometry_msgs::msg::Twist> publisher_; // 发布者智能指针
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; // 发布者智能指针

public:
    explicit TurtleCircle(const std::string &node_name) : Node(node_name)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        timer_ = this->create_wall_timer(1000ms, std::bind(&TurtleCircle::timer_callback, this));
    }

    void timer_callback()
    {
        auto msg = geometry_msgs::msg::Twist();
        msg.linear.x = 3;
        msg.angular.z = 0.5;
        publisher_->publish(msg);
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleCircle>("turtle_circle");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

/*
在main中的argc和argv：
示例 1：无参数运行
bash./turtle_circle

argc = 1
argv[0] = "./turtle_circle"

示例 2：带参数运行
bash./turtle_circle --ros-args -r __node:=my_turtle -p speed:=2.0

argc = 6
argv[0] = "./turtle_circle"
argv[1] = "--ros-args"
argv[2] = "-r"
argv[3] = "__node:=my_turtle"
argv[4] = "-p"
argv[5] = "speed:=2.0"
*/

/*
explicit 关键字用于修饰构造函数，表示该构造函数是显式的，不能被用于隐式转换。'
如果不是显示构造，可以：TurtleCircle t="name";
因为在一个构造函数只有一个参数的时候。，可以直接传递一个参数。 这种构造方式称为隐式转换。

我来为你详细讲解这几个ROS 2中的重要函数和消息类型：

## 1. `create_publisher`

**作用：**
创建一个发布者（Publisher），用于向指定的话题（Topic）发布消息。

**函数签名：**
```cpp
template<typename MessageT>
typename rclcpp::Publisher<MessageT>::SharedPtr
create_publisher(
    const std::string & topic_name,
    const rclcpp::QoS & qos
)
```

**参数：**
- `topic_name`：话题名称（字符串），例如 "cmd_vel"
- `qos`：服务质量（QoS）设置，通常传入队列大小，如 `10` 表示消息队列深度为10

**返回值：**
返回一个指向 `Publisher` 对象的智能指针（`SharedPtr`），用于后续发布消息。

**示例：**
```cpp
publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
```

---

## 2. `create_wall_timer`

**作用：**
创建一个定时器，按照指定的时间间隔周期性地调用回调函数。

**函数签名：**
```cpp
template<typename DurationT, typename CallbackT>
typename rclcpp::WallTimer<CallbackT>::SharedPtr
create_wall_timer(
    std::chrono::duration<DurationT> period,
    CallbackT callback
)
```

**参数：**
- `period`：定时器周期，使用 `std::chrono` 时间类型，例如 `500ms` 表示每500毫秒触发一次
- `callback`：回调函数，定时器触发时执行的函数

**返回值：**
返回一个指向 `WallTimer` 对象的智能指针，定时器会自动运行。

**示例：**
```cpp
timer_ = this->create_wall_timer(
    std::chrono::milliseconds(500),
    std::bind(&MyNode::timer_callback, this)
);
```

---

## 3. `geometry_msgs::msg::Twist()`

**作用：**
这是一个消息类型的构造函数，创建一个 `Twist` 消息对象，用于表示线速度和角速度。

**消息结构：**
```cpp
geometry_msgs::msg::Twist {
    geometry_msgs::msg::Vector3 linear;   // 线速度 (x, y, z)
    geometry_msgs::msg::Vector3 angular;  // 角速度 (x, y, z)
}
```

**参数：**
无参数（默认构造函数），所有字段初始化为0。

**返回值：**
返回一个 `Twist` 消息对象。

**示例：**
```cpp
auto message = geometry_msgs::msg::Twist();
message.linear.x = 2.0;   // 设置前进速度
message.angular.z = 1.8;  // 设置旋转速度
```

---

## 4. `publish`

**作用：**
通过发布者将消息发布到对应的话题上。

**函数签名：**
```cpp
void publish(const MessageT & message)
```

**参数：**
- `message`：要发布的消息对象（引用类型）

**返回值：**
无返回值（`void`）。

**示例：**
```cpp
auto message = geometry_msgs::msg::Twist();
message.linear.x = 2.0;
publisher_->publish(message);
```

---

## 完整使用示例

```cpp
class VelocityPublisher : public rclcpp::Node {
public:
    VelocityPublisher() : Node("velocity_publisher") {
        // 创建发布者
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
        
        // 创建定时器，每500ms执行一次
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&VelocityPublisher::timer_callback, this)
        );
    }

private:
    void timer_callback() {
        // 创建消息
        auto message = geometry_msgs::msg::Twist();
        message.linear.x = 2.0;
        message.angular.z = 1.8;
        
        // 发布消息
        publisher_->publish(message);
    }
    
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};
```

这四个函数/类型共同构成了ROS 2中周期性发布消息的基本模式。
*/