import launch 
import launch_ros

def generate_launch_description():
    action_node_turtlesim_node = launch_ros.actions.Node(
        package = 'turtlesim',
        executable = 'turtlesim_node',
        output = 'log'
    )

    action_node_turtle_control_v2 = launch_ros.actions.Node(
        package = 'cpp_pose_topic',
        executable = 'turtle_control_v2',
        output = 'log'
    )

    action_node_turtle_param_client = launch_ros.actions.Node(
        package = 'cpp_pose_topic',
        executable = 'turtle_param_client',
        output = 'log'
    )

    # 合成启动描述并返回
    launch_description = launch.LaunchDescription([
        action_node_turtlesim_node,
        action_node_turtle_control_v2,
        action_node_turtle_param_client
    ])

    return launch_description