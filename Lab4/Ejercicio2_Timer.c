#include <stdint.h>
#include <stdbool.h>

#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"

#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"


uint32_t FS = 120000000 * 2;
uint8_t contador = 0;


#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif


// Funcion de interrupcion del Timer0A
void timer0A_handler(void)
{
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    contador++;

    if(contador > 15)
    {
        contador = 0;
    }


    // 0 = 0000
    if(contador == 0)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0);
    }


    // 1 = 0001
    if(contador == 1)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0);
    }


    // 2 = 0010
    if(contador == 2)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0);
    }


    // 3 = 0011
    if(contador == 3)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_0 | GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0);
    }


    // 4 = 0100
    if(contador == 4)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0);
    }


    // 5 = 0101
    if(contador == 5)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0);
    }


    // 6 = 0110
    if(contador == 6)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0);
    }


    // 7 = 0111
    if(contador == 7)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_0 | GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0);
    }


    // 8 = 1000
    if(contador == 8)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_4);
    }


    // 9 = 1001
    if(contador == 9)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_4);
    }


    // 10 = 1010
    if(contador == 10)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_4);
    }


    // 11 = 1011
    if(contador == 11)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_0 | GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_4);
    }


    // 12 = 1100
    if(contador == 12)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0 | GPIO_PIN_4);
    }


    // 13 = 1101
    if(contador == 13)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0 | GPIO_PIN_4);
    }


    // 14 = 1110
    if(contador == 14)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0 | GPIO_PIN_4);
    }


    // 15 = 1111
    if(contador == 15)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_0 | GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0 | GPIO_PIN_4);
    }
}



int main(void)
{
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);


    // Habilitar perifericos
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);


    // Esperar que esten listos
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_TIMER0))
    {
    }


    // Configurar los 4 LEDs como salidas
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE,GPIO_PIN_0 | GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE,GPIO_PIN_0 | GPIO_PIN_4);


    // Configuracion del Timer0A
    TimerConfigure(TIMER0_BASE,TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE,TIMER_A,FS);
    // Habilitar interrupcion
    IntMasterEnable();
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE,TIMER_TIMA_TIMEOUT);
    TimerEnable(TIMER0_BASE,TIMER_A);


    // Bucle principal
    while(1)
    {
    }
}