KUKA KR 7 R900-3 - Grupo 07

Proyecto ROS 2 para la simulación y control cinemático del robot KUKA KR 7 R900-3.

El proyecto incluye:

Cinemática Directa
Cinemática Inversa
Visualización en RViz
Interfaz gráfica para enviar objetivos cartesianos


REQUISITOS

La computadora debe tener instalado:

Ubuntu 24.04
ROS 2 Jazzy
ROSLAB
Python 3
RViz2


CINEMÁTICA DIRECTA

1. Abrir una terminal.

2. Entrar a la carpeta donde se encuentra el proyecto.

cd Kuka_KR7_R900

3. Ejecutar:

roslab shell   -----> opcional
source robot_setup.sh
ros2 launch grupo07_kuka_kr7_bringup display.launch.py

4. Dejar esa terminal abierta.

5. Abrir una segunda terminal.

6. Entrar nuevamente a la carpeta del proyecto.

cd Kuka_KR7_R900

7. Ejecutar:

roslab shell  ----> opcional
source robot_setup.sh
ros2 run grupo07_robot_kinematics fk_node

8. Mover las articulaciones utilizando Joint State Publisher.

La terminal mostrará la posición calculada del robot:

X
Y
Z

La posición puede compararse en RViz en:

TF
Frames
tool0
Position



CINEMÁTICA INVERSA

1. Abrir una terminal.

2. Entrar a la carpeta donde se encuentra el proyecto.

cd Kuka_KR7_R900

3. Ejecutar:

roslab shell   ----> opcional
source robot_setup.sh
./iniciar_robot.sh

4. Este codigo nos permitira abrir todo lo necesario

5. Aparecera la ventana Joint State Publisher GUI.
   Tienes que cerrarla.

6. Posteriormente se abrira la interfaz de Cinematica Inversa.
   Desde esta interfaz podemos controlar al robot colocando la posicion deseada.

Ingresar las coordenadas deseadas:

X
Y
Z

7. Presionar:

ENVIAR OBJETIVO

El robot calculará la Cinemática Inversa y se moverá hacia la posición solicitada.

La posición final puede verificarse en:

RViz
TF
Frames
tool0
Position

La Cinemática Inversa utiliza un método numérico, por lo que puede existir una pequeña diferencia entre la posición solicitada y la posición alcanzada.