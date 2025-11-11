cmake_minimum_required(VERSION 3.8)
project(demo_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(cpp_node src/cpp_node.cpp)

message(STATUS ${rclcpp_INCLUDE_DIRS})  #打印头文件
message(STATUS ${rclcpp_LIBRARIES})     #打印库文件

target_include_directories(cpp_node PUBLIC ${rclcpp_INCLUDE_DIRS}) #链接头文件
target_link_libraries(cpp_node ${rclcpp_LIBRARIES})               #链接库文件
#或者使用两个结合的命令
#ament_target_dependencies(cpp_node rclcpp)

#这个命令会把cpp_node（可执行文件）拷贝到include下面的文件中。
#要在install/lib下面找到具体的执行的节点。才能用ros2 run找到节点
install(TARGETS
  cpp_node  
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