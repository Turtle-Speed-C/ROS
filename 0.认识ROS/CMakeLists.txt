cmake_minimum_required(VERSION 3.8)
#指定项目所需的CMake最低版本为3.8。
project(HelloWorld)
#规定项目名称为：HelloWorld:
#与文件名没有关系。
#设置项目名称，可以在后续通过${PROJECT_NAME}变量引用
#创建一些内置变量（如PROJECT_SOURCE_DIR、PROJECT_BINARY_DIR等）
add_executable(learn_cmake hello_world.cpp)
#learn_cmake：生成的可执行文件名称
#hello_world.cpp：用于编译这个可执行文件的源代码文件


#project的项目名和文件名.cpp都是独立的
#   project(HelloWorld) - 项目名称，用于逻辑组织
#   CMakeLists.txt - CMake配置文件，文件名必须是这个
#   add_executable(learn_cmake ...) - 可执行文件名，也可以不同
#   hello_world.cpp - 源代码文件名
#编译的两个阶段：
#   1.cmake ..：
#       解读CMakeLists.txt文件
#       生成构建系统文件（Makefile）
#   2 make：
#       读取第一个命令产生的Makefile
#       生成目标文件
#形象比喻：
#   cmake：建筑师——设计图纸
#   make：建筑工人——实施盖房子