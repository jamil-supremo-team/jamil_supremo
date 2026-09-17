#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"

int main(void) {
    // Configuración del clock a 120 MHz
    uint32_t g_ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                                 SYSCTL_OSC_MAIN |
                                                 SYSCTL_USE_PLL |
                                                 SYSCTL_CFG_VCO_480), 120000000);

    // Habilitar puertos N y F
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF));

    // Configuracion de  pines 
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4);

    while(1) {
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        SysCtlDelay(g_ui32SysClock / 3); 

      
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
        SysCtlDelay(g_ui32SysClock / 3);

        
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x00);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x00);
        SysCtlDelay(g_ui32SysClock / 3);

        
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x00);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x00);
        SysCtlDelay(g_ui32SysClock / 3);
    }
}
