#include <memory>
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"             //提供 tf2::Quaternion类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp" //提供消息类型转换函数
#include "tf2_ros/transform_broadcaster.h"         //提供坐标广播器类

using namespace std::chrono_literals;

class DynamicTFbroadcaster : public rclcpp::Node
{
public:
    DynamicTFbroadcaster() : Node("dynamic_tf_broadcaster")
    {
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
        timer_ = create_wall_timer(10ms, std::bind(&DynamicTFbroadcaster::publishTransform,this));
        // create_wall_timer:
        // 在内存中创建一个真正的 ROS2 定时器对象（可以理解为一个 “自动倒计时的小闹钟”），同时这个函数会返回这个小闹钟在内存中的地址。
        // std::bind:
        // &DynamicTFBroadcaster::publishTransform：取回调函数的地址（告诉定时器 “要调用的函数在哪里”）；
        // this：表示 “调用当前这个DynamicTFBroadcaster对象的publishTransform函数”—— 因为你的节点可能有多个实例，this能精准定位到当前对象。
        // 你的this出现在DynamicTFbroadcaster类的构造函数里，所以它的原生类型是：DynamicTFbroadcaster*（自定义子类的裸指针）。
        // 子类的指针 / 引用可以自动、隐式地转换成父类的指针 / 引用，且这个转换是安全的。
        // 所以this能被当作rclcpp::Node*。
    }

    void publishTransform()
    {
        geometry_msgs::msg::TransformStamped Transform;
        Transform.header.stamp = this->get_clock()->now();
        Transform.header.stamp = this->get_clock()->now();
        Transform.header.frame_id = "map";
        Transform.child_frame_id = "target_point";
        Transform.transform.translation.x = 5.0;
        Transform.transform.translation.y = 3.0;
        Transform.transform.translation.z = 0.0;
        tf2::Quaternion quat;
        quat.setRPY(0, 0, 60 * M_PI / 180); //弧度制欧拉角转四元数
        Transform.transform.rotation = tf2::toMsg(quat);    //转成消息接口类型
        tf_broadcaster_->sendTransform(Transform);
    }

private:
    std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
    rclcpp::TimerBase::SharedPtr timer_;
    // 定时器指针就是专门用来保存「ROS2 定时器对象」内存地址的变量
    // TimerBase 是 ROS2 中所有定时器的基类，不管是壁钟定时器（create_wall_timer）还是仿真定时器（create_timer），都继承自这个基类，所以用TimerBase::SharedPtr 可以接收所有类型的定时器对象。
};

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<DynamicTFbroadcaster>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}