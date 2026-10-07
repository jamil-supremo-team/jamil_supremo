import math
import numpy as np

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import (
    Point,
    PoseStamped,
    Vector3
)

from sensor_msgs.msg import JointState

from std_msgs.msg import (
    Bool,
    Float64
)

from .kinematics import (
    tcp_position,
    positional_jacobian
)


class IKNode(Node):

    def __init__(self):

        super().__init__('ik_node')

        self.joint_names = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]

        self.q_min = np.array([
            -3.22886,
            -3.31613,
            -2.00713,
            -3.49066,
            -2.09440,
            -6.10865
        ])

        self.q_max = np.array([
             3.22886,
             0.69813,
             2.79253,
             3.49066,
             2.09440,
             6.10865
        ])

        self.q_current = np.zeros(6)

        self.q_start = np.zeros(6)

        self.q_goal = np.zeros(6)

        self.current_target = np.zeros(3)

        self.has_target = False

        self.motion_duration = 4.0

        self.motion_start_time = None

        self.moving = False

        self.hold_position = False

        self.target_subscriber = self.create_subscription(
            Point,
            '/target',
            self.target_callback,
            10
        )

        self.joint_subscriber = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.joint_publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.solution_publisher = self.create_publisher(
            JointState,
            '/ik/solution',
            10
        )

        self.target_pose_publisher = self.create_publisher(
            PoseStamped,
            '/target_pose',
            10
        )

        self.reached_publisher = self.create_publisher(
            Point,
            '/ik/reached_point',
            10
        )

        self.error_vector_publisher = self.create_publisher(
            Vector3,
            '/ik/error_vector',
            10
        )

        self.error_norm_publisher = self.create_publisher(
            Float64,
            '/ik/error_norm',
            10
        )

        self.converged_publisher = self.create_publisher(
            Bool,
            '/ik/converged',
            10
        )

        self.timer = self.create_timer(
            0.02,
            self.timer_callback
        )

        self.get_logger().info(
            '========================================'
        )

        self.get_logger().info(
            ' IK - KUKA KR 7 R900-3'
        )

        self.get_logger().info(
            ' Metodo: Damped Least Squares'
        )

        self.get_logger().info(
            ' Esperando objetivo por /target'
        )

        self.get_logger().info(
            '========================================'
        )


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

        if all(
            name in joints
            for name in self.joint_names
        ):

            self.q_current = np.array([
                joints[name]
                for name in self.joint_names
            ])


    def publish_target_pose(
        self,
        target
    ):

        msg = PoseStamped()

        msg.header.stamp = (
            self.get_clock()
            .now()
            .to_msg()
        )

        msg.header.frame_id = 'base_link'

        msg.pose.position.x = float(
            target[0]
        )

        msg.pose.position.y = float(
            target[1]
        )

        msg.pose.position.z = float(
            target[2]
        )

        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 1.0

        self.target_pose_publisher.publish(
            msg
        )


    def solve_from_seed(
        self,
        target,
        q_seed,
        max_iterations=400,
        tolerance=1e-3
    ):

        q = np.asarray(
            q_seed,
            dtype=float
        ).copy()

        q = np.clip(
            q,
            self.q_min,
            self.q_max
        )

        alpha = 0.6

        damping = 0.02

        max_step = 0.20

        I = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ])

        for iteration in range(
            max_iterations
        ):

            Q = np.array([
                [q[0]],
                [q[1]],
                [q[2]],
                [q[3]],
                [q[4]],
                [q[5]]
            ])

            Pd = np.array([
                [target[0]],
                [target[1]],
                [target[2]]
            ])

            p_actual = tcp_position(
                q
            )

            P = np.array([
                [p_actual[0]],
                [p_actual[1]],
                [p_actual[2]]
            ])

            E = Pd - P

            error_norm = float(
                np.linalg.norm(
                    E
                )
            )

            if error_norm < tolerance:

                return (
                    q,
                    iteration + 1,
                    error_norm,
                    True
                )

            J_calc = positional_jacobian(
                q
            )

            J = np.array([

                [
                    J_calc[0, 0],
                    J_calc[0, 1],
                    J_calc[0, 2],
                    J_calc[0, 3],
                    J_calc[0, 4],
                    J_calc[0, 5]
                ],

                [
                    J_calc[1, 0],
                    J_calc[1, 1],
                    J_calc[1, 2],
                    J_calc[1, 3],
                    J_calc[1, 4],
                    J_calc[1, 5]
                ],

                [
                    J_calc[2, 0],
                    J_calc[2, 1],
                    J_calc[2, 2],
                    J_calc[2, 3],
                    J_calc[2, 4],
                    J_calc[2, 5]
                ]

            ])

            JT = np.array([

                [
                    J[0, 0],
                    J[1, 0],
                    J[2, 0]
                ],

                [
                    J[0, 1],
                    J[1, 1],
                    J[2, 1]
                ],

                [
                    J[0, 2],
                    J[1, 2],
                    J[2, 2]
                ],

                [
                    J[0, 3],
                    J[1, 3],
                    J[2, 3]
                ],

                [
                    J[0, 4],
                    J[1, 4],
                    J[2, 4]
                ],

                [
                    J[0, 5],
                    J[1, 5],
                    J[2, 5]
                ]

            ])

            JJT = (
                J
                @
                JT
            )

            LAMBDA2_I = (
                damping ** 2
            ) * I

            M = (
                JJT
                +
                LAMBDA2_I
            )

            try:

                M_INV = np.linalg.inv(
                    M
                )

                J_DLS = (
                    JT
                    @
                    M_INV
                )

            except np.linalg.LinAlgError:

                J_DLS = np.linalg.pinv(
                    J
                )

            DELTA_Q = (

                alpha

                *

                (
                    J_DLS
                    @
                    E
                )

            )

            max_abs = float(
                np.max(
                    np.abs(
                        DELTA_Q
                    )
                )
            )

            if max_abs > max_step:

                DELTA_Q = (

                    DELTA_Q

                    *

                    max_step

                    /

                    max_abs

                )

            Q_NEXT = (
                Q
                +
                DELTA_Q
            )

            q = np.array([
                Q_NEXT[0, 0],
                Q_NEXT[1, 0],
                Q_NEXT[2, 0],
                Q_NEXT[3, 0],
                Q_NEXT[4, 0],
                Q_NEXT[5, 0]
            ])

            q = np.clip(
                q,
                self.q_min,
                self.q_max
            )

        p_final = tcp_position(
            q
        )

        P_FINAL = np.array([
            [p_final[0]],
            [p_final[1]],
            [p_final[2]]
        ])

        P_DESIRED = np.array([
            [target[0]],
            [target[1]],
            [target[2]]
        ])

        E_FINAL = (
            P_DESIRED
            -
            P_FINAL
        )

        final_error = float(
            np.linalg.norm(
                E_FINAL
            )
        )

        return (
            q,
            max_iterations,
            final_error,
            False
        )


    def get_seeds(
        self,
        target
    ):

        direction = math.atan2(
            target[1],
            target[0]
        )

        return [

            self.q_current.copy(),

            np.zeros(6),

            np.array([
                direction,
                -0.8,
                1.0,
                0.0,
                0.5,
                0.0
            ]),

            np.array([
                direction,
                -1.3,
                0.5,
                0.0,
                0.5,
                0.0
            ]),

            np.array([
                direction,
                -1.0,
                -0.5,
                0.5,
                1.0,
                0.0
            ]),

            np.array([
                math.pi / 2.0,
                -0.7,
                0.7,
                0.0,
                0.5,
                0.0
            ]),

            np.array([
                -math.pi / 2.0,
                -0.7,
                0.7,
                0.0,
                0.5,
                0.0
            ])

        ]


    def solve_ik(
        self,
        target
    ):

        seeds = self.get_seeds(
            target
        )

        solutions = []

        best_failed = None

        for index, seed in enumerate(
            seeds
        ):

            (
                q,
                iterations,
                error,
                converged

            ) = self.solve_from_seed(
                target,
                seed
            )

            self.get_logger().info(
                f'Semilla {index + 1}: '
                f'error={error:.6f} m | '
                f'iter={iterations} | '
                f'convergencia={converged}'
            )

            if converged:

                distance = np.linalg.norm(
                    q
                    -
                    self.q_current
                )

                solutions.append(
                    (
                        distance,
                        error,
                        iterations,
                        q
                    )
                )

            else:

                if (
                    best_failed is None
                    or
                    error < best_failed[0]
                ):

                    best_failed = (
                        error,
                        iterations,
                        q
                    )

        if len(solutions) > 0:

            solutions.sort(
                key=lambda item: (
                    item[0],
                    item[1]
                )
            )

            (
                _,
                error,
                iterations,
                q

            ) = solutions[0]

            return (
                q,
                iterations,
                error,
                True
            )

        if best_failed is not None:

            return (
                best_failed[2],
                best_failed[1],
                best_failed[0],
                False
            )

        return (
            self.q_current.copy(),
            0,
            float('inf'),
            False
        )


    def target_callback(
        self,
        msg
    ):

        target = np.array([
            msg.x,
            msg.y,
            msg.z
        ])

        self.current_target = (
            target.copy()
        )

        self.has_target = True

        self.publish_target_pose(
            target
        )

        self.get_logger().info(

            '\n'
            '========================================\n'
            ' NUEVO OBJETIVO CARTESIANO\n'
            '========================================\n'
            f'x = {target[0]:.4f} m\n'
            f'y = {target[1]:.4f} m\n'
            f'z = {target[2]:.4f} m'

        )

        (
            q_solution,
            iterations,
            error,
            converged

        ) = self.solve_ik(
            target
        )

        p_final = tcp_position(
            q_solution
        )

        reached = Point()

        reached.x = float(
            p_final[0]
        )

        reached.y = float(
            p_final[1]
        )

        reached.z = float(
            p_final[2]
        )

        self.reached_publisher.publish(
            reached
        )

        error_vector = (
            target
            -
            p_final
        )

        error_msg = Vector3()

        error_msg.x = float(
            error_vector[0]
        )

        error_msg.y = float(
            error_vector[1]
        )

        error_msg.z = float(
            error_vector[2]
        )

        self.error_vector_publisher.publish(
            error_msg
        )

        norm_msg = Float64()

        norm_msg.data = float(
            error
        )

        self.error_norm_publisher.publish(
            norm_msg
        )

        converged_msg = Bool()

        converged_msg.data = bool(
            converged
        )

        self.converged_publisher.publish(
            converged_msg
        )

        solution_msg = JointState()

        solution_msg.header.stamp = (
            self.get_clock()
            .now()
            .to_msg()
        )

        solution_msg.name = (
            self.joint_names
        )

        solution_msg.position = (
            q_solution.tolist()
        )

        self.solution_publisher.publish(
            solution_msg
        )

        if converged:

            self.get_logger().info(

                '\n'
                '========================================\n'
                ' IK CONVERGIO\n'
                '========================================\n'
                f'Iteraciones = {iterations}\n'
                f'Error final = {error:.6f} m\n'
                '\n'
                f'q [rad] =\n'
                f'{np.round(q_solution, 5)}\n'
                '\n'
                f'q [grados] =\n'
                f'{np.round(np.degrees(q_solution), 2)}\n'
                '\n'
                f'Posicion alcanzada =\n'
                f'{np.round(p_final, 5)}'

            )

            self.q_start = (
                self.q_current.copy()
            )

            self.q_goal = (
                q_solution.copy()
            )

            self.motion_start_time = (
                self.get_clock()
                .now()
            )

            self.moving = True

            self.hold_position = False

            self.get_logger().info(
                'Iniciando movimiento suave hacia '
                'la solucion IK.'
            )

        else:

            self.get_logger().warning(

                '\n'
                '========================================\n'
                ' IK NO CONVERGIO\n'
                '========================================\n'
                f'Error minimo encontrado = '
                f'{error:.6f} m'

            )


    def publish_joint_state(
        self,
        q
    ):

        msg = JointState()

        msg.header.stamp = (
            self.get_clock()
            .now()
            .to_msg()
        )

        msg.name = (
            self.joint_names
        )

        msg.position = (
            q.tolist()
        )

        self.joint_publisher.publish(
            msg
        )


    def timer_callback(self):

        if self.has_target:

            self.publish_target_pose(
                self.current_target
            )

        if self.moving:

            now = (
                self.get_clock()
                .now()
            )

            elapsed = (
                now
                -
                self.motion_start_time
            ).nanoseconds / 1e9

            tau = (
                elapsed
                /
                self.motion_duration
            )

            tau = np.clip(
                tau,
                0.0,
                1.0
            )

            s = (

                0.5

                -

                0.5

                *

                math.cos(
                    math.pi
                    *
                    tau
                )

            )

            q_command = (

                self.q_start

                +

                s

                *

                (
                    self.q_goal
                    -
                    self.q_start
                )

            )

            self.publish_joint_state(
                q_command
            )

            if tau >= 1.0:

                self.moving = False

                self.hold_position = True

                self.q_current = (
                    self.q_goal.copy()
                )

                self.get_logger().info(
                    'Movimiento finalizado. '
                    'TCP en objetivo.'
                )

        elif self.hold_position:

            self.publish_joint_state(
                self.q_goal
            )


def main(args=None):

    rclpy.init(
        args=args
    )

    node = IKNode()

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