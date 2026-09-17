#include <stdint.h>
#include <stdbool.h>

#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"

#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"


uint32_t FS = 180000000;   // 1.5 segundos

int contador = 0;


#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif


void mostrar_numero(void)
{
    // 0 = 0000
    if(contador == 0)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);
    }

    // 1 = 0001
    else if(contador == 1)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_0);
    }

    // 2 = 0010
    else if(contador == 2)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4);
    }

    // 3 = 0011
    else if(contador == 3)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0);

        GPIOPinWrite(
            GPIO_PORTF_BASE,
            GPIO_PIN_4 | GPIO_PIN_0,
            GPIO_PIN_4 | GPIO_PIN_0
        );
    }

    // 4 = 0100
    else if(contador == 4)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);
    }

    // 5 = 0101
    else if(contador == 5)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_0);
    }

    // 6 = 0110
    else if(contador == 6)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4);
    }

    // 7 = 0111
    else if(contador == 7)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE,GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4 | GPIO_PIN_0);
    }

    // 8 = 1000
    else if(contador == 8)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);
    }

    // 9 = 1001
    else if(contador == 9)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_0);
    }

    // 10 = 1010
    else if(contador == 10)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4);
    }

    // 11 = 1011
    else if(contador == 11)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1);

        GPIOPinWrite(
            GPIO_PORTF_BASE,
            GPIO_PIN_4 | GPIO_PIN_0,
            GPIO_PIN_4 | GPIO_PIN_0
        );
    }

    // 12 = 1100
    else if(contador == 12)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1 | GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);
    }

    // 13 = 1101
    else if(contador == 13)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,GPIO_PIN_1 | GPIO_PIN_0,GPIO_PIN_1 | GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_0);
    }

    // 14 = 1110
    else if(contador == 14)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,GPIO_PIN_1 | GPIO_PIN_0,GPIO_PIN_1 | GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4);
    }

    // 15 = 1111
    else if(contador == 15)
    {
        GPIOPinWrite(
            GPIO_PORTN_BASE,
            GPIO_PIN_1 | GPIO_PIN_0,
            GPIO_PIN_1 | GPIO_PIN_0
        );

        GPIOPinWrite(
            GPIO_PORTF_BASE,
            GPIO_PIN_4 | GPIO_PIN_0,
            GPIO_PIN_4 | GPIO_PIN_0
        );
    }
}


void timer0A_handler(void)
{
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    contador = contador + 1;

    if(contador > 15)
    {
        contador = 0;
    }

    mostrar_numero();
}


int main(void)
{
    SysCtlClockFreqSet(
        (SYSCTL_XTAL_25MHZ |
         SYSCTL_OSC_MAIN |
         SYSCTL_USE_PLL |
         SYSCTL_CFG_VCO_480),
        120000000
    );


    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);


    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_TIMER0))
    {
    }


    GPIOPinTypeGPIOOutput(
        GPIO_PORTN_BASE,
        GPIO_PIN_1 | GPIO_PIN_0
    );

    GPIOPinTypeGPIOOutput(
        GPIO_PORTF_BASE,
        GPIO_PIN_4 | GPIO_PIN_0
    );


    GPIOPinTypeGPIOInput(
        GPIO_PORTJ_BASE,
        GPIO_PIN_0
    );

    GPIOPadConfigSet(
        GPIO_PORTJ_BASE,
        GPIO_PIN_0,
        GPIO_STRENGTH_2MA,
        GPIO_PIN_TYPE_STD_WPU
    );


    mostrar_numero();


    TimerConfigure(
        TIMER0_BASE,
        TIMER_CFG_PERIODIC
    );

    TimerLoadSet(
        TIMER0_BASE,
        TIMER_A,
        FS
    );


    IntMasterEnable();

    IntEnable(INT_TIMER0A);

    TimerIntEnable(
        TIMER0_BASE,
        TIMER_TIMA_TIMEOUT
    );

    TimerEnable(
        TIMER0_BASE,
        TIMER_A
    );


    while(1)
    {
        if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)
        {
            FS = 360000000;   // 3 segundos

            TimerLoadSet(
                TIMER0_BASE,
                TIMER_A,
                FS
            );

            while(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)
            {
            }
        }
    }
}
