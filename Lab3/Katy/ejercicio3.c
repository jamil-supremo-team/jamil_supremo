#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"

int counter = 0;

int main(void) {
    // Configurar clock 
    uint32_t g_ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                                 SYSCTL_OSC_MAIN |
                                                 SYSCTL_USE_PLL |
                                                 SYSCTL_CFG_VCO_480), 120000000);

    // Habilitar  pines
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ));

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4);

    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, (counter & 0x01) ? GPIO_PIN_1 : 0);
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, (counter & 0x02) ? GPIO_PIN_0 : 0);
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, (counter & 0x04) ? GPIO_PIN_4 : 0);
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, (counter & 0x08) ? GPIO_PIN_0 : 0);

    while(1) {
        
        if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
            SysCtlDelay(g_ui32SysClock / 30); 
            if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
                if(counter < 15) { 
                    counter++;
                    
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, (counter & 0x01) ? GPIO_PIN_1 : 0);
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, (counter & 0x02) ? GPIO_PIN_0 : 0);
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, (counter & 0x04) ? GPIO_PIN_4 : 0);
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, (counter & 0x08) ? GPIO_PIN_0 : 0);
                }
                while(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0); 
            }
        }

        if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
            SysCtlDelay(g_ui32SysClock / 30); 
            if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
                if(counter > 0) { 
                    counter--;
                    
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, (counter & 0x01) ? GPIO_PIN_1 : 0);
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, (counter & 0x02) ? GPIO_PIN_0 : 0);
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, (counter & 0x04) ? GPIO_PIN_4 : 0);
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, (counter & 0x08) ? GPIO_PIN_0 : 0);
                }
                while(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0); 
            }
        }
    }
}
