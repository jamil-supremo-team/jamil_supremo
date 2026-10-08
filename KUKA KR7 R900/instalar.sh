#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo " KUKA KR 7 R900-3 - GRUPO 07"
echo " Instalacion del proyecto"
echo "=========================================="
echo

cd "$PROJECT_DIR"

echo "[1/6] Verificando ROS 2 Jazzy..."

if [ ! -f /opt/ros/jazzy/setup.bash ]; then
    echo
    echo "ERROR: ROS 2 Jazzy no esta instalado."
    echo "Instale ROS 2 Jazzy Desktop antes de continuar."
    exit 1
fi

source /opt/ros/jazzy/setup.bash

echo "ROS 2 Jazzy encontrado."
echo


echo "[2/6] Instalando dependencias necesarias..."

sudo apt update

sudo apt install -y \
    ros-jazzy-kuka-agilus-support \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-xacro \
    ros-jazzy-rviz2 \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-numpy \
    python3-tk

echo
echo "Dependencias instaladas."
echo


echo "[3/6] Verificando rosdep..."

if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
    sudo rosdep init
fi

rosdep update

echo


echo "[4/6] Instalando dependencias de los paquetes ROS..."

rosdep install \
    --from-paths src \
    --ignore-src \
    -r \
    -y

echo


echo "[5/6] Limpiando compilaciones anteriores..."

rm -rf build install log

echo


echo "[6/6] Compilando proyecto..."

colcon build --symlink-install

echo

source "$PROJECT_DIR/install/setup.bash"

echo "=========================================="
echo " INSTALACION COMPLETADA"
echo "=========================================="
echo
echo "Proyecto ubicado en:"
echo "$PROJECT_DIR"
echo
echo "Ya puede ejecutar:"
echo
echo "  ./abrir_directa.sh"
echo
echo "o:"
echo
echo "  ./abrir_inversa.sh"
echo
