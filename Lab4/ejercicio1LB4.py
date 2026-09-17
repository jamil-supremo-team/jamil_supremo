#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"
#include "inc/hw_ints.h"

uint32_t tiempo = 120000000 * 1; 

void timer0A_handler(void)
{
    // Limpiar la bandera de interrupción del Timer 0A
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Alternar el estado del LED 1 (PN1)
    int32_t estado = GPIOPinRead(GPIO_PORTN_BASE, GPIO_PIN_1);
    if(estado == 0) {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    } else {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0);
    }
}

int main(void)
{
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);

    // GPIO N y Timer 0
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_TIMER0));

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);

    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE, TIMER_A, tiempo);

    // Vincula tu función timer0A_handler con la interrupción del Timer 0A
    TimerIntRegister(TIMER0_BASE, TIMER_A, timer0A_handler);

    // Inicializar la interrupción del Timer 0A
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    IntEnable(INT_TIMER0A);
    IntMasterEnable();

    // Iniciar el Timer
    TimerEnable(TIMER0_BASE, TIMER_A);

    while(1)
    {
        // La interrupción del Timer 0A se encargará de alternar el estado del LED 1
    }
}