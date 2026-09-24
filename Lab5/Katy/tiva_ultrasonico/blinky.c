#include <stdint.h>
#include "inc/tm4c1294ncpdt.h"

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


    // ---------------- PROGRAMA ----------------
   uint32_t distancia = 0;

    while(1)
    {
        if((UART0_FR_R & 0x10) == 0)
        {
            char dato = UART0_DR_R & 0xFF;

       
            if(dato >= '0' && dato <= '9')
            {
                distancia = distancia * 10 + (dato - '0');
            }

           
            else if(dato == '\n')
            { 
                GPIO_PORTN_DATA_R &= ~0x03;
                GPIO_PORTF_AHB_DATA_R &= ~0x11;

            
                if(distancia > 100)
                {
                   
                }

                else if(distancia > 80)
                {
                    GPIO_PORTN_DATA_R |= 0x02;      // PN1
                }

            
                else if(distancia > 60)
                {
                    GPIO_PORTN_DATA_R |= 0x03;      // PN1 + PN0
                }

                // Entre 6 y 4 cm
                else if(distancia >= 40)
                {
                    GPIO_PORTN_DATA_R |= 0x03;      // PN1 + PN0
                    GPIO_PORTF_AHB_DATA_R |= 0x10;  // PF4
                }

                else
                {
                    GPIO_PORTN_DATA_R |= 0x03;      // PN1 + PN0
                    GPIO_PORTF_AHB_DATA_R |= 0x11;  // PF4 + PF0
                }

                
                distancia = 0;
            }
        }
    }
}