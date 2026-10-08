# Desarrollo de cinematica - KUKA KR 7 R900-3

## 1. Identificacion del robot

El robot asignado al grupo es el KUKA KR 7 R900-3. Es un manipulador serial industrial de seis grados de libertad.

Las articulaciones identificadas en ROS 2 son:

- joint_1
- joint_2
- joint_3
- joint_4
- joint_5
- joint_6

Todas las articulaciones consideradas son revolutas.

El marco base utilizado por el modelo es:

- base_link

El efector final utilizado para el desarrollo cinematico es:

- tool0

## 2. Cadena cinematica

La cadena cinematica considerada es:

world -> base_link -> joint_1 -> link_1 -> joint_2 -> link_2 -> joint_3 -> link_3 -> joint_4 -> link_4 -> joint_5 -> link_5 -> joint_6 -> link_6 -> tool0

Para el calculo cinematico se consideran las seis articulaciones revolutas. La transformacion fija final desde link_6 hasta tool0 se incluye porque tool0 representa el efector final del modelo.

## 3. Datos geometricos obtenidos del URDF

| Transformacion | xyz [m] | rpy [rad] | Eje articular |
|---|---|---|---|
| base_link -> joint_1 | [0.0, 0.0, 0.1921] | [pi, 0, 0] | z |
| link_1 -> joint_2 | [0.05, -0.0946, -0.1499] | [pi/2, 0, 0] | z |
| link_2 -> joint_3 | [0.4100, 0.0, -0.0031] | [0, 0, 0] | z |
| link_3 -> joint_4 | [0.0895, -0.0450, -0.0915] | [pi/2, 0, -pi/2] | z |
| link_4 -> joint_5 | [0.0, 0.0484, -0.3505] | [0, pi/2, pi/2] | z |
| link_5 -> joint_6 | [0.0508, 0.0, -0.0484] | [pi/2, 0, -pi/2] | z |
| link_6 -> tool0 | [0.0, 0.0, -0.0262] | [pi, 0, pi] | fijo |

## 4. Estado actual

Ya se verifico que el robot abre correctamente en RViz2 y que publica el topico /joint_states.

Tambien se verifico que el robot publica las seis articulaciones:

- joint_1
- joint_2
- joint_3
- joint_4
- joint_5
- joint_6

El siguiente paso es realizar la asignacion de marcos de referencia siguiendo la convencion Denavit-Hartenberg estandar.

## 5. Asignacion de marcos de referencia

Para el desarrollo cinematico se utilizara la convencion Denavit-Hartenberg estandar.

Segun esta convencion, el eje z de cada marco se asocia con el eje de movimiento de la articulacion correspondiente. Como el KUKA KR 7 R900-3 es un manipulador serial de seis articulaciones revolutas, cada variable articular q_i representa una rotacion alrededor del eje z correspondiente.

La asignacion de marcos se realiza a partir de la cadena cinematica observada en el URDF del robot. Cada articulacion conecta un link padre con un link hijo. Por esta razon, el origen de cada marco se coloca en la posicion de la articulacion correspondiente.

La regla utilizada es la siguiente:

- El eje z_i se alinea con el eje de giro de la articulacion siguiente.
- El eje x_i se define sobre la normal comun entre dos ejes z consecutivos.
- El eje y_i se obtiene aplicando la regla de la mano derecha.
- El marco {0} se fija en la base del robot.
- El marco {T} se fija en el efector final tool0.

La cadena de marcos considerada es:

{0} -> {1} -> {2} -> {3} -> {4} -> {5} -> {6} -> {T}

donde {T} corresponde al efector final tool0.

### 5.1 Origenes de los marcos

| Marco | Origen fisico | Link asociado | Articulacion relacionada |
|---|---|---|---|
| {0} | base_link | base_link | referencia fija |
| {1} | joint_1 | link_1 | joint_1 |
| {2} | joint_2 | link_2 | joint_2 |
| {3} | joint_3 | link_3 | joint_3 |
| {4} | joint_4 | link_4 | joint_4 |
| {5} | joint_5 | link_5 | joint_5 |
| {6} | joint_6 | link_6 | joint_6 |
| {T} | tool0 | tool0 | efector final |

### 5.2 Ejes z de movimiento

Como todas las articulaciones son revolutas, el eje z se toma como el eje de rotacion de cada articulacion.

| Variable articular | Articulacion ROS 2 | Eje de giro usado |
|---|---|---|
| q1 | joint_1 | z0 |
| q2 | joint_2 | z1 |
| q3 | joint_3 | z2 |
| q4 | joint_4 | z3 |
| q5 | joint_5 | z4 |
| q6 | joint_6 | z5 |

Por tanto, cada transformacion articular incluye una rotacion variable alrededor de su eje z:

q1 alrededor de z0  
q2 alrededor de z1  
q3 alrededor de z2  
q4 alrededor de z3  
q5 alrededor de z4  
q6 alrededor de z5  

### 5.3 Relacion geometrica entre marcos

Los desplazamientos entre articulaciones se obtuvieron del URDF generado del robot. Estos desplazamientos permiten identificar la separacion fisica entre los origenes de los marcos.

| Transformacion | Desplazamiento xyz [m] | Rotacion fija rpy [rad] |
|---|---|---|
| base_link -> joint_1 | [0.0, 0.0, 0.1921] | [pi, 0, 0] |
| link_1 -> joint_2 | [0.05, -0.0946, -0.1499] | [pi/2, 0, 0] |
| link_2 -> joint_3 | [0.4100, 0.0, -0.0031] | [0, 0, 0] |
| link_3 -> joint_4 | [0.0895, -0.0450, -0.0915] | [pi/2, 0, -pi/2] |
| link_4 -> joint_5 | [0.0, 0.0484, -0.3505] | [0, pi/2, pi/2] |
| link_5 -> joint_6 | [0.0508, 0.0, -0.0484] | [pi/2, 0, -pi/2] |
| link_6 -> tool0 | [0.0, 0.0, -0.0262] | [pi, 0, pi] |

La transformacion fija desde link_6 hasta tool0 se incluye al final de la cadena, porque tool0 representa el efector final usado para reportar la posicion y orientacion del robot.

### 5.4 Figura de frames

La Figura 2 muestra el robot KUKA KR 7 R900-3 en RViz2 con los frames TF visibles. Esta figura se utiliza para verificar visualmente la ubicacion de los marcos de referencia sobre la cadena cinematica.

Figura 2. Asignacion de marcos de referencia del robot KUKA KR 7 R900-3.
## 6. Paso pendiente

El siguiente paso es construir la tabla de parametros Denavit-Hartenberg del robot.

Despues se escribiran las matrices homogeneas individuales A_0_1, A_1_2, A_2_3, A_3_4, A_4_5 y A_5_6.

Finalmente se obtendra la cinematica directa multiplicando las transformaciones individuales hasta llegar al efector final tool0.