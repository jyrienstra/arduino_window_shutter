/*
 * temperature.c
 *
 * Created: 7-11-2016 13:50:49
 *  Author: jouke
 */ 


#include <avr/io.h>
#include "../../uart/uart.c"
#include <avr/interrupt.h>
//adc0 = temperaturepin

double temperature = 0;

int main(void)
{
	
	uart_init(); //set uart at 19200 baud
	_delay_ms(1000);
	setupADC(); //setup adc
	sei(); //set external interupts
    while(1)
    {
       transmit(temperature);
	   _delay_ms(1000);
	  
    }
}

//adc0 = temperaturepin
void setupADC(){
	//set AVCC with external capacitor at AREF pin
	//no definition of mux3...0 because 0000 means selecting ADC0
	//datasheet p. 248
	ADMUX = (1 << REFS0);
	
	//ADEN = enable ADC
	//ADIE = the ADC Conversion Complete Interrupt is activated.
	//ADPS0 & ADPS1 & ADPS2 1 = prescaler on 128
	//Datasheet p. 250
	ADCSRA = (1 << ADEN) | (1 << ADIE) | (1 << ADPS0) || (1 << ADPS1) || (1 << ADPS2);
	
	//Digital input disabled on ADC0
	DIDR0 = (1 << ADC0D);

	//Start the first conversion
	startConversion();
}

void startConversion()
{
	//ADC Start Conversion
	//ADSC will read as one as long as a conversion is in progress. 
	//When the conversion is complete, it returns to zero. 
	//Writing zero to this bit has no effect.
	ADCSRA |= (1 << ADSC);
}

//handling adc interupts
//ADC0 = temperaturepin
ISR(ADC_vect)
{
	temperature = ADC; //read analoge output in variable
	startConversion(); //start conversion again
}