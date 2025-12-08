#include <cstdlib> //C++对C标准库<stdlib.h>的封装
#include <ctime>
#include "rclcpp/rclcpp.hpp"
#include "turtle_control_interfaces/srv/patrol.hpp"
#include <chrono>

using namespace std::chrono_literals;
using patrol = turtle_control_interfaces::srv::Patrol;

class PatrolClient : public rclcpp::Node
{
public:
    PatrolClient() : Node("patrol_client")
    {
        patrol_client_ = this->create_client<patrol>("patrol");
        timer_ = this->create_wall_timer(10s, std::bind(&PatrolClient::timer_callback, this));
        srand(time(NULL)); // 初始化随机数种子，使用当前时间作为种子
    }

    void timer_callback()
    {
        // 1.等待服务端上线
        while (!patrol_client_->wait_for_service(std::chrono::seconds(1)))
        {
            // 等待的时候还要做点别的事
            if (!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(), "等待服务的过程被打断");
                return;
            }
            RCLCPP_ERROR(this->get_logger(), "等待服务上线");
        }

        // 2.构造请求的对象
        auto request = std::make_shared<patrol::Request>();
        request->target_x = rand() % 11;
        request->target_y = rand() % 11;
        RCLCPP_INFO(this->get_logger(), " 请 求 巡 逻：(%f,%f)", request->target_x, request->target_y);

        // 3.发送异步请求，然后等待返回，返回时调用回调函数
        patrol_client_->async_send_request(
            request,
            [&](rclcpp::Client<patrol>::SharedFuture result_future) -> void
            {
                auto response = result_future.get();
                if (response->result == patrol::Response::SUCCESS)
                {
                    RCLCPP_INFO(this->get_logger(), " 目标点处理成功 ");
                }
                else if (response->result == patrol::Response::FAIL)
                {
                    RCLCPP_INFO(this->get_logger(), " 目标点处理失败 ");
                }
            });
    }

private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Client<patrol>::SharedPtr patrol_client_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PatrolClient>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}