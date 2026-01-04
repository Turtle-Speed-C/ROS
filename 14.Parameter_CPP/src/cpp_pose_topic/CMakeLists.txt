cmake_minimum_required(VERSION 3.8)
project(cpp_pose_topic)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)

include_directories(include)

add_executable(turtle_circle src/turtle_circle.cpp)
add_executable(turtle_control src/turtle_control.cpp)
add_executable(turtle_control_v2 src/turtle_control_v2.cpp)
# 这里的turtle_control是可执行文件，在后面的install会把turtle_control放入到install/lib下面
# 但是节点名一定是在cpp的node_name‘
add_executable(turtle_param_client src/turtle_param_client.cpp)


# 链接依赖
ament_target_dependencies(turtle_circle 
  rclcpp 
  geometry_msgs 
  turtlesim
) 

ament_target_dependencies(turtle_control 
  rclcpp 
  geometry_msgs 
  turtlesim
) 

ament_target_dependencies(turtle_control_v2 
  rclcpp 
  geometry_msgs 
  turtlesim
) 

ament_target_dependencies(turtle_param_client 
  rclcpp 
  geometry_msgs 
  turtlesim
) 

# 安装
install(TARGETS
  turtle_circle turtle_control turtle_control_v2 turtle_param_client
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
