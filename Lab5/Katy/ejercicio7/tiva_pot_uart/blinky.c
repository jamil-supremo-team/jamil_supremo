#include <stdint.h>
#include <stdbool.h>

#include "inc/tm4c1294ncpdt.h"
#include "inc/hw_memmap.h"

#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/adc.h"


uint32_t leerADC(void)
{
    uint32_t valorADC;

    ADCProcessorTrigger(ADC0_BASE, 3);

    while(!ADCIntStatus(ADC0_BASE, 3, false))
    {
    }

    ADCSequenceDataGet(ADC0_BASE, 3, &valorADC);

    ADCIntClear(ADC0_BASE, 3);

    return valorADC;
}


int main(void)
{
    // ---------------- RELOJ ----------------

    SysCtlClockFreqSet(
        SYSCTL_XTAL_25MHZ |
        SYSCTL_OSC_MAIN |
        SYSCTL_USE_PLL |
        SYSCTL_CFG_VCO_480,
        120000000
    );


    // ---------------- UART0 ----------------

    SYSCTL_RCGCUART_R |= 0x01;
    SYSCTL_RCGCGPIO_R |= 0x01;

    while((SYSCTL_PRUART_R & 0x01) == 0)
    {
    }

    while((SYSCTL_PRGPIO_R & 0x01) == 0)
    {
    }

    GPIO_PORTA_AHB_AFSEL_R |= 0x03;
    GPIO_PORTA_AHB_DEN_R |= 0x03;
    GPIO_PORTA_AHB_AMSEL_R &= ~0x03;

    GPIO_PORTA_AHB_PCTL_R =
        (GPIO_PORTA_AHB_PCTL_R & ~0x000000FF) | 0x00000011;

    UART0_CTL_R &= ~0x01;

    UART0_CC_R = 0x05;

    UART0_IBRD_R = 104;
    UART0_FBRD_R = 11;

    UART0_LCRH_R = 0x60;

    UART0_CTL_R = 0x301;


    // ---------------- ADC0 ----------------

    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_ADC0))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOK))
    {
    }

    GPIOPinTypeADC(GPIO_PORTK_BASE, GPIO_PIN_3);//cambiar  el numero 3 si es PK2

    ADCClockConfigSet(
        ADC0_BASE,
        ADC_CLOCK_SRC_PIOSC | ADC_CLOCK_RATE_HALF,
        1
    );

    ADCSequenceDisable(ADC0_BASE, 3);

    ADCSequenceConfigure(
        ADC0_BASE,
        3,
        ADC_TRIGGER_PROCESSOR,
        0
    );

    ADCSequenceStepConfigure(
        ADC0_BASE,
        3,
        0,
        ADC_CTL_CH19 | ADC_CTL_IE | ADC_CTL_END //Cambiar CHANEL(19)
    );

    ADCSequenceEnable(ADC0_BASE, 3);

    ADCIntClear(ADC0_BASE, 3);


    // ---------------- PROGRAMA ----------------

    while(1)
    {
        uint32_t valorADC = leerADC();

        uint32_t porcentaje = (valorADC * 100) / 4095;

        while(UART0_FR_R & 0x20) //bit5 = 32 decimales
        {
        }

        UART0_DR_R = porcentaje;

        SysCtlDelay(20000000); //0.5 segundos vuelve
    }
}