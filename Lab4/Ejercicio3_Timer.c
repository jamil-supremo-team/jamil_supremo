#include <stdint.h>
#include <stdbool.h>

#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"

#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"


uint32_t FS = 240000000;

int contador = 0;
int tiempo = 0;


#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif


void mostrar_numero(void)
{
    if(contador == 0)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);
    }

    else if(contador == 1)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_0);
    }

    else if(contador == 2)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4);
    }

    else if(contador == 3)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0);
        GPIOPinWrite(GPIO_PORTF_BASE,
                     GPIO_PIN_4 | GPIO_PIN_0,
                     GPIO_PIN_4 | GPIO_PIN_0);
    }

    else if(contador == 4)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);
    }

    else if(contador == 5)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_0);
    }

    else if(contador == 6)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4);
    }

    else if(contador == 7)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE,GPIO_PIN_4 | GPIO_PIN_0,GPIO_PIN_4 | GPIO_PIN_0);
    }

    else if(contador == 8)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);
    }

    else if(contador == 9)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_0);
    }

    else if(contador == 10)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4);
    }

    else if(contador == 11)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE,
                     GPIO_PIN_4 | GPIO_PIN_0,
                     GPIO_PIN_4 | GPIO_PIN_0);
    }

    else if(contador == 12)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_1 | GPIO_PIN_0,
                     GPIO_PIN_1 | GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);
    }

    else if(contador == 13)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_1 | GPIO_PIN_0,
                     GPIO_PIN_1 | GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_0);
    }

    else if(contador == 14)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_1 | GPIO_PIN_0,
                     GPIO_PIN_1 | GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, GPIO_PIN_4);
    }

    else if(contador == 15)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_1 | GPIO_PIN_0,
                     GPIO_PIN_1 | GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE,
                     GPIO_PIN_4 | GPIO_PIN_0,
                     GPIO_PIN_4 | GPIO_PIN_0);
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

    TimerConfigure(TIMER0_BASE,TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE,TIMER_A,FS);
    IntMasterEnable();
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE,TIMER_TIMA_TIMEOUT);
    TimerEnable(TIMER0_BASE,TIMER_A);


    while(1)
    {
        if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)
        {
            tiempo = tiempo + 1;

            if(tiempo == 1)
            {
                FS = 120000000;
            }

            else if(tiempo == 2)
            {
                FS = 60000000;
            }

            else if(tiempo == 3)
            {
                FS = 240000000;
                tiempo = 0;
            }

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
