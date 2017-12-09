#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

// Define baud rate
#define USART_BAUDRATE 9600  #Depends on 
#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

volatile unsigned char value;  
/* This variable is volatile so both main and RX interrupt can use it.
It could also be a uint8_t type */

/* Interrupt Service Routine for Receive Complete 
NOTE: vector name changes with different AVRs see AVRStudio -
Help - AVR-Libc reference - Library Reference - <avr/interrupt.h>: Interrupts
for vector names other than USART_RXC_vect for ATmega32 */

ISR(USART_RXC_vect){
 
   value = UDR;             //read UART register into value
}

void USART_Init(void){
   // Set baud rate
   UBRRL = BAUD_PRESCALE;// Load lower 8-bits into the low byte of the UBRR register
   UBRRH = (BAUD_PRESCALE >> 8); 
	 /* Load upper 8-bits into the high byte of the UBRR register
    Default frame format is 8 data bits, no parity, 1 stop bit
  to change use UCSRC, see AVR datasheet*/ 

  // Enable receiver and transmitter and receive complete interrupt 
  UCSRB = ((1<<TXEN)|(1<<RXEN) | (1<<RXCIE));
}


void USART_SendByte(uint8_t u8Data){

  // Wait until last byte has been transmitted
  while((UCSRA &(1<<UDRE)) == 0);

  // Transmit data
  UDR = u8Data;
}

void Led_init(void){
   //outputs, all off
	 DDRC =0xFF;       //set to OUTPUT mode
     PORTC = 0x00;
}

// not being used but here for completeness
// Wait until a byte has been received and return received data 
uint8_t USART_ReceiveByte(){
  while((UCSRA &(1<<RXC)) == 0);
  
  return UDR;
}


int main(void){
   USART_Init();  // Initialise USART
   sei();         // enable all interrupts
   Led_init();    // init LEDs for testing
   
   for(;;){    // Repeat indefinitely
   char val = '5'; 
   val = USART_ReceiveByte(); 
	if(val == 0x37) //ASCII value of 7
		{
			PORTC = 0xFF; 
			_delay_ms(50); 
			PORTC = 0x00; 
			_delay_ms(50); 
			PORTC = 0xFF; 
			_delay_ms(50); 
			PORTC = 0x00; 
			_delay_ms(50); 
			PORTC = 0xFF; 

		}
	else
		{
			PORTC = 0x00;
		}
	         
     USART_SendByte(val);  // send value 
     _delay_ms(250);         
		         // delay just to stop Hyperterminal screen cluttering up    
   }
}
