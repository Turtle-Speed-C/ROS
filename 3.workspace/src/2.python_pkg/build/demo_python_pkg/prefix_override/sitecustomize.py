import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/lxf/桌面/ROS/2.python_pkg/install/demo_python_pkg'
