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
    // enciende el puerto N y espera a que este listo

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    // configura los 2 leds de usuario (PN0 y PN1) como salida

    uint8_t contador = 0;
    // variable que guarda el numero actual de la secuencia (0, 1, 2, 3)

    while(1)
    {
        if (contador == 0)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
            // 0 en binario es 00, ambos leds apagados
        }
        else if (contador == 1)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
            // 1 en binario es 01, solo prende PN0
        }
        else if (contador == 2)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
            // 2 en binario es 10, solo prende PN1
        }
        else if (contador == 3)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
            // 3 en binario es 11, ambos leds prendidos
        }

        SysCtlDelay(80000000);
        // espera 2 segundos (el doble que tu ejemplo original, que esperaba 1 segundo con 40000000)

        contador++;
        // pasa al siguiente numero

        if (contador > 3)
        {
            contador = 0;
        }
        // si se paso de 3, vuelve a 0 (porque con 2 leds solo hay 4 combinaciones posibles: 0,1,2,3)
    }
}



//nota para hacer algo dentro del while o dentro del bucle si o si tenemos que comentar la interrupcion si no la vamos a usar no se porque 
//sucedera eso eso hay que preguntar pero para que funcione hay que comentar el startup /home/nico/Documentos/Texas/Tivaware/examples/boards/ek-tm4c1294xl/labo3/startup_gcc.c 
//en esta ruta y comentar el nombre de la interrupcion que usaremos si no no funciona 