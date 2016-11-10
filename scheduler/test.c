/*
 * CFile1.c
 *
 * Created: 10-11-2016 22:03:07
 *  Author: jouke
 */ 
#include "scheduler.c"
#include <avr/io.h>
#include <stdio.h>
#define F_CPU 16E6
#include <util/delay.h>

//define ammount of tasks in scheduler.h
uint8_t test;


	//for testing purposes, scheduling LEDs
	//PB0 = LED1
	//PB1 = LED2

void toggleLed1(){
	PORTB ^= 1 << 1;
}

void toggleLed0(){
	PORTB ^= 1 << 0;
}

int main(){
	//set portb as output
	DDRB = 0xFF;
	
	//Scheduler initialisation function.  Prepares scheduler
	//data structures and sets up timer interrupts at required rate.
	//You must call this function before using the scheduler.
	SCH_Init_T1();
	
	
	//16MHz = 16.000.000.000 ticks per second
	//@todo set prescaler so delay can be easyer timed
	//delay is in sch ticks
	
	
	//Causes the function toggleLed0() to be executed regularly, every 10 ticks.
	SCH_Add_Task(toggleLed0, 0, 10);
	
	
	//Causes the function toggleLed1() to be executed regularly, every 100 ticks.
	SCH_Add_Task(toggleLed1, 0, 100);

	//Starts the scheduler, by enabling interrupts.
	SCH_Start();
	
	while(1){
		//This is the 'dispatcher' function.  When a task (function)
		//is due to run, SCH_Dispatch_Tasks() will run it.
		//This function must be called (repeatedly) from the main loop.
		SCH_Dispatch_Tasks();
	}
}
