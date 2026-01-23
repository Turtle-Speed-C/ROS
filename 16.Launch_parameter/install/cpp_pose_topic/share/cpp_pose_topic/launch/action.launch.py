import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory


# get_package_share_directory：获取功能包的安装共享路径
def generate_launch_description():
    # 利用IncludeLaunchDescriptiion动作包含其他launch文件
    # PythonLaunchDescriptionSource:指定python格式的launch文件的地址
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            # [get_package_share_directory("turtlesim"), "launch", "multisim.launch.py"]
            # 修正：用os.path.join拼接路径片段，生成完整合法路径字符串
            os.path.join(
                get_package_share_directory("turtlesim"),
                "launch",
                "multisim.launch.py"
            )
        )
    )

    # 利用ExecuteProcess动作执行命令行
    # ExecuteProcess: 执行系统命令
    # cmd 参数: 相当于在终端执行：ros2 service call /turtlesim1/spawn turtlesim/srv/Spawn "{x: 1, y: 1}"
    action_executeprpcess = launch.actions.ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/turtlesim1/spawn",
            "turtlesim/srv/Spawn",
            "{x:1,y:1}",
        ]
    )

    # LogInfo: 在终端输出日志信息
    action_log_info = launch.actions.LogInfo(msg="使用launch来调用服务生成海龟")

    # TimerAction: 延迟执行动作
    # GroupAction: 将多个动作组合成一个逻辑组
    action_group = launch.actions.GroupAction(
        [
            launch.actions.TimerAction(period=2.0, actions=[action_log_info]),
            launch.actions.TimerAction(period=3.0, actions=[action_executeprpcess]),
        ]
    )

    # 创建并返回启动描述
    launch_description = launch.LaunchDescription([action_include_launch, action_group])

    return launch_description