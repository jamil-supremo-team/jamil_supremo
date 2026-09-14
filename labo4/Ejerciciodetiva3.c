#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"


#ifdef DEBUG
void //bucle anti errores
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif

int
main(void)
{
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);
    // configura el reloj del sistema a 120 MHz 

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }
    // enciende el puerto N (leds) y espera a que este listo

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
    {
    }
    // enciende el puerto J (interruptor) y espera a que este listo
    // NUEVO respecto al ejercicio anterior

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    // configura los 2 leds de usuario como salida

    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
    // configura el interruptor de usuario SW1 (PJ0) como entrada, con pull-up
    // NUEVO respecto al ejercicio anterior

    uint8_t contador = 0;
    uint32_t tiempo_espera = 40000000;
    // NUEVO: variable que guarda cuanto se debe esperar, empieza en 1 segundo

    while(1)
    {
        if (contador == 0)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
        }
        else if (contador == 1)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
        }
        else if (contador == 2)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
        }
        else if (contador == 3)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
        }

        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)
        {
            tiempo_espera = 20000000;
            // NUEVO: si el interruptor esta presionado (0, por el pull-up),
            // el intervalo pasa a 0.5 segundos
        }
        else
        {
            tiempo_espera = 40000000;
            // NUEVO: si NO esta presionado, el intervalo es de 1 segundo
        }

        SysCtlDelay(tiempo_espera);
        // espera el tiempo que corresponda segun el interruptor

        contador++;

        if (contador > 3)
        {
            contador = 0;
        }
    }
}