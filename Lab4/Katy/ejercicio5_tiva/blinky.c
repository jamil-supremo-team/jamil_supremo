#include <stdint.h>
#include <stdbool.h>
#include "inc/tm4c1294ncpdt.h"

volatile uint32_t estado = 0;


// ---------------- TIMER ----------------

void Timer0A_Handler(void)
{
    // Limpiar interrupción
    TIMER0_ICR_R = 0x01;

    // Apagar los 3 LEDs
    GPIO_PORTN_DATA_R &= ~0x03;
    GPIO_PORTF_AHB_DATA_R &= ~0x10;

    // Secuencia de 3 estados
    if(estado == 0)
    {
        GPIO_PORTN_DATA_R |= 0x02;   // PN1
        estado = 1;
    }
    else if(estado == 1)
    {
        GPIO_PORTN_DATA_R |= 0x01;   // PN0
        estado = 2;
    }
    else
    {
        GPIO_PORTF_AHB_DATA_R |= 0x10;  // PF4
        estado = 0;
    }
}


int main(void)
{

    // ---------------- LEDs ----------------

    SYSCTL_RCGCGPIO_R |= (1 << 12);   // Puerto N
    SYSCTL_RCGCGPIO_R |= (1 << 5);    // Puerto F

    while((SYSCTL_PRGPIO_R & (1 << 12)) == 0)
    {
    }

    while((SYSCTL_PRGPIO_R & (1 << 5)) == 0)
    {
    }

    GPIO_PORTN_DIR_R |= 0x03;
    GPIO_PORTN_DEN_R |= 0x03;

    GPIO_PORTF_AHB_DIR_R |= 0x10;
    GPIO_PORTF_AHB_DEN_R |= 0x10;


    // ---------------- UART0 ----------------

    SYSCTL_RCGCUART_R |= 0x01;
    SYSCTL_RCGCGPIO_R |= 0x01;

    while((SYSCTL_PRUART_R & 0x01) == 0)
    {
    }

    while((SYSCTL_PRGPIO_R & 0x01) == 0)
    {
    }

    GPIO_PORTA_AHB_AFSEL_R |= 0x03;
    GPIO_PORTA_AHB_DEN_R |= 0x03;

    GPIO_PORTA_AHB_PCTL_R =
        (GPIO_PORTA_AHB_PCTL_R & ~0xFF) | 0x11;

    UART0_CTL_R &= ~0x01;

    UART0_CC_R = 0x05;

    UART0_IBRD_R = 104;
    UART0_FBRD_R = 11;

    UART0_LCRH_R = 0x60;

    UART0_CTL_R = 0x301;


    // ---------------- TIMER0A ----------------

    SYSCTL_RCGCTIMER_R |= 0x01;

    while((SYSCTL_PRTIMER_R & 0x01) == 0)
    {
    }

    TIMER0_CTL_R &= ~0x01;

    TIMER0_CFG_R = 0x00;

    TIMER0_TAMR_R = 0x02;   // Timer periódico

    // Inicialmente 1 segundo
    TIMER0_TAILR_R = 16000000 - 1;

    TIMER0_ICR_R = 0x01;

    TIMER0_IMR_R |= 0x01;

    NVIC_EN0_R |= (1 << 19);

    TIMER0_CTL_R |= 0x01;


    // ---------------- PROGRAMA ----------------

    while(1)
    {
        // Si llega un dato por UART
        if((UART0_FR_R & 0x10) == 0)
        {
            char dato = UART0_DR_R;

            if(dato >= '1' && dato <= '9')
            {
                uint32_t segundos = dato - '0';

                // Detener timer
                TIMER0_CTL_R &= ~0x01;

                // Cambiar tiempo
                TIMER0_TAILR_R =
                    (16000000 * segundos) - 1;

                // Limpiar interrupción
                TIMER0_ICR_R = 0x01;

                // Volver a iniciar
                TIMER0_CTL_R |= 0x01;
            }
        }
    }
}