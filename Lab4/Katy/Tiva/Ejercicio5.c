#include <stdint.h>
#include <stdbool.h>

#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"

#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"


uint32_t FS;
uint8_t estado;


void timer0A_handler(void)
{
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Apagar todos los LEDs
    GPIOPinWrite(GPIO_PORTN_BASE,
                 GPIO_PIN_0 | GPIO_PIN_1,
                 0x00);

    GPIOPinWrite(GPIO_PORTF_BASE,
                 GPIO_PIN_0 | GPIO_PIN_4,
                 0x00);

    // Estado 1
    if(estado == 0)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_1,
                     GPIO_PIN_1);
    }

    // Estado 2
    else if(estado == 1)
    {
        GPIOPinWrite(GPIO_PORTN_BASE,
                     GPIO_PIN_0,
                     GPIO_PIN_0);
    }

    // Estado 3
    else
    {
        GPIOPinWrite(GPIO_PORTF_BASE,
                     GPIO_PIN_0 | GPIO_PIN_4,
                     GPIO_PIN_0 | GPIO_PIN_4);
    }

    estado++;

    if(estado > 2)
    {
        estado = 0;
    }
}


int main(void)
{
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                        SYSCTL_OSC_MAIN |
                        SYSCTL_USE_PLL |
                        SYSCTL_CFG_VCO_480),
                        120000000);

    // Habilitar puertos de LEDs
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    // Habilitar Timer0
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_TIMER0));

    // Configurar LEDs como salida
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE,
                          GPIO_PIN_0 | GPIO_PIN_1);

    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE,
                          GPIO_PIN_0 | GPIO_PIN_4);

    // Apagar LEDs inicialmente
    GPIOPinWrite(GPIO_PORTN_BASE,
                 GPIO_PIN_0 | GPIO_PIN_1,
                 0x00);

    GPIOPinWrite(GPIO_PORTF_BASE,
                 GPIO_PIN_0 | GPIO_PIN_4,
                 0x00);

    estado = 0;

    // Intervalo inicial: 1 segundo
    FS = 120000000;

    // Timer periodico
    TimerConfigure(TIMER0_BASE,
                   TIMER_CFG_PERIODIC);

    TimerLoadSet(TIMER0_BASE,
                 TIMER_A,
                 FS);

    // Interrupciones
    IntMasterEnable();

    IntEnable(INT_TIMER0A);

    TimerIntEnable(TIMER0_BASE,
                   TIMER_TIMA_TIMEOUT);

    // Iniciar Timer
    TimerEnable(TIMER0_BASE,
                TIMER_A);

    while(1)
    {

    }
}