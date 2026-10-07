#!/usr/bin/env bash

# ============================================================
# CONFIGURACION DEL ENTORNO
# KUKA KR 7 R900-3 - GRUPO 07
# ============================================================

WS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ROS 2 Jazzy
source /opt/ros/jazzy/setup.bash

# Middleware ROS 2
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Workspace compilado
if [ -f "$WS/install/setup.bash" ]; then
    source "$WS/install/setup.bash"
fi

echo "=============================================="
echo " KUKA KR 7 R900-3"
echo " Entorno cargado correctamente"
echo "=============================================="
echo "Workspace:"
echo "$WS"
