#!/usr/bin/env bash
source /opt/ros/jazzy/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
if [ -f "$HOME/Desktop/Robot/grupo_07_kuka_kr7_r900_3_ws/install/setup.bash" ]; then
  source "$HOME/Desktop/Robot/grupo_07_kuka_kr7_r900_3_ws/install/setup.bash"
fi
