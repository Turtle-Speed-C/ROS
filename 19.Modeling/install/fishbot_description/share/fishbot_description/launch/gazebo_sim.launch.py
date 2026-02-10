import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

# 新增：导入事件处理器（虽然launch已包含，但显式导入更清晰）
from launch.event_handlers import OnProcessExit
from launch.actions import ExecuteProcess, RegisterEventHandler


def generate_launch_description():
    # 获取默认路径
    robot_name_in_model = "fishbot"
    urdf_tutorial_path = get_package_share_directory("fishbot_description")

    default_model_path = os.path.join(
        urdf_tutorial_path, "urdf", "fishbot", "fish.urdf.xacro"
    )
    default_world_path = os.path.join(urdf_tutorial_path, "world", "custom_room.world")

    action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
        name="model",
        default_value=str(default_model_path),
        description="URDF 的绝对路径",
    )

    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(
            ["xacro ", launch.substitutions.LaunchConfiguration("model")]
        ),
        value_type=str,
    )

    robot_state_publisher_node = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        output="screen",
    )

    # 包含Gazebo官方的launch文件（启动Gazebo仿真器）
    launch_gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                get_package_share_directory("gazebo_ros"),
                "/launch",
                "/gazebo.launch.py",
            ]
        ),
        launch_arguments=[("world", default_world_path), ("verbose", "true")],
    )

    # 启动spawn_entity.py节点（加载机器人到Gazebo）
    spawn_entity_node = launch_ros.actions.Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic",
            "/robot_description",
            "-entity",
            robot_name_in_model,
            "-R",
            "0",
            "-P",
            "0",
            "-Y",
            "0",
            "-x",
            "0.5",
            "-y",
            "0.5",
            "-z",
            "0.0",
        ],
        output="screen",  # 新增：输出日志，方便排查
    )

    # 新增1：定义加载并激活关节状态控制器的命令
    load_joint_state_controller = ExecuteProcess(
        cmd=[
            "ros2", "control", "load_controller", 
            "--set-state", "active", 
            "fishbot_joint_state_broadcaster"
        ],
        output="screen",  # 输出命令执行日志
        shell=True  # 关键：启用shell，否则可能找不到ros2命令
    )

    # 新增2：注册事件处理器——spawn_entity_node结束后执行控制器加载
    load_controller_event = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity_node,  # 监听的目标进程
            on_exit=[load_joint_state_controller]  # 进程结束后执行的动作
        )
    )

    # 组装所有launch组件（原有组件 + 事件处理器）
    return launch.LaunchDescription(
        [
            action_declare_arg_model_path,
            robot_state_publisher_node,
            launch_gazebo,
            spawn_entity_node,
            load_controller_event,  # 新增：添加事件处理器
        ]
    )