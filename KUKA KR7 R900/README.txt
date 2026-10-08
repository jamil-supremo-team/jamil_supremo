IMT-342 ROBOTICA
Practica de Cinematica Directa e Inversa

GRUPO 07
Robot: KUKA KR 7 R900-3


============================================================
1. REQUISITOS
============================================================

La computadora debe tener previamente:

- Ubuntu 24.04
- ROS 2 Jazzy
- conexion a internet durante la primera instalacion

No es necesario utilizar ROSLAB.


============================================================
2. PRIMERA INSTALACION
============================================================

Abrir una terminal dentro de la carpeta del proyecto.

Dar permisos de ejecucion a los archivos:

chmod +x instalar.sh abrir_directa.sh abrir_inversa.sh

Ejecutar:

./instalar.sh

El instalador se encargara de:

- verificar ROS 2 Jazzy;
- instalar las dependencias necesarias;
- instalar el soporte necesario para el robot;
- instalar las dependencias de los paquetes ROS;
- compilar el proyecto con colcon.

Durante la compilacion se generaran automaticamente las carpetas:

build
install
log

La instalacion solamente es necesaria la primera vez.


============================================================
3. CINEMATICA DIRECTA
============================================================

Para ejecutar la Cinematica Directa abrir una terminal dentro de la carpeta del proyecto y ejecutar:

./abrir_directa.sh

Se abriran:

- RViz2;
- Joint State Publisher GUI;
- el robot KUKA KR 7 R900-3;
- el nodo de Cinematica Directa.

Mover las articulaciones utilizando Joint State Publisher GUI.

La terminal del nodo mostrara la posicion calculada del TCP:

X
Y
Z

La posicion calculada puede compararse en RViz2 en:

TF
Frames
tool0
Position


============================================================
4. CINEMATICA INVERSA
============================================================

Para ejecutar la Cinematica Inversa abrir una terminal dentro de la carpeta del proyecto y ejecutar:

./abrir_inversa.sh

Se abriran:

- RViz2;
- el robot KUKA KR 7 R900-3;
- el nodo de Cinematica Inversa;
- la interfaz grafica para ingresar el objetivo cartesiano.


IMPORTANTE:

Al iniciar el robot tambien aparecera Joint State Publisher GUI.

Para utilizar la Cinematica Inversa se debe cerrar la ventana Joint State Publisher GUI antes de enviar un objetivo.

Esto evita que Joint State Publisher GUI y el nodo de Cinematica Inversa publiquen al mismo tiempo sobre /joint_states.


Una vez cerrada la ventana Joint State Publisher GUI, utilizar la interfaz de Cinematica Inversa.

Ingresar:

X
Y
Z

y presionar:

ENVIAR OBJETIVO

El sistema calculara los valores articulares necesarios y movera el robot hacia la posicion solicitada.

La interfaz mostrara:

- estado de convergencia;
- error final;
- posicion X alcanzada;
- posicion Y alcanzada;
- posicion Z alcanzada.

La posicion tambien puede comprobarse en RViz2 en:

TF
Frames
tool0
Position

La Cinematica Inversa utiliza un metodo numerico iterativo, por lo que puede existir una pequena diferencia entre la posicion solicitada y la posicion alcanzada.


============================================================
5. EJECUCION RAPIDA
============================================================

PRIMERA VEZ:

chmod +x instalar.sh abrir_directa.sh abrir_inversa.sh
./instalar.sh


CINEMATICA DIRECTA:

./abrir_directa.sh


CINEMATICA INVERSA:

./abrir_inversa.sh


============================================================
6. ARCHIVOS PRINCIPALES
============================================================

instalar.sh

Instala las dependencias necesarias y compila el proyecto.


abrir_directa.sh

Abre el robot y ejecuta la Cinematica Directa.


abrir_inversa.sh

Abre el robot, ejecuta la Cinematica Inversa y abre la interfaz grafica.


src/

Contiene los paquetes ROS 2 y los codigos utilizados por el proyecto.


============================================================
7. NOTA
============================================================

Las carpetas:

build
install
log
__pycache__

no necesitan ser incluidas al compartir el proyecto.

Estas carpetas se generan automaticamente en la computadora donde se compile y ejecute el proyecto.
