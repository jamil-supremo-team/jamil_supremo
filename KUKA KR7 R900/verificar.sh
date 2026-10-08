#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo " KUKA KR 7 R900-3 - GRUPO 07"
echo " Verificacion del entorno"
echo "=========================================="
echo


echo "[1] ROS 2 Jazzy"

if [ -f /opt/ros/jazzy/setup.bash ]; then
    echo "OK - ROS 2 Jazzy instalado"
else
    echo "ERROR - ROS 2 Jazzy no encontrado"
fi

echo


echo "[2] Cargando entorno del proyecto"

if [ -f "$PROJECT_DIR/robot_setup.sh" ]; then

    source "$PROJECT_DIR/robot_setup.sh"

    echo "OK - robot_setup.sh cargado"

else

    echo "ERROR - robot_setup.sh no encontrado"

    if [ -f /opt/ros/jazzy/setup.bash ]; then
        source /opt/ros/jazzy/setup.bash
    fi

    if [ -f "$PROJECT_DIR/install/setup.bash" ]; then
        source "$PROJECT_DIR/install/setup.bash"
    fi

fi

echo


echo "[3] ROS 2"

if command -v ros2 >/dev/null 2>&1; then
    echo "OK - ros2 disponible"
else
    echo "ERROR - ros2 no disponible"
fi

echo


echo "[4] RViz2"

if command -v rviz2 >/dev/null 2>&1; then
    echo "OK - RViz2 disponible"
else
    echo "ERROR - RViz2 no disponible"
fi

echo


echo "[5] Colcon"

if command -v colcon >/dev/null 2>&1; then
    echo "OK - colcon disponible"
else
    echo "ERROR - colcon no disponible"
fi

echo


echo "[6] Soporte KUKA"

if ros2 pkg prefix kuka_agilus_support >/dev/null 2>&1; then

    echo "OK - kuka_agilus_support encontrado"

    ros2 pkg prefix kuka_agilus_support

else

    echo "ERROR - kuka_agilus_support no encontrado"

fi

echo


echo "[7] Paquete Bringup"

if ros2 pkg prefix grupo07_kuka_kr7_bringup >/dev/null 2>&1; then
    echo "OK - grupo07_kuka_kr7_bringup encontrado"
else
    echo "ERROR - grupo07_kuka_kr7_bringup no encontrado"
fi

echo


echo "[8] Paquete de Cinematica"

if ros2 pkg prefix grupo07_robot_kinematics >/dev/null 2>&1; then
    echo "OK - grupo07_robot_kinematics encontrado"
else
    echo "ERROR - grupo07_robot_kinematics no encontrado"
fi

echo


echo "[9] Proyecto compilado"

if [ -f "$PROJECT_DIR/install/setup.bash" ]; then
    echo "OK - Proyecto compilado"
else
    echo "ERROR - Proyecto no compilado"
    echo "Ejecute primero:"
    echo "./instalar.sh"
fi

echo


echo "[10] Python - NumPy"

if python3 -c "import numpy" >/dev/null 2>&1; then
    echo "OK - NumPy disponible"
else
    echo "ERROR - NumPy no disponible"
fi

echo


echo "[11] Python - Tkinter"

if python3 -c "import tkinter" >/dev/null 2>&1; then
    echo "OK - Tkinter disponible"
else
    echo "ERROR - Tkinter no disponible"
fi

echo


echo "=========================================="
echo " FIN DE LA VERIFICACION"
echo "=========================================="
