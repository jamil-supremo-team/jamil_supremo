#include <stdint.h>
#include <stdbool.h>

#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"

#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"


uint32_t FS;
int counter;


void timer0A_handler(void)
{
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    if(counter < 15)
    {
        counter++;
    }

    // Mostrar contador en binario
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1,
                 (counter & 0x01) ? GPIO_PIN_1 : 0);

    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0,
                 (counter & 0x02) ? GPIO_PIN_0 : 0);

    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4,
                 (counter & 0x04) ? GPIO_PIN_4 : 0);

    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0,
                 (counter & 0x08) ? GPIO_PIN_0 : 0);
}


int main(void)
{
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                        SYSCTL_OSC_MAIN |
                        SYSCTL_USE_PLL |
                        SYSCTL_CFG_VCO_480),
                        120000000);

    // Habilitar puertos
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);

    // Habilitar Timer0
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_TIMER0));

    // LEDs
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE,
                          GPIO_PIN_0 | GPIO_PIN_1);

    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE,
                          GPIO_PIN_0 | GPIO_PIN_4);

    // Switch PJ0
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);

    GPIOPadConfigSet(GPIO_PORTJ_BASE,
                     GPIO_PIN_0,
                     GPIO_STRENGTH_2MA,
                     GPIO_PIN_TYPE_STD_WPU);

    // Contador comienza en 0
    counter = 0;

    GPIOPinWrite(GPIO_PORTN_BASE,
                 GPIO_PIN_0 | GPIO_PIN_1, 0x00);

    GPIOPinWrite(GPIO_PORTF_BASE,
                 GPIO_PIN_0 | GPIO_PIN_4, 0x00);

    // 1,5 segundos
    FS = 180000000;

    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);

    IntMasterEnable();
    IntEnable(INT_TIMER0A);

    TimerIntEnable(TIMER0_BASE,
                   TIMER_TIMA_TIMEOUT);

    TimerEnable(TIMER0_BASE, TIMER_A);

    while(1)
    {
        // Si PJ0 esta presionado -> 3 segundos
        if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)
        {
            FS = 360000000;

            TimerLoadSet(TIMER0_BASE,
                         TIMER_A,
                         FS);
        }
        else
        {
            // Sin presionar -> 1,5 segundos
            FS = 180000000;

            TimerLoadSet(TIMER0_BASE,
                         TIMER_A,
                         FS);
        }
    }
}