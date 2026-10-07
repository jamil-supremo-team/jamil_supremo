import tkinter as tk
from tkinter import ttk

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from std_msgs.msg import Bool, Float64


class TargetGUI(Node):

    def __init__(self):

        super().__init__('target_gui')

        self.running = True

        # Publicador del objetivo cartesiano
        self.target_publisher = self.create_publisher(
            Point,
            '/target',
            10
        )

        # Suscriptores de resultados de la IK
        self.create_subscription(
            Bool,
            '/ik/converged',
            self.converged_callback,
            10
        )

        self.create_subscription(
            Float64,
            '/ik/error_norm',
            self.error_callback,
            10
        )

        self.create_subscription(
            Point,
            '/ik/reached_point',
            self.reached_callback,
            10
        )

        # Ventana principal
        self.root = tk.Tk()

        self.root.title(
            'KUKA KR 7 R900-3 - Control IK'
        )

        self.root.geometry(
            '470x720'
        )

        self.root.resizable(
            False,
            False
        )

        # Estilo de la interfaz
        style = ttk.Style()

        try:
            style.theme_use('clam')
        except:
            pass

        style.configure(
            'Title.TLabel',
            font=('Arial', 16, 'bold')
        )

        style.configure(
            'Subtitle.TLabel',
            font=('Arial', 10)
        )

        style.configure(
            'Axis.TLabel',
            font=('Arial', 11, 'bold')
        )

        style.configure(
            'Send.TButton',
            font=('Arial', 11, 'bold')
        )

        main_frame = ttk.Frame(
            self.root,
            padding=20
        )

        main_frame.pack(
            fill='both',
            expand=True
        )

        ttk.Label(
            main_frame,
            text='KUKA KR 7 R900-3',
            style='Title.TLabel'
        ).pack(
            pady=(0, 3)
        )

        ttk.Label(
            main_frame,
            text='Control de posición mediante Cinemática Inversa',
            style='Subtitle.TLabel'
        ).pack(
            pady=(0, 15)
        )

        target_frame = ttk.LabelFrame(
            main_frame,
            text='  Objetivo cartesiano [m]  ',
            padding=15
        )

        target_frame.pack(
            fill='x',
            pady=(0, 10)
        )

        # Valores iniciales del objetivo
        self.x_var = tk.DoubleVar(
            value=0.977
        )

        self.y_var = tk.DoubleVar(
            value=0.000
        )

        self.z_var = tk.DoubleVar(
            value=0.388
        )

        # Controles de X, Y y Z
        self.create_coordinate_control(
            target_frame,
            'X',
            self.x_var,
            0.10,
            1.05,
            0
        )

        self.create_coordinate_control(
            target_frame,
            'Y',
            self.y_var,
            -0.60,
            0.60,
            1
        )

        self.create_coordinate_control(
            target_frame,
            'Z',
            self.z_var,
            0.10,
            0.90,
            2
        )

        # Botones de posiciones predefinidas
        preset_frame = ttk.Frame(
            main_frame
        )

        preset_frame.pack(
            fill='x',
            pady=(0, 10)
        )

        ttk.Button(
            preset_frame,
            text='Home',
            command=self.home_values
        ).pack(
            side='left',
            expand=True,
            fill='x',
            padx=(0, 4)
        )

        ttk.Button(
            preset_frame,
            text='Objetivo 1',
            command=self.preset_1
        ).pack(
            side='left',
            expand=True,
            fill='x',
            padx=4
        )

        ttk.Button(
            preset_frame,
            text='Objetivo 2',
            command=self.preset_2
        ).pack(
            side='left',
            expand=True,
            fill='x',
            padx=(4, 0)
        )

        ttk.Button(
            main_frame,
            text='ENVIAR OBJETIVO',
            style='Send.TButton',
            command=self.send_target
        ).pack(
            fill='x',
            ipady=7,
            pady=(0, 12)
        )

        # Panel de resultados
        result_frame = ttk.LabelFrame(
            main_frame,
            text='  Resultado de Cinemática Inversa  ',
            padding=15
        )

        result_frame.pack(
            fill='x'
        )

        status_frame = ttk.Frame(
            result_frame
        )

        status_frame.pack(
            fill='x',
            pady=4
        )

        ttk.Label(
            status_frame,
            text='Estado:',
            style='Axis.TLabel'
        ).pack(
            side='left'
        )

        self.status_label = ttk.Label(
            status_frame,
            text='Esperando objetivo...'
        )

        self.status_label.pack(
            side='right'
        )

        error_frame = ttk.Frame(
            result_frame
        )

        error_frame.pack(
            fill='x',
            pady=4
        )

        ttk.Label(
            error_frame,
            text='Error final:',
            style='Axis.TLabel'
        ).pack(
            side='left'
        )

        self.error_label = ttk.Label(
            error_frame,
            text='--- m'
        )

        self.error_label.pack(
            side='right'
        )

        ttk.Separator(
            result_frame,
            orient='horizontal'
        ).pack(
            fill='x',
            pady=12
        )

        ttk.Label(
            result_frame,
            text='Posición alcanzada',
            style='Axis.TLabel'
        ).pack(
            anchor='w',
            pady=(0, 8)
        )

        self.reached_x_label = self.create_result_row(
            result_frame,
            'X'
        )

        self.reached_y_label = self.create_result_row(
            result_frame,
            'Y'
        )

        self.reached_z_label = self.create_result_row(
            result_frame,
            'Z'
        )

        ttk.Separator(
            result_frame,
            orient='horizontal'
        ).pack(
            fill='x',
            pady=12
        )

        ttk.Label(
            result_frame,
            text='Último objetivo enviado',
            style='Axis.TLabel'
        ).pack(
            anchor='w',
            pady=(0, 8)
        )

        self.sent_target_label = ttk.Label(
            result_frame,
            text='X = ---    Y = ---    Z = ---'
        )

        self.sent_target_label.pack(
            anchor='w'
        )

        self.root.after(
            20,
            self.ros_update
        )

        self.root.protocol(
            'WM_DELETE_WINDOW',
            self.close_gui
        )

        self.get_logger().info(
            'GUI de Cinemática Inversa iniciada.'
        )

        self.get_logger().info(
            'Publicando objetivos en /target'
        )


    # Crea un control para cada coordenada
    def create_coordinate_control(
        self,
        parent,
        name,
        variable,
        minimum,
        maximum,
        row
    ):

        container = ttk.Frame(
            parent
        )

        container.grid(
            row=row,
            column=0,
            sticky='ew',
            pady=7
        )

        container.columnconfigure(
            0,
            weight=1
        )

        top_frame = ttk.Frame(
            container
        )

        top_frame.grid(
            row=0,
            column=0,
            sticky='ew'
        )

        top_frame.columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            top_frame,
            text=name,
            style='Axis.TLabel'
        ).grid(
            row=0,
            column=0,
            sticky='w'
        )

        value_box = ttk.Spinbox(
            top_frame,
            from_=minimum,
            to=maximum,
            increment=0.001,
            textvariable=variable,
            width=10,
            format='%.3f'
        )

        value_box.grid(
            row=0,
            column=2,
            sticky='e'
        )

        slider = ttk.Scale(
            container,
            from_=minimum,
            to=maximum,
            orient='horizontal',
            variable=variable
        )

        slider.grid(
            row=1,
            column=0,
            sticky='ew',
            pady=(5, 0)
        )

        parent.columnconfigure(
            0,
            weight=1
        )


    # Crea una fila para mostrar resultados
    def create_result_row(
        self,
        parent,
        axis_name
    ):

        row = ttk.Frame(
            parent
        )

        row.pack(
            fill='x',
            pady=3
        )

        ttk.Label(
            row,
            text=axis_name,
            style='Axis.TLabel'
        ).pack(
            side='left'
        )

        value_label = ttk.Label(
            row,
            text='--- m'
        )

        value_label.pack(
            side='right'
        )

        return value_label


    # Posicion inicial del robot
    def home_values(self):

        self.x_var.set(
            0.977
        )

        self.y_var.set(
            0.000
        )

        self.z_var.set(
            0.388
        )


    # Primer objetivo predefinido
    def preset_1(self):

        self.x_var.set(
            0.400
        )

        self.y_var.set(
            0.200
        )

        self.z_var.set(
            0.400
        )


    # Segundo objetivo predefinido
    def preset_2(self):

        self.x_var.set(
            0.300
        )

        self.y_var.set(
            -0.200
        )

        self.z_var.set(
            0.600
        )


    # Envia el objetivo XYZ al nodo de IK
    def send_target(self):

        try:

            x = float(
                self.x_var.get()
            )

            y = float(
                self.y_var.get()
            )

            z = float(
                self.z_var.get()
            )

        except:

            self.status_label.config(
                text='Valores inválidos'
            )

            return

        msg = Point()

        msg.x = x
        msg.y = y
        msg.z = z

        self.target_publisher.publish(
            msg
        )

        self.status_label.config(
            text='Calculando IK...'
        )

        self.error_label.config(
            text='--- m'
        )

        self.reached_x_label.config(
            text='--- m'
        )

        self.reached_y_label.config(
            text='--- m'
        )

        self.reached_z_label.config(
            text='--- m'
        )

        self.sent_target_label.config(
            text=(
                f'X = {x:.3f} m    '
                f'Y = {y:.3f} m    '
                f'Z = {z:.3f} m'
            )
        )

        self.get_logger().info(
            f'Objetivo enviado: '
            f'X={x:.3f}, '
            f'Y={y:.3f}, '
            f'Z={z:.3f}'
        )


    # Actualiza el estado de convergencia
    def converged_callback(
        self,
        msg
    ):

        if msg.data:

            self.status_label.config(
                text='OBJETIVO ALCANZADO'
            )

        else:

            self.status_label.config(
                text='IK NO CONVERGIÓ'
            )


    # Actualiza el error final
    def error_callback(
        self,
        msg
    ):

        self.error_label.config(
            text=f'{msg.data:.6f} m'
        )


    # Actualiza la posicion alcanzada
    def reached_callback(
        self,
        msg
    ):

        self.reached_x_label.config(
            text=f'{msg.x:.4f} m'
        )

        self.reached_y_label.config(
            text=f'{msg.y:.4f} m'
        )

        self.reached_z_label.config(
            text=f'{msg.z:.4f} m'
        )


    # Procesa los callbacks de ROS 2
    def ros_update(self):

        if (
            self.running
            and
            rclpy.ok()
        ):

            rclpy.spin_once(
                self,
                timeout_sec=0.0
            )

            if self.running:

                self.root.after(
                    20,
                    self.ros_update
                )


    # Cierra la interfaz
    def close_gui(self):

        self.running = False

        self.root.destroy()


    # Ejecuta la interfaz
    def run(self):

        self.root.mainloop()


def main(args=None):

    rclpy.init(
        args=args
    )

    node = TargetGUI()

    try:

        node.run()

    except KeyboardInterrupt:

        pass

    finally:

        node.running = False

        try:

            node.destroy_node()

        except:

            pass

        if rclpy.ok():

            rclpy.shutdown()


if __name__ == '__main__':

    main()