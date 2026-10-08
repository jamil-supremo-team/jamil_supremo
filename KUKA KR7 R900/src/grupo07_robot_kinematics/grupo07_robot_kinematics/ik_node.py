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

from .kinematics import tcp_position


class IKNode(Node):

    def __init__(self):

        super().__init__(
            'ik_node'
        )

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

        self.q_current = np.zeros(
            6,
            dtype=float
        )

        self.q_start = np.zeros(
            6,
            dtype=float
        )

        self.q_goal = np.zeros(
            6,
            dtype=float
        )

        self.current_target = np.zeros(
            3,
            dtype=float
        )

        self.has_target = False

        self.moving = False

        self.hold_position = False

        self.motion_duration = 4.0

        self.motion_start_time = None

        self.target_subscriber = (
            self.create_subscription(
                Point,
                '/target',
                self.target_callback,
                10
            )
        )

        self.joint_subscriber = (
            self.create_subscription(
                JointState,
                '/joint_states',
                self.joint_state_callback,
                10
            )
        )

        self.joint_publisher = (
            self.create_publisher(
                JointState,
                '/joint_states',
                10
            )
        )

        self.solution_publisher = (
            self.create_publisher(
                JointState,
                '/ik/solution',
                10
            )
        )

        self.target_pose_publisher = (
            self.create_publisher(
                PoseStamped,
                '/target_pose',
                10
            )
        )

        self.reached_publisher = (
            self.create_publisher(
                Point,
                '/ik/reached_point',
                10
            )
        )

        self.error_vector_publisher = (
            self.create_publisher(
                Vector3,
                '/ik/error_vector',
                10
            )
        )

        self.error_norm_publisher = (
            self.create_publisher(
                Float64,
                '/ik/error_norm',
                10
            )
        )

        self.converged_publisher = (
            self.create_publisher(
                Bool,
                '/ik/converged',
                10
            )
        )

        self.timer = self.create_timer(
            0.02,
            self.timer_callback
        )

        self.get_logger().info(
            '\n'
            '========================================\n'
            ' CINEMATICA INVERSA\n'
            ' KUKA KR 7 R900-3\n'
            '========================================\n'
            ' Metodo: numerico iterativo\n'
            ' Jacobiano: diferencias finitas\n'
            ' Solucion: Damped Least Squares\n'
            ' Entrada: /target\n'
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

        if not all(
            name in joints
            for name in self.joint_names
        ):

            return

        self.q_current = np.array([
            joints[name]
            for name in self.joint_names
        ], dtype=float)

    def numerical_jacobian(
        self,
        q,
        h=1e-6
    ):

        q = np.asarray(
            q,
            dtype=float
        )

        J = np.zeros(
            (3, 6),
            dtype=float
        )

        for i in range(6):

            q_plus = q.copy()

            q_minus = q.copy()

            q_plus[i] += h

            q_minus[i] -= h

            p_plus = tcp_position(
                q_plus
            )

            p_minus = tcp_position(
                q_minus
            )

            J[:, i] = (
                p_plus
                -
                p_minus
            ) / (2.0 * h)

        return J

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
        max_iterations=600,
        tolerance=1e-3
    ):

        target = np.asarray(
            target,
            dtype=float
        )

        q = np.asarray(
            q_seed,
            dtype=float
        ).copy()

        q = np.clip(
            q,
            self.q_min,
            self.q_max
        )

        alpha = 0.70

        damping = 0.02

        max_step = 0.15

        I = np.eye(
            3,
            dtype=float
        )

        for iteration in range(
            max_iterations
        ):

            p_actual = tcp_position(
                q
            )

            error_vector = (
                target
                -
                p_actual
            )

            error_norm = float(
                np.linalg.norm(
                    error_vector
                )
            )

            if error_norm < tolerance:

                return (
                    q,
                    iteration + 1,
                    error_norm,
                    True
                )

            J = self.numerical_jacobian(
                q
            )

            JJT = (
                J
                @
                J.T
            )

            M = (
                JJT
                +
                (damping ** 2) * I
            )

            try:

                auxiliary = np.linalg.solve(
                    M,
                    error_vector
                )

                delta_q = (
                    alpha
                    *
                    (
                        J.T
                        @
                        auxiliary
                    )
                )

            except np.linalg.LinAlgError:

                delta_q = (
                    alpha
                    *
                    (
                        np.linalg.pinv(J)
                        @
                        error_vector
                    )
                )

            max_abs = float(
                np.max(
                    np.abs(
                        delta_q
                    )
                )
            )

            if max_abs > max_step:

                delta_q = (
                    delta_q
                    *
                    (
                        max_step
                        /
                        max_abs
                    )
                )

            q_next = (
                q
                +
                delta_q
            )

            q_next = np.clip(
                q_next,
                self.q_min,
                self.q_max
            )

            if np.linalg.norm(
                q_next - q
            ) < 1e-10:

                q = q_next

                break

            q = q_next

        p_final = tcp_position(
            q
        )

        final_error = float(
            np.linalg.norm(
                target
                -
                p_final
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

        seeds = [

            self.q_current.copy(),

            np.zeros(
                6,
                dtype=float
            ),

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
                direction,
                -0.6,
                 1.4,
                 0.0,
                -0.5,
                 0.0
            ]),

            np.array([
                direction,
                -1.8,
                 1.8,
                 0.0,
                 0.5,
                 0.0
            ]),

            np.array([
                direction + math.pi / 2.0,
                -0.7,
                 0.7,
                 0.0,
                 0.5,
                 0.0
            ]),

            np.array([
                direction - math.pi / 2.0,
                -0.7,
                 0.7,
                 0.0,
                 0.5,
                 0.0
            ])

        ]

        return seeds

    def solve_ik(
        self,
        target
    ):

        seeds = self.get_seeds(
            target
        )

        valid_solutions = []

        best_failed = None

        for index, seed in enumerate(
            seeds
        ):

            (
                q_solution,
                iterations,
                error,
                converged
            ) = self.solve_from_seed(
                target,
                seed
            )

            self.get_logger().info(
                f'Semilla {index + 1}: '
                f'error = {error:.6f} m | '
                f'iteraciones = {iterations} | '
                f'convergio = {converged}'
            )

            if converged:

                distance = float(
                    np.linalg.norm(
                        q_solution
                        -
                        self.q_current
                    )
                )

                valid_solutions.append(
                    (
                        distance,
                        error,
                        iterations,
                        q_solution
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
                        q_solution
                    )

        if len(
            valid_solutions
        ) > 0:

            valid_solutions.sort(
                key=lambda item: (
                    item[0],
                    item[1]
                )
            )

            (
                _,
                error,
                iterations,
                q_solution

            ) = valid_solutions[0]

            return (
                q_solution,
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
        ], dtype=float)

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
            f'X = {target[0]:.6f} m\n'
            f'Y = {target[1]:.6f} m\n'
            f'Z = {target[2]:.6f} m\n'
            '========================================'
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

        error_vector = (
            target
            -
            p_final
        )

        real_error = float(
            np.linalg.norm(
                error_vector
            )
        )

        reached_msg = Point()

        reached_msg.x = float(
            p_final[0]
        )

        reached_msg.y = float(
            p_final[1]
        )

        reached_msg.z = float(
            p_final[2]
        )

        self.reached_publisher.publish(
            reached_msg
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

        norm_msg.data = real_error

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

            q_rad_text = np.array2string(
                q_solution,
                formatter={
                    'float_kind':
                    lambda value:
                    f'{value:.6f}'
                }
            )

            q_deg = np.degrees(
                q_solution
            )

            q_deg_text = np.array2string(
                q_deg,
                formatter={
                    'float_kind':
                    lambda value:
                    f'{value:.6f}'
                }
            )

            self.get_logger().info(
                '\n'
                '========================================\n'
                ' IK CONVERGIO\n'
                '========================================\n'
                f'Iteraciones = {iterations}\n'
                f'Error final = {real_error:.6f} m\n'
                '\n'
                f'q [rad] =\n'
                f'{q_rad_text}\n'
                '\n'
                f'q [grados] =\n'
                f'{q_deg_text}\n'
                '\n'
                'Objetivo:\n'
                f'X = {target[0]:.6f} m\n'
                f'Y = {target[1]:.6f} m\n'
                f'Z = {target[2]:.6f} m\n'
                '\n'
                'Posicion alcanzada:\n'
                f'X = {p_final[0]:.6f} m\n'
                f'Y = {p_final[1]:.6f} m\n'
                f'Z = {p_final[2]:.6f} m\n'
                '========================================'
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

        else:

            self.get_logger().warning(
                '\n'
                '========================================\n'
                ' IK NO CONVERGIO\n'
                '========================================\n'
                f'Mejor error encontrado = '
                f'{real_error:.6f} m\n'
                '\n'
                'Posicion mas cercana:\n'
                f'X = {p_final[0]:.6f} m\n'
                f'Y = {p_final[1]:.6f} m\n'
                f'Z = {p_final[2]:.6f} m\n'
                '========================================'
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

            tau = float(
                np.clip(
                    tau,
                    0.0,
                    1.0
                )
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
                    'Movimiento finalizado.'
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