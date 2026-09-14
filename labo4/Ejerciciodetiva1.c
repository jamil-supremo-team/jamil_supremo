#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"

uint32_t FS = 120000000;// tiempo de carga del timer, empieza en 1 segundo 120Mhz //par 2 segundos $120,000,000 \times 2 = 240,000,000$
//para 5 segundos $120,000,000 \times 5 = 600,000,000

#ifdef DEBUG
void //bucle anti errores
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif

void timer0A_handler(void);
// declaramos el handler ANTES de main, igual que en tu ejemplo,
// para poder usarlo mas abajo aunque este definido despues

uint8_t led_state = 0;// guarda si el led esta prendido (1) o apagado (0)

int main(void)
{
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);
    // configura el reloj del sistema, igual que siempre

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }
    // enciende el puerto N y espera a que este listo

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    // configura PN1 como salida, para el led

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    // habilita el periferico del timer0

    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    // configura el timer como periodico (se repite solo)

    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
    // carga el tiempo de conteo (1 segundo, segun el valor de FS)








    IntMasterEnable();
    // habilita las interrupciones en general

    IntEnable(INT_TIMER0A);
    // habilita la interrupcion especifica del timer0

    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    // habilita que el timer SI dispare la interrupcion al terminar de contar

    TimerEnable(TIMER0_BASE, TIMER_A);
    // arranca el timer

    while(1)
    {
        
    }
    // main ya no hace nada, todo el trabajo lo hace la interrupcion
}

void timer0A_handler(void)
{
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    // limpia la bandera de interrupcion, obligatorio para que no se quede pegada

    if (led_state == 0)
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
        led_state = 1;
    }
    else
    {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
        led_state = 0;
    }
    // esto prende y apaga el led cada vez que se dispara la interrupcion
}