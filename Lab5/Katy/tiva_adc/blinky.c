#include <stdint.h>
#include <stdbool.h>

#include "inc/tm4c1294ncpdt.h"
#include "inc/hw_memmap.h"

#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/adc.h"

volatile uint32_t estado = 0;

void Timer0A_Handler(void)
{
   
    TIMER0_ICR_R = 0x01;

    GPIO_PORTN_DATA_R &= ~0x03;      
    GPIO_PORTF_AHB_DATA_R &= ~0x10;  

    if(estado == 0)
    {
        GPIO_PORTN_DATA_R |= 0x02;   
        estado = 1;
    }
    else if(estado == 1)
    {
        GPIO_PORTN_DATA_R |= 0x01;    
        estado = 2;
    }
    else
    {
        GPIO_PORTF_AHB_DATA_R |= 0x10; 
        estado = 0;
    }
}
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
    SysCtlClockFreqSet(
        SYSCTL_XTAL_25MHZ |
        SYSCTL_OSC_MAIN |
        SYSCTL_USE_PLL |
        SYSCTL_CFG_VCO_480,
        120000000
        );
    // ---------------- LEDs ----------------

    SYSCTL_RCGCGPIO_R |= (1 << 12);   
    SYSCTL_RCGCGPIO_R |= (1 << 5);    

    while((SYSCTL_PRGPIO_R & (1 << 12)) == 0)
    {
    }

    while((SYSCTL_PRGPIO_R & (1 << 5)) == 0)
    {
    }

    GPIO_PORTN_DIR_R |= 0x03;
    GPIO_PORTN_DEN_R |= 0x03;

    GPIO_PORTF_AHB_DIR_R |= 0x11;
    GPIO_PORTF_AHB_DEN_R |= 0x11;

    GPIO_PORTN_DATA_R &= ~0x03;
    GPIO_PORTF_AHB_DATA_R &= ~0x11; 

    GPIO_PORTN_DATA_R &= ~0x02;


    // ---------------- UART0 ----------------
    // Habilitar UART0 y GPIOA
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

    // ---------------- ADC0 - POTENCIOMETRO ----------------

    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);


    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_ADC0))
    {
    }

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOK))
    {
    }

    GPIOPinTypeADC(GPIO_PORTK_BASE, GPIO_PIN_3);

   
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
        ADC_CTL_CH19 | ADC_CTL_IE | ADC_CTL_END
    );

    ADCSequenceEnable(ADC0_BASE, 3);

    ADCIntClear(ADC0_BASE, 3);

// ---------------- TIMER 0A ----------------

SYSCTL_RCGCTIMER_R |= 0x01;

while((SYSCTL_PRTIMER_R & 0x01) == 0)
{
}

TIMER0_CTL_R &= ~0x01;

TIMER0_CFG_R = 0x00;

TIMER0_TAMR_R = 0x02;


TIMER0_TAILR_R = 120000000 - 1;

TIMER0_ICR_R = 0x01;

TIMER0_IMR_R |= 0x01;

NVIC_EN0_R |= (1 << 19);


TIMER0_CTL_R |= 0x01;

uint32_t ultimoSegundos = 0;

    while(1)
    {
        uint32_t valorADC = leerADC();

        uint32_t segundos = 1 + ((valorADC * 4) / 4095);
    
        if(segundos != ultimoSegundos)
         {
            // Detener Timer0
            TIMER0_CTL_R &= ~0x01;

            TIMER0_TAILR_R = (reloj * segundos) - 1;
            
            TIMER0_ICR_R = 0x01;

            TIMER0_CTL_R |= 0x01;

            ultimoSegundos = segundos;
        }
    }
}