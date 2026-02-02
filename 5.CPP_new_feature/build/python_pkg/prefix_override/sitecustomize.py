import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/lxf/桌面/ROS/5.CPP_new_feature/install/python_pkg'
