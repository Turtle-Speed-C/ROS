cmake_minimum_required(VERSION 3.8)
project(ros2_cpp)
add_executable(ros2_node_cpp first.cpp)

find_package(rclcpp REQUIRED) #查找头文件和库文件
#find_package 是 CMake 的核心命令之一，用于查找并加载外部依赖包（这里是rclcpp）的配置信息。
#REQUIRED 是一个选项，表示rclcpp是项目必须的依赖：如果找不到该包，CMake 配置过程会直接失败并报错（而不是警告），确保项目不会在缺少核心依赖的情况下继续构建。

message(STATUS ${rclcpp_INCLUDE_DIRS})  #头文件
#message 是 CMake 的信息输出命令，用于在配置阶段向控制台打印信息。
#STATUS 是输出级别，表示这是一条状态信息（通常会在信息前自动添加-- 前缀，与其他级别区分）。
#${rclcpp_INCLUDE_DIRS} 是一个 CMake 变量，在find_package(rclcpp)成功后自动定义，存储了rclcpp库的头文件（.h）所在的目录路径。
#因此，这句的作用是在 CMake 配置时，打印出rclcpp头文件的具体目录，方便开发者验证是否正确找到依赖的头文件路径（例如排查 “头文件找不到” 的问题）。

message(STATUS ${rclcpp_LIBRARIES}) #库文件（以.so结尾）

target_include_directories(ros2_node_cpp PUBLIC ${rclcpp_INCLUDE_DIRS}) #头文件包含
target_link_libraries(ros2_node_cpp ${rclcpp_LIBRARIES})    #库文件包含