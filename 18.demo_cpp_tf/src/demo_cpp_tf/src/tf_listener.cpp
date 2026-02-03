#include <memory>
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"             //提供 tf2::Quaternion类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp" //提供消息类型转换函数
#include "tf2_ros/transform_broadcaster.h"         //提供坐标广播器类
#include "tf2/utils.h"                             //提供tf2::getEulerYPR函数
#include "tf2_ros/buffer.h"                        //提供TF缓冲类Buffer
#include "tf2_ros/transform_listener.h"            //提供坐标监听器类
#include <chrono>                                  //引入时间相关头文件
using namespace std::chrono_literals;

class TFListener : public rclcpp::Node
{
public:
    TFListener() : Node("tf_listener")
    {
        buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
        listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_, this);
        timer_ = this->create_wall_timer(5s, std::bind(&TFListener::getTransform, this));
    }

    void getTransform()
    {
        // 要查询的父坐标系和子坐标系（根据你的实际场景修改，比如base_link→laser）
        std::string parent_frame = "base_link";
        std::string child_frame = "target_point";

        try
        {
            // 核心：查询父坐标系到子坐标系的**最新**变换数据
            // tf2::TimePointZero 表示取最新的TF数据，无需指定时间戳
            geometry_msgs::msg::TransformStamped transform_stamped_ =
                buffer_->lookupTransform(parent_frame, child_frame, tf2::TimePointZero);

            // 1. 获取平移信息（x/y/z，单位：米）
            double x = transform_stamped_.transform.translation.x;
            double y = transform_stamped_.transform.translation.y;
            double z = transform_stamped_.transform.translation.z;

            // 2. 获取四元数旋转信息，转成欧拉角（yaw/pitch/roll，单位：弧度）
            // 步骤：ROS2四元数消息 → tf2四元数类 → 调用tf2::getEulerYPR转欧拉角
            tf2::Quaternion q;
            // 详细版：将变换消息中的ROS2四元数消息（geometry_msgs::msg::Quaternion）转换为tf2库的四元数类对象
            tf2::fromMsg(transform_stamped_.transform.rotation, q); 
            double roll, pitch, yaw;
            tf2::getEulerYPR(q, roll, pitch, yaw); // 四元数转欧拉角（顺序：滚转/俯仰/偏航）

            // 3. 打印查询结果（ROS2标准日志，在终端能看到）
            RCLCPP_INFO(this->get_logger(), "成功查询 %s → %s 的变换：", parent_frame.c_str(), child_frame.c_str());
            RCLCPP_INFO(this->get_logger(), "平移：x=%.2f m, y=%.2f m, z=%.2f m", x, y, z);
            RCLCPP_INFO(this->get_logger(), "欧拉角：roll=%.2f rad, pitch=%.2f rad, yaw=%.2f rad", roll, pitch, yaw);
        }
        catch (const tf2::TransformException &ex)
        {
            // 捕获TF查询失败的异常（必加！否则查询失败会导致节点崩溃）
            // 常见失败原因：坐标系不存在、TF数据过期、没有对应的变换关系
            RCLCPP_WARN(this->get_logger(), "查询TF变换失败：%s", ex.what());
        }
    }

private:
    std::shared_ptr<tf2_ros::Buffer> buffer_;
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<TFListener>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}