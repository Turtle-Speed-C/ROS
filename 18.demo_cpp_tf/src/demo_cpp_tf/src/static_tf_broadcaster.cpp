#include <memory>
#include "geometry_msgs/msg/transform_stamped.hpp" //提供消息接口
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"             //提供 tf2::Quaternion类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp" //提供消息类型转换函数
#include "tf2_ros/static_transform_broadcaster.h"  //提供静态坐标广播器类

class StaticTFBroadcaster : public rclcpp::Node
{
public:
    StaticTFBroadcaster() : Node("tf_broadcaster_node")
    {
        // 创建静态广播发布器并发布
        // this在类的成员函数 / 构造函数里，是一个普通指针，指向当前类的实例对象；
        // 你的这个语句写在StaticTFBroadcaster的构造函数里，
        // 所以这里的this → 指向当前正在创建的 ROS2 节点对象（就是你后面main里std::make_shared<StaticTFBroadcaster>()创建的那个节点）；
        // 为什么要传this给广播器？
        // TF 广播器不是独立工作的，它需要依赖 ROS2 节点的核心资源（比如节点的时钟、通信上下文、命名空间等）才能正常发布 TF 坐标变换消息，
        // 简单说：告诉 TF 广播器 “你属于哪个节点，要跟着这个节点干活”，这是 ROS2 所有组件（发布器、订阅器、TF 广播器 / 监听器）的通用规则 —— 创建时必须绑定所属节点。
        broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);
        this->publish_tf();
    }

    void publish_tf()
    {
        geometry_msgs::msg::TransformStamped transform;
        transform.header.stamp = this->get_clock()->now();
        transform.header.frame_id = "map";
        transform.child_frame_id = "target_point";
        transform.transform.translation.x = 5.0;
        transform.transform.translation.y = 3.0;
        transform.transform.translation.z = 0.0;
        tf2::Quaternion quat;
        quat.setRPY(0, 0, 60 * M_PI / 180); //弧度制欧拉角转四元数
        transform.transform.rotation = tf2::toMsg(quat);    //转成消息接口类型
        broadcaster_->sendTransform(transform);
    }

private:
    std::shared_ptr<tf2_ros::StaticTransformBroadcaster> broadcaster_;
};

int main(int argc,char** argv){
    rclcpp::init(argc,argv);
    auto node = std::make_shared<StaticTFBroadcaster>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

/*
使用ros2 run demo_cpp_tf static_tf_broadcaster 执行文件

$ ros2 run tf2_ros tf2_echo map target_point
---
At time 0.0
- Translation: [5.000, 3.000, 0.000]
- Rotation: in Quaternion [0.000, 0.000, 0.500, 0.866]
- Rotation: in RPY （radian） [0.000, -0.000, 1.047]
- Rotation: in RPY （degree） [0.000, -0.000, 60.000]
- Matrix:
0.500 -0.866 0.000 5.000
0.866 0.500 0.000 3.000
0.000 0.000 1.000 0.000
0.000 0.000 0.000 1.000
这个命令
ros2 run <功能包名> <可执行文件/节点名> [参数1] [参数2] ...
tf2_ros：功能包名，是 ROS2 处理 ** 坐标系变换（tf2）** 的核心功能包，提供了 tf2 相关的工具、节点和底层 API；
tf2_echo：该功能包下的可执行调试工具，核心功能是「回显 / 打印」两个坐标系之间的 tf 变换数据，且会实时刷新（坐标系变换更新时，输出也会同步更新）；
*/