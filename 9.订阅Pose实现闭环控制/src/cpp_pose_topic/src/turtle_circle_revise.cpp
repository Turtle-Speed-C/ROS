#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"

using namespace std::chrono_literals;

class turtle_circle : public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;

public:
    explicit turtle_circle(const std::string &node_name) : Node(node_name)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        timer_ = this->create_wall_timer(1000ms, [this]()
                                         { this->time_callback(); });
    }

    void time_callback()
    {
        auto msg_ = geometry_msgs::msg::Twist();
        msg_.linear.x = 1.0;
        msg_.angular.z = 2.0;
        publisher_->publish(msg_);
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc,argv);
    auto node=std::make_shared<turtle_circle>("TurtleCircle");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}