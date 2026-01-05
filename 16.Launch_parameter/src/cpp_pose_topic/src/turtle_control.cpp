#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include <cmath>

using namespace std::chrono_literals;

class TurtleControl : public rclcpp::Node
{
public:
    TurtleControl(const std::string &node_name) : Node(node_name)
    {
        velocity_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel", 10);
        pose_subscription_ = this->create_subscription<turtlesim::msg::Pose>("turtle1/pose", 10, std::bind(&TurtleControl::poseCallback, this, std::placeholders::_1));
        // k 和 max_speed 是 ROS 2 节点的参数名（字符串标识）；
        // k_ 和 max_speed_ 是 C++ 类中用来存储这些参数值的成员变量。
        this->declare_parameter("k", 1.0);         // 参数名用"k"
        this->declare_parameter("max_speed", 3.0); // 参数名用"max_speed"
        this->get_parameter("k", k_);
        this->get_parameter("max_speed", max_speed_);
    }

public:
    void poseCallback(const turtlesim::msg::Pose::SharedPtr pose)
    {
        auto message = geometry_msgs::msg::Twist();
        // 1.记录当前的位置：
        double current_x_ = pose->x;
        double current_y_ = pose->y;
        RCLCPP_INFO(this->get_logger(), "当前位置：x=%f，y=%f", current_x_, current_y_);

        // 2.记录与目标点之间的距离，以及当前海龟的朝向的角速度
        double distance = std::sqrt((target_x_ - current_x_) * (target_x_ - current_x_) + (target_y_ - current_y_) * (target_y_ - current_y_));
        double angle = atan2(target_y_ - current_y_, target_x_ - current_x_) - pose->theta;

        if (angle > M_PI)
        {
            angle -= 2 * M_PI;
        }
        else if (angle < -M_PI)
        {
            angle += 2 * M_PI;
        }

        // 3. 控制策略：距离大于0.1继续运动，角度差大于0.2则原地旋转，否则直行
        if (distance > 0.05)
        {
            if (fabs(angle) > 0.2)
            {
                message.angular.z = 0.5 * fabs(angle);
            }
            else
            {
                message.linear.x = k_ * distance;
            }
        }

        // 4.限制最大值并发布消息
        if (message.linear.x > max_speed_)
        {
            message.linear.x = max_speed_;
        }

        velocity_publisher_->publish(message);
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_publisher_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_subscription_;
    double target_x_{3.0};
    double target_y_{4.0};
    double k_{1.0};
    double max_speed_{3.0};
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleControl>("control_turtle_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

/*
pose_subscription_ = this->create_subscription<turtlesim::msg::Pose>(
    "/turtle1/pose",  // 订阅的话题名称
    10,               // 队列大小
    std::bind(&TurtleController::on_pose_received_, this, std::placeholders::_1)
    //                                                     ^^^^^^^^^^^^^^^^^^^
    //                                                     占位符：表示"将来会有一个参数传进来"
);
```

### 2. ROS 2 系统的工作流程
```
其他节点发布消息到 /turtle1/pose
            ↓
ROS 2 中间件接收到消息
            ↓
检查谁订阅了这个话题
            ↓
找到你的订阅者 pose_subscription_
            ↓
调用绑定的回调函数 on_pose_received_
            ↓
把接收到的消息作为参数传递给回调函数
            ↓
void on_pose_received_(const turtlesim::msg::Pose::SharedPtr pose)
                                                              ^^^^
                                                              这就是传进来的消息
*/