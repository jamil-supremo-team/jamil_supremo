#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$PROJECT_DIR"

source /opt/ros/jazzy/setup.bash
source "$PROJECT_DIR/install/setup.bash"

gnome-terminal -- bash -c "
cd '$PROJECT_DIR'
source /opt/ros/jazzy/setup.bash
source '$PROJECT_DIR/install/setup.bash'
ros2 run grupo07_robot_kinematics ik_node
exec bash
" &

sleep 2

gnome-terminal -- bash -c "
cd '$PROJECT_DIR'
source /opt/ros/jazzy/setup.bash
source '$PROJECT_DIR/install/setup.bash'
ros2 run grupo07_robot_kinematics target_gui_node
exec bash
" &

ros2 launch grupo07_kuka_kr7_bringup display.launch.py
