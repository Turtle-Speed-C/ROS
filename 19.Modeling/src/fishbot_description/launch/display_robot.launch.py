import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # 获取默认路径
    urdf_tutorial_path = get_package_share_directory("fishbot_description")
    # 传入功能包名fishbot_description，返回该功能包在当前系统中的share目录绝对路径（比如/home/xxx/ros2_ws/install/fishbot_description/share/fishbot_description/）；
    default_model_path = urdf_tutorial_path + "/urdf/first_robot.urdf"
    default_rviz_config_path = urdf_tutorial_path + '/config/rviz/display_model.rviz'

    # DeclareLaunchArgument:声明参数
    # 声明了一个名为model的参数，默认值是上面拼接的first_robot.urdf路径
    # 用户启动时可通过命令行覆盖默认值，比如：ros2 launch fishbot_description xxx.launch.py --ros-args -p model:=/home/xxx/my_robot.urdf
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name="model",
        default_value=str(default_model_path),
        description="URDF 的绝对路径",
    )

    # ParameterValue：复杂参数值封装
    # 获取文件内容生成新的参数
    # LaunchConfiguration('model')：获取前面声明的model参数的值（URDF 文件绝对路径）；
    # Command(['cat ', 路径])：执行系统 shell 命令cat，cat 路径的作用是读取文件的文本内容，这是 ROS2 中加载文件内容的标准写法；
    # ParameterValue(内容, value_type=str)：将cat命令读取的 URDF 文本内容，封装为字符串类型的 ROS2 参数值（因为 URDF 是文本，必须指定str类型）；
    # 最终赋值给robot_description：这个变量就是后续要传给节点的「机器人模型内容参数」。
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(
            ['cat ', launch.substitutions.LaunchConfiguration("model")]
        ),
        value_type=str,
    )

    # 状态发布节点
    # 包名package：节点所在的 ROS2 功能包（robot_state_publisher是 ROS2 官方提供的功能包，需提前安装）；
    # 可执行文件名executable：节点的可执行文件（和包名同名，是官方默认命名）；
    # parameters=[{...}]：给节点传入参数，这里把前面构建的robot_description（URDF 内容）传给节点；
    # 节点的核心功能：解析 URDF 中的连杆（link）和关节（joint）关系，发布机器人的 TF/TF2 坐标变换（机器人各个部件的相对位置），是 RViz2 可视化机器人的基础（没有 TF 变换，RViz2 找不到机器人的坐标）。
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
    )

    # 关节状态发布节点
    joint_state_publisher_node = launch_ros.actions.Node(
    package='joint_state_publisher',
    executable='joint_state_publisher',
    )

    # RViz节点
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d',default_rviz_config_path]
    )

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])