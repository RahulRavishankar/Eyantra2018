#define F_CPU 14745600
#include<avr/io.h>
#include<avr/interrupt.h>
#include<util/delay.h>

void port_init()
{ 
 DDRB=DDRB | 0x20;
 PORTB=PORTB | 0x20;
 }
void timer_init()
{ TCCR1A=0x00;
  ICR1=1023;
  TCNT1H=0xFC;
  TCNT1L=0x01;
  OCR1A=1023;
  TCCR1A=OxAB;
  
 } 
 
 void servo(unsigned char degrees)
 {
  float regval=((float)degrees*0.512)+34.56;
  OCR1A=(uint16_t)regval;
 }
 void servo_free()
 { OCR1A=1023;}
 
void init()
{cli();
 port_init();
 timer1_init();
 sei();
 }
 int main()
 { 
   init(); 
   servo(45); //servo(135);
   _delay_ms(3000);
   servo(90); //servo(180);
   while(1); 
   
   return 0;
 }
 
 
 
 
 
 
 