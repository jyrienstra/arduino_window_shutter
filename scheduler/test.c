/*
 * CFile1.c
 *
 * Created: 10-11-2016 22:03:07
 *  Author: jouke
 */ 

#include <avr/io.h>
#include <stdio.h>
#define F_CPU 16E6
#include <util/delay.h>
#include "../afstandlezer/ultrasonoor.c"
#include "scheduler.c"
#include "../temperature/temperature/temperature.c"

//define ammount of tasks in scheduler.h

//PB2 = LED1 (ROOD) = uitgerold
//PB3 = LED2 (GROEN) = ingerold
//PB4 = LED3 (GEEL) = bezig met uit- of inrollen
int rood = 2;
int groen = 3;
int geel = 4;

//Define variables
//uint16_t uitgerold_cm = 20; //uitgerolde cm
uint8_t sonoor_cm = 0;
uint8_t max_uitgerold = 4; //bij 4 cm is hij uitgerold
uint8_t min_ingerold = 20; //bij 20cm is hij ingerold
uint8_t temperature = 0;
uint8_t temperature2 = 25;
uint8_t max_temp = 20;
uint8_t min_temp = 10;
uint8_t uitgerold = 0;
uint8_t ingerold = 0;

	
//Als het rolluik is uitgerold brandt er een rood ledlampje. 
void rolluikUitgerold(){
	//set led
	PORTB |= 1 << rood; //uitgerold aan
	PORTB &= ~(1 << groen); //ingerold uit
}

//Als het rolluik is opgerold brandt er een groen ledlampje. 
void rolluikIngerold(){
	//set led
	PORTB |= 1 << groen; //ingerold aan
	PORTB &= ~(1 << rood); //uitgerold uit
}

//Als het rolluik in of uit wordt gerold knippert er een geel ledlampje.
void rolluikRollen(){
	//toggle led
	PORTB ^=1 << geel;
	_delay_ms(150);
}

void sonoor(){
	//dit buggt blijkbaar iets met dat ze allebij interupt gebruiken
	
	/**
	uint16_t cm = 0;
	echo = BEGIN; // set flag
	// start trigger puls lo -> hi
	PORTD |= _BV(4); // set bit D0
	_delay_us(12); // micro sec
	// stop trigger puls hi -> lo
	PORTD &=~ _BV(4); // clear bit D0
	_delay_ms(20); // milli sec, timer1 is read in ISR
	cm = calc_cm(gv_counter);
	int cm_with_key = concat(1, cm);
	transmit(cm_with_key); // Verstuur het aantal cm via UART
	show_distance(cm);
	_delay_ms(500); // milli sec
	**/

}

//krijg de temperatuur en transmit deze via uart naar python
void getTemperature(){
	temperature = getCTemperature(); //get the temperature
	transmit(temperature); //send the temperature trough uart
	_delay_ms(1000);
}

//regelt de simulatie van het uitrollen
//laad bijbehorende ledjes branden
void lampjes(){
	
	
	/**
	//uitgerold defineert wat de waarde is wanneer we een rolluik als "uitgerold" beschauwen bv. 0 = uitgerold 20=ingerold
	//uitgerold_cm is daadwerkelijke cm dat de sonoor uitleest
	if(uitgerold_cm <= uitgerold){
		//voer de functies uit die horen bij een "uitgerold" rolluik
		rolluikUitgerold();
	}
	//ingerold defineert wat de waarde is wanneer we een rolluik als "uitgerold" beschauwen bv. 0 = uitgerold 20=ingerold
	//uitgerold_cm is daadwerkelijke cm dat de sonoor uitleest
	if(uitgerold_cm >= ingerold){
		//voer de functies uit die horen bij een "ingerold" rolluik
		rolluikIngerold();
	}
	**/
	//temperature = de daadwerkelijk temperatuur die wordt uitgelezen
	//max_temp is de maximale temperatuur voordat het scherm wordt uitgerold
	if(temperature2 >= max_temp && uitgerold==0){
		uitgerold = 1;
		ingerold = 0;
		for(int i=0; i<20; i++){
			rolluikRollen();
		}		
		rolluikUitgerold();
	}
	//temperature = de daadwerkelijk temperatuur die wordt uitgelezen
	//min_temp is de minimale temperatuur voordat het scherm wordt ingerold
	if(temperature2 <= min_temp && ingerold==0){
		ingerold = 1;
		uitgerold = 0;
		for(int i=0; i<20; i++){
			rolluikRollen();
		}
		rolluikIngerold();
	}
	
}

int main(){
	// Initialiseert UART zodat gegevens verstuurd kunnen worden
	uart_init(); 
	
	// setup ADC for temperature
	setupADC();
	
	//set register voor ultrasonoor
	init_ports();
	init_timer(); //initaliseer timer voor sonoor
	init_ext_int(); //initaliseer externe interupts
	sei(); //set externe interupt aan
	_delay_ms(50);
	
	//set portb as output
	DDRB = 0xFF;
	//set alle ledjes op b eerst uit
	//@todo even goed checken of dit niet andere code kapot maakt
	PORTB = 0x00;
	
	//bij levering is het rolluik ingerold
	rolluikIngerold();
	ingerold = 1;
	
	//Scheduler initialisation function.  Prepares scheduler
	//data structures and sets up timer interrupts at required rate.
	//You must call this function before using the scheduler.
	SCH_Init_T1();
	
	
	//16MHz = 16.000.000.000 ticks per second
	//@todo set prescaler so delay can be easyer timed
	//delay is in sch ticks
	
	
	//Causes the function toggleLed0() to be executed regularly, every 10 ticks.
	SCH_Add_Task(sonoor, 0, 10);
	SCH_Add_Task(getTemperature, 0, 10);
	SCH_Add_Task(lampjes, 0, 10);
	//SCH_Add_Task(rolluikRollen, 0, 10);
	
	
	//Causes the function toggleLed1() to be executed regularly, every 100 ticks.
	//SCH_Add_Task(toggleLed1, 0, 100);

	//Starts the scheduler, by enabling interrupts.
	SCH_Start();
	
	while(1){
		//This is the 'dispatcher' function.  When a task (function)
		//is due to run, SCH_Dispatch_Tasks() will run it.
		//This function must be called (repeatedly) from the main loop.
		SCH_Dispatch_Tasks();
		//sonoor();
	}
}


