# KUKA KR 7 R900-3 - Grupo 07

Proyecto ROS 2 para la simulación y control cinemático del robot
KUKA KR 7 R900-3.

El proyecto incluye:

- Visualización del robot en RViz
- Cinemática Directa (FK)
- Cinemática Inversa (IK)
- Jacobiano
- Control mediante objetivo cartesiano X, Y, Z
- Interfaz gráfica para enviar objetivos
- Validación de la posición alcanzada


# Requisitos

El proyecto fue desarrollado utilizando:

- Ubuntu
- ROS 2 Jazzy
- ROSLab
- Python 3
- RViz2


# Ejecución del proyecto

Abrir una terminal y ejecutar:

1. roslab shell
2. entrar dentro del repositor.
3. Encoentrar los archivos.
	iniciar_robot.sh 
	robot_setup.sh
4. Ejecute
	source robot_settup.sh
	./iniciar_robot.sh
