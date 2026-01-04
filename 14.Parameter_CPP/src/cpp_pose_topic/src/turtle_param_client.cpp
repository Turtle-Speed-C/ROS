#include "rclcpp/rclcpp.hpp"
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"
#include <chrono>

using namespace std::chrono_literals;
using SetP=rcl_interfaces::srv::SetParameters;

class TurtleParamClient : public rclcpp::Node
{
public:
    TurtleParamClient() : Node("turtle_control_client")
    {
        RCLCPP_INFO(this->get_logger(),"海龟控制客户端已启动");
    }

    //通用的参数设置方法
    std::shared_ptr<SetP::Response>call_set_parameters(rcl_interfaces::msg::Parameter &parameter)
    {
        // 1.创建客户端等待服务上线
        auto param_client = this->create_client<SetP>("/control_turtle_node/set_parameters");

        while(!param_client->wait_for_service(std::chrono::seconds(1)))
        {
            if(!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(),"等待服务的过程中被打断");
                return nullptr;
            }
            RCLCPP_INFO(this->get_logger(),"等待参数设置服务端上线中");
        }

        // 2.创建请求对象（修正：std::make_shared）
        auto request = std::make_shared<SetP::Request>();
        request->parameters.push_back(parameter);

        //3. 异步调用、等待并返回响应结果（修正：笔误“调试”改为“调用”）
        auto future = param_client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
        auto response=future.get();
        return response;
    }

    //更新参数k（控制速度）
    void update_param_k(double k)
    {
        //1.创建一个参数对象
        auto param = rcl_interfaces::msg::Parameter();
        param.name = "k";

        //2.创建参数值对象并赋值
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type=rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;
        param.value=param_value;

        //3.请求更新参数并处理（修正：逻辑颠倒问题）
        auto response = call_set_parameters(param);
        if(response == nullptr)
        {
            RCLCPP_WARN(this->get_logger(),"k参数修改请求失败（服务调用异常）");
            return;
        }
        else
        {
            for(auto result : response->results)
            {
                if(result.successful)
                {
                    RCLCPP_INFO(this->get_logger(),"参数 k 已修改为：%f", k);
                }
                else
                {
                    RCLCPP_WARN(this->get_logger(),"参数k失败原因：%s",result.reason.c_str());
                }
            }
        }
    }

    //更新参数max_speed（最大速度限制）（修正：doouble改为double）
    void update_param_max_speed(double max_speed)
    {
        //1.创建一个参数对象（修正：max+speed改为max_speed）
        auto param = rcl_interfaces::msg::Parameter();
        param.name="max_speed";

        //2.创建参数值对象并赋值
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type=rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = max_speed;
        param.value=param_value;

        //3.请求更新参数并处理（修正：逻辑颠倒+日志匹配问题）
        auto response = call_set_parameters(param);
        if(response == nullptr)
        {
            RCLCPP_WARN(this->get_logger(),"max_speed参数修改请求失败（服务调用异常）");
            return;
        }
        else
        {
            for(auto result : response->results)
            {
                if(result.successful)
                {
                    // 修正：日志参数名匹配max_speed
                    RCLCPP_INFO(this->get_logger(),"参数 max_speed 已修改为：%f", max_speed);
                }
                else
                {
                    // 修正：日志参数名匹配max_speed
                    RCLCPP_WARN(this->get_logger(),"参数max_speed失败原因：%s",result.reason.c_str());
                }
            }
        }
    }

    //同时更新两个参数
    void update_both_params(double k,double max_speed)
    {
        RCLCPP_INFO(this->get_logger(),"开始更新参数k=%f，max_speed=%f",k,max_speed);
        update_param_k(k);
        // 增加短暂延时，避免两个服务请求同时发送导致冲突
        std::this_thread::sleep_for(500ms);
        update_param_max_speed(max_speed);
    }
};

// 补全：main函数（ROS 2 C++标准流程）
int main(int argc,char **argv)
{
    rclcpp::init(argc,argv);
    // 创建客户端节点对象
    auto client_node=std::make_shared<TurtleParamClient>();
    // 調用參數更新方法
    client_node->update_both_params(1.8,4.0);
    // 单独更新示例（可选注释）
    // client_node->update_param_k(2.0);
    // client_node->update_param_max_speed(3.5);

    //消毀節點
    rclcpp::shutdown();
    
}