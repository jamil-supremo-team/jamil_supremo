#include <stdint.h>
#include "inc/tm4c1294ncpdt.h"

volatile uint32_t estado = 0;

void Timer0A_Handler(void)
{
    // Limpiar la bandera de interrupción del Timer0A
    TIMER0_ICR_R = 0x01;

    // Apagar los tres LEDs
    GPIO_PORTN_DATA_R &= ~0x03;       // PN0 y PN1 OFF
    GPIO_PORTF_AHB_DATA_R &= ~0x10;   // PF4 OFF

    if(estado == 0)
    {
        GPIO_PORTN_DATA_R |= 0x02;    // PN1 ON
        estado = 1;
    }
    else if(estado == 1)
    {
        GPIO_PORTN_DATA_R |= 0x01;    // PN0 ON
        estado = 2;
    }
    else
    {
        GPIO_PORTF_AHB_DATA_R |= 0x10; // PF4 ON
        estado = 0;
    }
}

int main(void)
{
    // ---------------- LEDs ----------------

    // Habilitar Puerto N y Puerto F
    SYSCTL_RCGCGPIO_R |= (1 << 12);   // Puerto N
    SYSCTL_RCGCGPIO_R |= (1 << 5);    // Puerto F

    // Esperar a que estén disponibles
    while((SYSCTL_PRGPIO_R & (1 << 12)) == 0)
    {
    }

    while((SYSCTL_PRGPIO_R & (1 << 5)) == 0)
    {
    }

    // PN0 y PN1 como salida
    GPIO_PORTN_DIR_R |= 0x03;
    GPIO_PORTN_DEN_R |= 0x03;

    // PF0 y PF4 como salida
    GPIO_PORTF_AHB_DIR_R |= 0x11;
    GPIO_PORTF_AHB_DEN_R |= 0x11;

    // Todos apagados inicialmente
    GPIO_PORTN_DATA_R &= ~0x03;
    GPIO_PORTF_AHB_DATA_R &= ~0x11; 

    GPIO_PORTN_DATA_R &= ~0x02;


    // ---------------- UART0 ----------------
    // Habilitar UART0 y GPIOA
    SYSCTL_RCGCUART_R |= 0x01;
    SYSCTL_RCGCGPIO_R |= 0x01;

    while((SYSCTL_PRUART_R & 0x01) == 0)
    {
    }

    while((SYSCTL_PRGPIO_R & 0x01) == 0)
    {
    }


    // PA0 = U0RX
    // PA1 = U0TX
    GPIO_PORTA_AHB_AFSEL_R |= 0x03;
    GPIO_PORTA_AHB_DEN_R |= 0x03;
    GPIO_PORTA_AHB_AMSEL_R &= ~0x03;

    GPIO_PORTA_AHB_PCTL_R =
        (GPIO_PORTA_AHB_PCTL_R & ~0x000000FF) | 0x00000011;

    // Deshabilitar UART mientras configuramos
    UART0_CTL_R &= ~0x01;

    // Usar PIOSC = 16 MHz como reloj de UART
    UART0_CC_R = 0x05;

    // 9600 baudios con reloj de 16 MHz
    UART0_IBRD_R = 104;
    UART0_FBRD_R = 11;

    // 8 bits, sin paridad, 1 bit de parada
    UART0_LCRH_R = 0x60;

    // Habilitar UART, TX y RX
    UART0_CTL_R = 0x301;

// ---------------- TIMER 0A ----------------

// Habilitar Timer0
SYSCTL_RCGCTIMER_R |= 0x01;

// Esperar a que Timer0 esté listo
while((SYSCTL_PRTIMER_R & 0x01) == 0)
{
}

// Deshabilitar Timer0A mientras configuramos
TIMER0_CTL_R &= ~0x01;

// Timer de 32 bits
TIMER0_CFG_R = 0x00;

// Modo periódico
TIMER0_TAMR_R = 0x02;

// 1 segundo aproximadamente con reloj de 16 MHz
TIMER0_TAILR_R = 16000000 - 1;

// Limpiar cualquier interrupción anterior
TIMER0_ICR_R = 0x01;

// Habilitar interrupción por timeout
TIMER0_IMR_R |= 0x01;

// Habilitar Timer0A en NVIC
NVIC_EN0_R |= (1 << 19);

// Encender Timer0A
TIMER0_CTL_R |= 0x01;

    // ---------------- PROGRAMA ----------------
    while(1)
    {
        // Revisar si llegó un dato por UART
        if((UART0_FR_R & 0x10) == 0)
        {
            char dato = UART0_DR_R & 0xFF;

            // Aceptar solamente números del 1 al 9
            if(dato >= '1' && dato <= '9')
            {
                uint32_t segundos = dato - '0';

                // Detener Timer
                TIMER0_CTL_R &= ~0x01;

                // Cambiar el tiempo
                TIMER0_TAILR_R = (16000000 * segundos) - 1;

                // Limpiar interrupción pendiente
                TIMER0_ICR_R = 0x01;

                // Volver a encender Timer
                TIMER0_CTL_R |= 0x01;
            }
        }
    }
}