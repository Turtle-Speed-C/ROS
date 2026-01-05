import launch
import launch_ros


def generate_launch_description():
    # 创建参数声明 action，用于解析 launch 命令后的参数
    action_declare_arg_max_speed = launch.actions.DeclareLaunchArgument(
        "launch_max_speed", default_value="2.0"
    )

    # 启动节点，
    action_node_turtlesim_node = launch_ros.actions.Node(
        package="turtlesim",
        executable="turtlesim_node",
        output="log",
    )

    # 启动了海龟控制节点
    action_node_turtle_control_v2 = launch_ros.actions.Node(
        package="cpp_pose_topic", executable="turtle_control_v2", output="log",
        # 使用 launch 中参数 launch_max_speed 值替换节点中的 max_speed 参数值
        parameters=[
            {
                # launchConfiguration是关键，他的作用是获取上下文的launch_max_speed，用来代替turtle_control_v2可执行文件的max_speed
                "max_speed": launch.substitutions.launchConfiguration(
                    "launch_max_speed", default="2.0"
                )
            }
        ],
    )

    action_node_turtle_param_client = launch_ros.actions.Node(
        package="cpp_pose_topic", executable="turtle_param_client", output="log"
    )

    # 合成启动描述并返回
    launch_description = launch.LaunchDescription(
        [
            action_declare_arg_max_speed,
            action_node_turtlesim_node,
            action_node_turtle_control_v2,
            action_node_turtle_param_client,
        ]
    )

    return launch_description

"""
# 使用默认值 2.0
ros2 launch your_package your_launch.py

# 自定义最大速度为 5.0
ros2 launch your_package your_launch.py launch_max_speed:=5.0

"""