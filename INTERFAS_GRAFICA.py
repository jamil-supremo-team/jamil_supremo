import tkinter as tk
import serial
import time


# ============================================================
# COLORES DE LA INTERFAZ
# ============================================================

COLOR_FONDO = "#E8EEF7"
COLOR_TITULO = "#163A5F"
COLOR_TEXTO = "#1F2937"

COLOR_FRAME = "#D9E4F5"
COLOR_FRAME_AUX = "#EAF2F8"

COLOR_BOTON = "#2E86DE"
COLOR_BOTON_ACTIVO = "#1B4F72"

COLOR_LED_IZQ = "#F1C40F"
COLOR_LED_DER = "#3498DB"

COLOR_BUZZER = "#8E44AD"

COLOR_EMERGENCIA = "#C0392B"
COLOR_EMERGENCIA_ACTIVO = "#922B21"

COLOR_CONECTADO = "#229954"
COLOR_DESCONECTADO = "#C0392B"


# ============================================================
# COMUNICACION UART
# ============================================================

class ComunicacionUART:
    def __init__(self, puerto, baudrate):
        self.puerto = puerto
        self.baudrate = baudrate
        self.tiva = None
        self.conectada = False
        try:
            self.tiva = serial.Serial(
                self.puerto,
                self.baudrate,
                timeout=0.1
            )
            self.conectada = True
            print("TIVA CONECTADA")
        except Exception as e:
            print("ERROR UART:", e)

    def enviar(self, comando):
        if self.tiva is not None and self.tiva.is_open:
            self.tiva.write(
                (comando + "\n").encode()
            )
            self.tiva.flush()
            time.sleep(0.02)
            print("Enviado:", comando)


    def cerrar(self):
        if self.tiva is not None and self.tiva.is_open:
            self.tiva.close()


# ============================================================
# MOTOR
# ============================================================

class Motor:
    def __init__(self, numero, comunicacion):
        self.numero = numero
        self.comunicacion = comunicacion
        # Estado inicial
        self.estado = "PARADO"
        # PWM inicial
        self.pwm = 0
    # ========================================================
    # CAMBIAR DIRECCION
    # ========================================================
    def cambiar_direccion(self):
        # ADELANTE -> ATRAS
        if self.estado == "ADELANTE":
            self.comunicacion.enviar(
                f"M{self.numero}B"
            )
            self.estado = "ATRÁS"
        # PARADO o ATRAS -> ADELANTE
        else:
            self.comunicacion.enviar(
                f"M{self.numero}F"
            )
            self.estado = "ADELANTE"


    # ========================================================
    # PWM
    # ========================================================

    def cambiar_pwm(self, valor):
        self.pwm = int(float(valor))
        self.comunicacion.enviar(
            f"M{self.numero}PWM:{self.pwm}"
        )
        # PWM = 0 -> detener
        if self.pwm == 0:
            self.estado = "PARADO"
    # ========================================================
    # PARAR
    # ========================================================

    def parar(self):
        self.comunicacion.enviar(
            f"M{self.numero}S"
        )
        self.estado = "PARADO"


# ============================================================
# DISPOSITIVO AUXILIAR
# ============================================================

class Dispositivo:

    def __init__(self, comando_on, comando_off):
        self.comando_on = comando_on
        self.comando_off = comando_off
        self.activo = False

    def cambiar_estado(self, comunicacion):
        if self.activo:
            comunicacion.enviar(
                self.comando_off
            )
            self.activo = False
        else:
            comunicacion.enviar(
                self.comando_on
            )
            self.activo = True


    def apagar(self, comunicacion):
        comunicacion.enviar(
            self.comando_off
        )
        self.activo = False


# ============================================================
# INTERFAZ
# ============================================================

class InterfazMotores:

    def __init__(
        self,
        ventana,
        comunicacion,
        motores
    ):
        self.ventana = ventana
        self.comunicacion = comunicacion
        self.motores = motores
        # ====================================================
        # ESTADO DE EMERGENCIA
        # ====================================================
        self.emergencia = False

        # ====================================================
        # DISPOSITIVOS
        # ====================================================

        # LED izquierda
        self.led_izquierda = Dispositivo(
            "LI1",
            "LI0"
        )

        # LED derecha
        self.led_derecha = Dispositivo(
            "LD1",
            "LD0"
        )

        # Buzzer
        self.buzzer = Dispositivo(
            "BZ1",
            "BZ0"
        )

        # ====================================================
        # CONFIGURACION VENTANA
        # ====================================================

        self.ventana.title(
            "Control de Robot"
        )

        self.ventana.geometry(
            "1200x750"
        )

        self.ventana.resizable(
            False,
            False
        )

        # COLOR DE FONDO

        self.ventana.configure(
            bg=COLOR_FONDO
        )


        self.estados = []

        self.textos_pwm = []


        # Crear interfaz

        self.crear_interfaz()


        # Cerrar ventana correctamente

        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar
        )


    # ========================================================
    # INTERFAZ PRINCIPAL
    # ========================================================

    def crear_interfaz(self):

        # ----------------------------------------------------
        # TITULO
        # ----------------------------------------------------

        tk.Label(
            self.ventana,
            text="CONTROL DEL ROBOT",
            font=("Arial", 24, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TITULO
        ).pack(
            pady=15
        )


        # ----------------------------------------------------
        # ESTADO TIVA
        # ----------------------------------------------------

        if self.comunicacion.conectada:

            texto = "● TIVA CONECTADA"
            color = COLOR_CONECTADO

        else:

            texto = "● TIVA NO CONECTADA"
            color = COLOR_DESCONECTADO


        tk.Label(
            self.ventana,
            text=texto,
            font=("Arial", 13, "bold"),
            bg=COLOR_FONDO,
            fg=color
        ).pack(
            pady=3
        )


        # ====================================================
        # MOTORES
        # ====================================================

        frame_motores = tk.LabelFrame(
            self.ventana,
            text="CONTROL INDIVIDUAL DE MOTORES",
            font=("Arial", 14, "bold"),
            bg=COLOR_FRAME,
            fg=COLOR_TITULO,
            padx=15,
            pady=15
        )

        frame_motores.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        for i in range(4):

            self.crear_motor(
                frame_motores,
                self.motores[i],
                i
            )


        # ====================================================
        # LEDS Y BUZZER
        # ====================================================

        frame_auxiliares = tk.LabelFrame(
            self.ventana,
            text="LEDS Y BUZZER",
            font=("Arial", 14, "bold"),
            bg=COLOR_FRAME_AUX,
            fg=COLOR_TITULO,
            padx=20,
            pady=15
        )

        frame_auxiliares.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        # ----------------------------------------------------
        # LED IZQUIERDA
        # ----------------------------------------------------

        self.boton_led_izquierda = tk.Button(
            frame_auxiliares,
            text="LED IZQUIERDA",
            width=18,
            height=2,
            font=("Arial", 11, "bold"),

            bg=COLOR_LED_IZQ,
            fg="black",

            activebackground="#D4AC0D",
            activeforeground="black",

            command=self.cambiar_led_izquierda
        )

        self.boton_led_izquierda.grid(
            row=0,
            column=0,
            padx=15,
            pady=5
        )


        # ----------------------------------------------------
        # LED DERECHA
        # ----------------------------------------------------

        self.boton_led_derecha = tk.Button(
            frame_auxiliares,
            text="LED DERECHA",
            width=18,
            height=2,
            font=("Arial", 11, "bold"),

            bg=COLOR_LED_DER,
            fg="white",

            activebackground="#2874A6",
            activeforeground="white",

            command=self.cambiar_led_derecha
        )

        self.boton_led_derecha.grid(
            row=0,
            column=1,
            padx=15,
            pady=5
        )


        # ----------------------------------------------------
        # BUZZER
        # ----------------------------------------------------

        self.boton_buzzer = tk.Button(
            frame_auxiliares,
            text="BUZZER",
            width=18,
            height=2,
            font=("Arial", 11, "bold"),

            bg=COLOR_BUZZER,
            fg="white",

            activebackground="#6C3483",
            activeforeground="white",

            command=self.cambiar_buzzer
        )

        self.boton_buzzer.grid(
            row=0,
            column=2,
            padx=15,
            pady=5
        )


        # ====================================================
        # PARADA DE EMERGENCIA
        # ====================================================

        frame_emergencia = tk.LabelFrame(
            self.ventana,
            text="SEGURIDAD",
            font=("Arial", 14, "bold"),
            bg="#FDEDEC",
            fg=COLOR_EMERGENCIA,
            padx=20,
            pady=15
        )

        frame_emergencia.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        self.boton_emergencia = tk.Button(
            frame_emergencia,
            text="PARADA DE EMERGENCIA",
            width=25,
            height=2,
            font=("Arial", 12, "bold"),

            bg=COLOR_EMERGENCIA,
            fg="white",

            activebackground=COLOR_EMERGENCIA_ACTIVO,
            activeforeground="white",

            command=self.cambiar_emergencia
        )

        self.boton_emergencia.pack(
            pady=5
        )


    # ========================================================
    # CREAR MOTOR
    # ========================================================

    def crear_motor(
        self,
        padre,
        motor,
        columna
    ):

        frame = tk.LabelFrame(
            padre,
            text=f"MOTOR {motor.numero}",
            font=("Arial", 12, "bold"),
            bg="#F4F7FB",
            fg=COLOR_TITULO,
            padx=15,
            pady=12
        )

        frame.grid(
            row=0,
            column=columna,
            padx=15,
            pady=8
        )


        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        estado = tk.StringVar(
            value="PARADO"
        )


        # ----------------------------------------------------
        # PWM
        # ----------------------------------------------------

        texto_pwm = tk.StringVar(
            value="PWM: 0 / 255"
        )


        self.estados.append(
            estado
        )

        self.textos_pwm.append(
            texto_pwm
        )


        # ----------------------------------------------------
        # LABEL ESTADO
        # ----------------------------------------------------

        tk.Label(
            frame,
            textvariable=estado,
            font=("Arial", 11, "bold"),
            bg="#F4F7FB",
            fg=COLOR_TEXTO
        ).pack(
            pady=4
        )


        # ----------------------------------------------------
        # LABEL PWM
        # ----------------------------------------------------

        tk.Label(
            frame,
            textvariable=texto_pwm,
            font=("Arial", 11, "bold"),
            bg="#F4F7FB",
            fg=COLOR_TITULO
        ).pack(
            pady=4
        )


        # ----------------------------------------------------
        # SCALE PWM
        # ----------------------------------------------------

        escala = tk.Scale(
            frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            length=190,
            resolution=1,
            showvalue=False,

            bg="#F4F7FB",
            fg=COLOR_TITULO,
            troughcolor="#B8C7D9",
            highlightthickness=0,

            command=lambda valor,
            m=motor,
            t=texto_pwm:

                self.cambiar_pwm(
                    m,
                    t,
                    valor
                )
        )


        escala.set(0)


        escala.pack(
            pady=5
        )


        # ----------------------------------------------------
        # BOTON MOTOR
        # ----------------------------------------------------

        tk.Button(
            frame,
            text=f"MOTOR{motor.numero}",
            width=14,
            height=2,
            font=("Arial", 11, "bold"),

            bg=COLOR_BOTON,
            fg="white",

            activebackground=COLOR_BOTON_ACTIVO,
            activeforeground="white",

            command=lambda m=motor,
            e=estado:

                self.cambiar_direccion(
                    m,
                    e
                )
        ).pack(
            pady=8
        )


    # ========================================================
    # BOTON MOTOR
    # ========================================================

    def cambiar_direccion(
        self,
        motor,
        estado
    ):

        # Si emergencia está activa,
        # no permitimos movimiento.

        if self.emergencia:

            return


        motor.cambiar_direccion()


        estado.set(
            motor.estado
        )


    # ========================================================
    # PWM
    # ========================================================

    def cambiar_pwm(
        self,
        motor,
        texto_pwm,
        valor
    ):

        motor.cambiar_pwm(
            valor
        )


        texto_pwm.set(
            f"PWM: {motor.pwm} / 255"
        )


    # ========================================================
    # LED IZQUIERDA
    # ========================================================

    def cambiar_led_izquierda(self):

        if self.emergencia:

            return


        self.led_izquierda.cambiar_estado(
            self.comunicacion
        )


        if self.led_izquierda.activo:

            self.boton_led_izquierda.config(
                text="LED IZQUIERDA: ON"
            )

        else:

            self.boton_led_izquierda.config(
                text="LED IZQUIERDA"
            )


    # ========================================================
    # LED DERECHA
    # ========================================================

    def cambiar_led_derecha(self):

        if self.emergencia:

            return


        self.led_derecha.cambiar_estado(
            self.comunicacion
        )


        if self.led_derecha.activo:

            self.boton_led_derecha.config(
                text="LED DERECHA: ON"
            )

        else:

            self.boton_led_derecha.config(
                text="LED DERECHA"
            )


    # ========================================================
    # BUZZER
    # ========================================================

    def cambiar_buzzer(self):

        if self.emergencia:

            return


        self.buzzer.cambiar_estado(
            self.comunicacion
        )


        if self.buzzer.activo:

            self.boton_buzzer.config(
                text="BUZZER: ON"
            )

        else:

            self.boton_buzzer.config(
                text="BUZZER"
            )


    # ========================================================
    # PARADA DE EMERGENCIA
    # ========================================================

    def cambiar_emergencia(self):

        # Enviar comando a la Tiva

        self.comunicacion.enviar(
            "E"
        )


        # Cambiar estado local

        self.emergencia = not self.emergencia


        # ----------------------------------------------------
        # EMERGENCIA ACTIVADA
        # ----------------------------------------------------

        if self.emergencia:

            # La Tiva detiene todo,
            # pero actualizamos también la interfaz.

            for motor in self.motores:

                motor.estado = "PARADO"


            for estado in self.estados:

                estado.set(
                    "PARADO"
                )


            # Estados auxiliares

            self.led_izquierda.activo = False
            self.led_derecha.activo = False
            self.buzzer.activo = False


            self.boton_led_izquierda.config(
                text="LED IZQUIERDA"
            )

            self.boton_led_derecha.config(
                text="LED DERECHA"
            )

            self.boton_buzzer.config(
                text="BUZZER"
            )


            self.boton_emergencia.config(
                text="EMERGENCIA ACTIVA",

                bg=COLOR_EMERGENCIA_ACTIVO,
                activebackground=COLOR_EMERGENCIA
            )


        # ----------------------------------------------------
        # EMERGENCIA DESACTIVADA
        # ----------------------------------------------------

        else:

            self.boton_emergencia.config(
                text="PARADA DE EMERGENCIA",

                bg=COLOR_EMERGENCIA,
                activebackground=COLOR_EMERGENCIA_ACTIVO
            )


    # ========================================================
    # CERRAR
    # ========================================================

    def cerrar(self):

        # ----------------------------------------------------
        # DETENER MOTORES
        # ----------------------------------------------------

        for motor in self.motores:

            motor.parar()


        # ----------------------------------------------------
        # APAGAR LEDS Y BUZZER
        # ----------------------------------------------------

        self.led_izquierda.apagar(
            self.comunicacion
        )

        self.led_derecha.apagar(
            self.comunicacion
        )

        self.buzzer.apagar(
            self.comunicacion
        )


        time.sleep(0.1)


        # ----------------------------------------------------
        # CERRAR UART
        # ----------------------------------------------------

        self.comunicacion.cerrar()


        # ----------------------------------------------------
        # CERRAR TKINTER
        # ----------------------------------------------------

        self.ventana.destroy()


# ============================================================
# MAIN
# ============================================================

def main():

    # UART

    comunicacion = ComunicacionUART(
        "/dev/ttyACM0",
        9600
    )


    # MOTORES

    motor1 = Motor(
        1,
        comunicacion
    )

    motor2 = Motor(
        2,
        comunicacion
    )

    motor3 = Motor(
        3,
        comunicacion
    )

    motor4 = Motor(
        4,
        comunicacion
    )


    motores = [
        motor1,
        motor2,
        motor3,
        motor4
    ]


    # --------------------------------------------------------
    # TKINTER
    # --------------------------------------------------------

    ventana = tk.Tk()


    InterfazMotores(
        ventana,
        comunicacion,
        motores
    )


    ventana.mainloop()


if __name__ == "__main__":

    main()