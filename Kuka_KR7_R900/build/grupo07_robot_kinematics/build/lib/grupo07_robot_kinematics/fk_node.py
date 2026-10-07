import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point

from .kinematics import (
    forward_kinematics
)


class FKNode(Node):

    def __init__(self):

        super().__init__(
            'fk_node'
        )


        self.joint_names = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]


        # ====================================================
        # SUSCRIPTOR
        # ====================================================

        self.joint_subscriber = (
            self.create_subscription(
                JointState,
                '/joint_states',
                self.joint_state_callback,
                10
            )
        )


        # ====================================================
        # PUBLICADOR
        # ====================================================

        self.position_publisher = (
            self.create_publisher(
                Point,
                '/fk_position',
                10
            )
        )


        self.get_logger().info(
            '\n'
            '========================================\n'
            ' CINEMATICA DIRECTA\n'
            ' KUKA KR 7 R900-3\n'
            ' NUEVA TABLA DH\n'
            '========================================\n'
            ' Suscrito a: /joint_states\n'
            ' Publicando: /fk_position\n'
            ' Comparar con: RViz -> tool0\n'
            '========================================'
        )


    # ========================================================
    # RECIBIR q1 ... q6
    # ========================================================

    def joint_state_callback(
        self,
        msg
    ):

        joints = dict(
            zip(
                msg.name,
                msg.position
            )
        )


        if not all(
            name in joints
            for name in self.joint_names
        ):

            return


        q = np.array([
            joints[name]
            for name in self.joint_names
        ])


        # ====================================================
        # CINEMATICA DIRECTA
        # ====================================================

        T06 = forward_kinematics(
            q
        )


        # ====================================================
        # POSICION DEL TCP
        # ====================================================

        p = T06[0:3, 3]


        # ====================================================
        # PUBLICAR POSICION
        # ====================================================

        position = Point()

        position.x = float(
            p[0]
        )

        position.y = float(
            p[1]
        )

        position.z = float(
            p[2]
        )


        self.position_publisher.publish(
            position
        )


        # ====================================================
        # MOSTRAR 6 DECIMALES
        # ====================================================

        q_text = np.array2string(
            q,
            formatter={
                'float_kind':
                lambda value: f'{value:.6f}'
            }
        )


        self.get_logger().info(
            '\n'
            '========================================\n'
            ' CINEMATICA DIRECTA - NUEVA DH\n'
            '========================================\n'
            f'q [rad] = {q_text}\n'
            '\n'
            'TCP calculado:\n'
            f'X = {p[0]:.6f} m\n'
            f'Y = {p[1]:.6f} m\n'
            f'Z = {p[2]:.6f} m\n'
            '\n'
            'Comparar estos valores con:\n'
            'RViz -> Frames -> tool0 -> Position\n'
            '========================================'
        )


def main(args=None):

    rclpy.init(
        args=args
    )


    node = FKNode()


    try:

        rclpy.spin(
            node
        )

    except KeyboardInterrupt:

        pass


    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':

    main()