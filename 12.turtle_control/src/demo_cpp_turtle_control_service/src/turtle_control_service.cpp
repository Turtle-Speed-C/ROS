#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include "turtle_control_interfaces/srv/patrol.hpp"

using namespace std::chrono_literals;
using Patrol = turtle_control_interfaces::srv::Patrol;
// 为 ROS 2 自定义服务类型 turtle_control_interfaces::srv::Patrol 创建简短的类型别名 Patrol
// 等价于传统的 typedef turtle_control_interfaces::srv::Patrol Patrol;，但更易读

class TurtleControl : public rclcpp ::Node
{
public:
    TurtleControl(const std::string &node_name) : Node(node_name)
    {
        // 发布者和订阅者
        velocity_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel", 10);

        pose_subscribers_ = this->create_subscription<turtlesim::msg::Pose>(
            "turtle1/pose",
            10,
            std::bind(&TurtleControl::poseCallback, this, std::placeholders::_1));
        // bind函数：
        // 第一步：绑定成员函数 poseCallback 到 this 指向的 TurtleControl 实例；
        // 第二步：用 _1 占位符 “预留位置”：告诉 bind“这个函数需要一个参数，等调用的时候再传进来”；
        // 第三步：生成一个「无上下文依赖的可调用对象」—— ROS 2 订阅器可以直接调用这个对象，不需要关心它背后是类的成员函数。

        patrol_server_ = this->create_service<Patrol>(
            // <Patrol>   这个服务可以处理的请求类型
            "patrol", // 服务端的名称
            [this](const std::shared_ptr<Patrol::Request> request, const std::shared_ptr<Patrol::Response> response)
            {
                if (request->target_x > 0 && request->target_y > 0 && request->target_x < 11 && request->target_y < 11)
                {
                    target_x_ = request->target_x;
                    target_y_ = request->target_y;

                    response->result = Patrol::Response::SUCCESS;
                    RCLCPP_INFO(this->get_logger(), "新目标点已设置: (%.2f, %.2f)", target_x_, target_y_);
                }
                else
                {
                    response->result = Patrol::Response::FAIL;
                    RCLCPP_WARN(this->get_logger(), "目标点超出范围: (%.2f, %.2f)", request->target_x, request->target_y);
                }
            });
    }

public:
    void poseCallback(const turtlesim::msg::Pose::SharedPtr pose)
    // turtlesim::msg::Pose	消息类型    ::SharedPtr 智能指针类型    const 不能修改消息  pose 参数名
    // 传递过来的pose是系统直接传递的，
    {
        auto message = geometry_msgs::msg::Twist();

        double current_x_ = pose->x;
        double current_y_ = pose->y;
        RCLCPP_DEBUG(this->get_logger(), "当前的位置是：x=%f，y=%f", current_x_, current_y_);

        double distance = std::sqrt( // sqrt是负数平方根
            (target_x_ - current_x_) * (target_x_ - current_x_) + (target_y_ - current_y_) * (target_y_ - current_y_));

        double angle = atan2( // 从 x 轴正方向逆时针旋转到「点 (x, y) 与原点连线」的角度，数学上等价于 arctan(y/x)
                           target_y_ - current_y_, target_x_ - current_x_) -
                       pose->theta;

        while (angle > M_PI)
            angle -= 2 * M_PI;
        while (angle < -M_PI)
            angle += 2 * M_PI;

        if (distance > 0.1)
        {
            if (std::fabs(angle) > 0.2)
            {
                // 转向：角速度与角度误差成正比，带方向
                message.angular.z = 2.0 * angle; // 建议加系数并保留符号
            }
            else
            {
                message.linear.x = k_ * distance;
            }
        }

        // 限制线速度最大值
        if (message.linear.x > max_linear_speed_)
        {
            message.linear.x = max_linear_speed_;
        }
        // 也可以限制角速度
        if (message.angular.z > max_angular_speed_)
        {
            message.angular.z = max_angular_speed_;
        }
        else if (message.angular.z < -max_angular_speed_)
        {
            message.angular.z = -max_angular_speed_;
        }

        velocity_publisher_->publish(message);
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_publisher_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_subscribers_;
    rclcpp::Service<Patrol>::SharedPtr patrol_server_;

    double target_x_{3.0};
    double target_y_{4.0};
    const double k_{1.0};
    const double max_linear_speed_{3.0};
    const double max_angular_speed_{3.0};
};

int main(int argc,char** argv){
    rclcpp::init(argc,argv);
    auto node=std::make_shared<TurtleControl>("control_turtle_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}