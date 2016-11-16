/*
 * temperature.c
 *
 * Created: 7-11-2016 13:50:49
 *  Author: jouke
 */ 


#include <avr/io.h>
//#include "../../uart/uart.c"
#include <avr/interrupt.h>
//adc0 = temperaturepin

uint8_t getAdcValue();
float getVoltage();
uint8_t getCTemperature();

/**
int main(void)
{
	uart_init(); //set uart at 19200 baud
	_delay_ms(1000);
	setupADC(); //setup adc
	//sei(); //set external interupts
    while(1)
    {
	   transmit(getAdcValue());
	   transmit(getVoltage());
	   transmit(getCTemperature());
	   _delay_ms(1000);
    }
}
**/
//adc0 = temperaturepin
void setupADC(){
	//set AVCC with external capacitor at AREF pin
	//no definition of mux3...0 because 0000 means selecting ADC0
	//datasheet p. 248
	ADMUX = (1 << REFS0) | (1<<ADLAR);
	
	//ADEN = enable ADC
	//ADIE = the ADC Conversion Complete Interrupt is activated.
	//ADPS0 & ADPS1 & ADPS2 1 = prescaler on 128
	//Datasheet p. 250
	ADCSRA = (1 << ADEN) | (1 << ADPS0) | (1 << ADPS1) | (1 << ADPS2);
	
	//Digital input disabled on ADC0
	//DIDR0 = (1 << ADC0D);

	//Start the first conversion
	//startConversion();
}

//Get the voltage
//In mV
uint8_t getAdcValue()
{
	//ADC Start Conversion
	//ADSC will read as one as long as a conversion is in progress. 
	//When the conversion is complete, it returns to zero. 
	//Writing zero to this bit has no effect.
	ADCSRA |= (1 << ADSC);
	loop_until_bit_is_clear(ADCSRA,ADSC);
	
	return ADCH;
}

float getVoltage()
{
	//mV * 5v
	//if 3.3 volt is used change this
	float voltage = getAdcValue() * 5.0;
	//convert mV to Voltage
	voltage /= 1024.0;
	
	//voltage results in a number < 1 so don't transmitting this with uart results 0
	//use the getCtemperature function before tranmitting
	
	return voltage;
}

//Get the celcius temperature of voltage
uint8_t getCTemperature(){
	//voltage - 500mV
	//to celcius * 100
	//uint8_t cTemperature = (getVoltage() - 0.5) * 100;
	uint8_t cTemperature = getVoltage() * 100;
	
	return cTemperature;
}