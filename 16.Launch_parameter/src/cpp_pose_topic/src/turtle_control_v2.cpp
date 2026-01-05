#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include <cmath>
#include "rcl_interfaces/msg/set_parameters_result.hpp"
// 这是ROS 2的标准头文件，定义了"参数设置结果"的消息类型

// SetParametersResult 是 ROS 2 中 rcl_interfaces 包定义的一个结构体，用于表示参数设置操作的结果。
// struct SetParametersResult {
//   bool successful;
//   std::string reason;
// };

using namespace std::chrono_literals;
// 定义别名：把长类型名映射为短类型名
using SetParametersResult = rcl_interfaces::msg::SetParametersResult;
// 导入了rcl_interfaces::msg::SetParametersResult消息接口，用于返回参数设置结果

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

        parameters_callback_handle_ = this->add_on_set_parameters_callback
                                      // add_on_set_parameters_callback：这是ROS2提供的一个"安装遥控器"的方法
                                      // 你告诉ROS2："当有人修改我的参数时，请调用我后面写的这个函数"
                                      (
                                          [&](const std::vector<rclcpp::Parameter> &params) -> SetParametersResult
                                          // [&]：表示这个函数能直接用到你类里的变量（比如k_、max_speed_）
                                          {
                                              for (auto param : params)
                                              {
                                                  RCLCPP_INFO(this->get_logger(), "更新参数 %s 值为： %f", param.get_name().c_str(), param.as_double());
                                                  // param.get_name()：获取参数的名字，比如"k"
                                                  // param.as_double()：把参数值转成数字，比如5.0

                                                  if (param.get_name() == "k")
                                                  {
                                                      k_ = param.as_double();
                                                  }
                                                  else if (param.get_name() == "max_speed")
                                                  {
                                                      max_speed_ = param.as_double();
                                                  }
                                              }
                                              auto result = SetParametersResult();
                                              result.successful = true;
                                              return result;
                                          }

                                      );
                                      
        this->set_parameter(rclcpp::Parameter("k", 2));
        /*  rclcpp::Parameter("k", 2.0) - 创建参数对象
            this->set_parameter(...) - 调用设置参数的方法
        
            // ROS 2 内部大概是这样定义的
            class Parameter {
            public:
                Parameter(const std::string& name, double value) 
                    : name_(name), value_(value) {}
                
            private:
                std::string name_;   // 存储参数名
                double value_;       // 存储参数值
            };
        */
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

    rclcpp::Node::OnSetParametersCallbackHandle::SharedPtr parameters_callback_handle_;
    // OnSetParametersCallbackHandle是专门用于管理 “参数设置回调函数” 生命周期的
    // 赋值时（parameters_callback_handle_ = this->add_on_set_parameters_callback(...)）：拿到 “注册成功的凭证”，证明回调已生效；
    // 后续可通过它主动注销回调（比如节点析构前清理资源）
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleControl>("control_turtle_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
