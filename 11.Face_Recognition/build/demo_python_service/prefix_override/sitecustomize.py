import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/lxf/Desktop/ROS/11.Face_Recognition/install/demo_python_service'
