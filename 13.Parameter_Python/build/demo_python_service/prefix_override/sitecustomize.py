import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/lxf/Desktop/ROS/13.Parameter_Python/install/demo_python_service'
