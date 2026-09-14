#include <stdint.h>
#include <stdbool.h>

#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"

#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"


uint32_t FS = 120000000 * 2;   // inicia en 2 segundos
uint8_t estado = 0;


#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif


void timer0A_handler(void)
{
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    estado++;

    if(estado > 2)
    {
        estado = 0;
    }


    // ESTADO 0
    if(estado == 0)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_0);

        GPIOPinWrite(GPIO_PORTF_BASE,
                     GPIO_PIN_0 | GPIO_PIN_4,
                     0);
    }


    // ESTADO 1
    if(estado == 1)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_0 | GPIO_PIN_1,
                     GPIO_PIN_1);

        GPIOPinWrite(GPIO_PORTF_BASE,
                     GPIO_PIN_0 | GPIO_PIN_4,
                     0);
    }


    // ESTADO 2
    if(estado == 2)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_0 | GPIO_PIN_1,
                     0);

        GPIOPinWrite(GPIO_PORTF_BASE,
                     GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0 | GPIO_PIN_4);
    }
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


    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);


    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_TIMER0))
    {
    }


    GPIOPinTypeGPIOOutput(
        GPIO_PORTN_BASE,
        GPIO_PIN_0 | GPIO_PIN_1
    );

    GPIOPinTypeGPIOOutput(
        GPIO_PORTF_BASE,
        GPIO_PIN_0 | GPIO_PIN_4
    );


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

    IntEnable(
        INT_TIMER0A
    );

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
    }
}