#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"

int main(void) {
    uint32_t g_ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                                 SYSCTL_OSC_MAIN |
                                                 SYSCTL_USE_PLL |
                                                 SYSCTL_CFG_VCO_480), 120000000);

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

    int state = 0;

    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0x00);
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0x00);
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);

    while(1) {
        
        if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
            SysCtlDelay(g_ui32SysClock / 30);
            if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
                state = (state + 1) % 4; 

        
                GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0x00);
                GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0x00);

                
                switch(state) {
                    case 0:
                        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1); 
                        break;
                    case 1:
                        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0); 
                        break;
                    case 2:
                        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4); 
                        break;
                    case 3:
                        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0); 
                        break;
                }

                while(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0); 
            }
        }

        
        if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
            SysCtlDelay(g_ui32SysClock / 30); 
            if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
                state = (state - 1 + 4) % 4; 

                
                GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0x00);
                GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0x00);

        
                switch(state) {
                    case 0:
                        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1); 
                        break;
                    case 1:
                        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0); 
                        break;
                    case 2:
                        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
                        break;
                    case 3:
                        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0); 
                        break;
                }

                while(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0); 
            }
        }
    }
}