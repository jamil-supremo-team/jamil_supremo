#!/usr/bin/env bash

# ============================================================
# INICIO COMPLETO DEL PROYECTO
# KUKA KR 7 R900-3 - GRUPO 07
# ============================================================

WS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


# ============================================================
# CARGAR ENTORNO
# ============================================================

source "$WS/robot_setup.sh"


# ============================================================
# VERIFICAR QUE EL WORKSPACE ESTE COMPILADO
# ============================================================

if [ ! -f "$WS/install/setup.bash" ]; then

    echo
    echo "El workspace no esta compilado."
    echo "Compilando..."
    echo

    cd "$WS"

    colcon build --symlink-install

    source "$WS/install/setup.bash"

fi


# ============================================================
# FUNCION PARA ABRIR TERMINALES
# ============================================================

abrir_terminal()
{
    TITULO="$1"
    COMANDO="$2"

    gnome-terminal \
        --title="$TITULO" \
        -- bash -c "

            cd '$WS'

            source '$WS/robot_setup.sh'

            clear

            echo '========================================'
            echo ' $TITULO'
            echo '========================================'
            echo

            $COMANDO

            exec bash
        "
}


clear

echo "=============================================="
echo " KUKA KR 7 R900-3"
echo " GRUPO 07"
echo "=============================================="
echo
echo "Iniciando proyecto..."
echo


# ============================================================
# 1. RVIZ + ROBOT
# ============================================================

echo "[1/4] Abriendo KUKA en RViz..."

abrir_terminal \
    "01 - KUKA RViz" \
    "ros2 launch grupo07_kuka_kr7_bringup display.launch.py"


# Esperar a que RViz cargue
sleep 5


# ============================================================
# CERRAR JOINT STATE PUBLISHER GUI
#
# El IK publica /joint_states.
# No queremos dos nodos publicando al mismo tiempo.
# ============================================================

pkill -f joint_state_publisher_gui 2>/dev/null || true

sleep 1


# ============================================================
# 2. CINEMATICA DIRECTA
# ============================================================

echo "[2/4] Abriendo Cinematica Directa..."

abrir_terminal \
    "02 - Cinematica Directa FK" \
    "ros2 run grupo07_robot_kinematics fk_node"


sleep 1


# ============================================================
# 3. CINEMATICA INVERSA
# ============================================================

echo "[3/4] Abriendo Cinematica Inversa..."

abrir_terminal \
    "03 - Cinematica Inversa IK" \
    "ros2 run grupo07_robot_kinematics ik_node"


sleep 1


# ============================================================
# 4. INTERFAZ GRAFICA
# ============================================================

echo "[4/4] Abriendo Interfaz IK..."

abrir_terminal \
    "04 - Interfaz IK" \
    "ros2 run grupo07_robot_kinematics target_gui"


echo
echo "=============================================="
echo " PROYECTO INICIADO"
echo "=============================================="
echo
echo " Robot + RViz             OK"
echo " Cinematica Directa FK    OK"
echo " Cinematica Inversa IK    OK"
echo " Interfaz XYZ             OK"
echo
echo "=============================================="
