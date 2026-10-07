import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/alex/Desktop/Robot/grupo_07_kuka_kr7_r900_3_ws/install/grupo07_robot_kinematics'
