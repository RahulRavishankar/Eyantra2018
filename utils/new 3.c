#define		THRESHOLD		210     // set the pots such that all three sensor 
                                      // calibrated to show its min value on LCD. 
                                      // i.e on LCD Sensor values are betwn 168 to 172
									  // on black line  
#define		VELOCITY_MAX	50
#define		VELOCITY_MIN	30
#define 	VELOCITY_LOW	0
#define F_CPU 14745600
#include <avr/io.h>
#include <stdbool.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
volatile unsigned long int ShaftCountLeft = 0; //to keep track of left position encoder
volatile unsigned long int ShaftCountRight = 0; //to keep track of right position encoder
volatile unsigned int Degrees; //to accept angle in degrees for turning
#define RX  (1<<4)
#define TX  (1<<3)
#define TE  (1<<5)
#define RE  (1<<7)

volatile unsigned char data;
unsigned char ADC_Conversion(unsigned char);
unsigned char ADC_Value;
unsigned char Left_white_line = 0;
unsigned char Center_white_line = 0;
unsigned char Right_white_line = 0;
int flag=0;
void uart0_init()
{
	UCSR0B = 0x00;							//disable while setting baud rate
	UCSR0A = 0x00;
	UCSR0C = 0x06;
	UBRR0L = 0x5F; 							//9600BPS at 14745600Hz
	UBRR0H = 0x00;
	UCSR0B = 0x98;
	UCSR0C = 3<<1;							//setting 8-bit character and 1 stop bit
	UCSR0B = RX | TX;
}


void uart_tx(char data)
{
	while(!(UCSR0A & TE));						//waiting to transmit
	UDR0 = data;
}

ISR(USART0_RX_vect)
{
	data = UDR0;
}

char uart_rx()
{
	while(!(UCSR0A & RE));						//waiting to receive
	return UDR0;
}



	



void left_encoder_pin_config (void)
{
	DDRE  = DDRE & 0xEF;  //Set the direction of the PORTE 4 pin as input
	PORTE = PORTE | 0x10; //Enable internal pull-up for PORTE 4 pin
}
void right_encoder_pin_config (void)
{
	DDRE  = DDRE & 0xDF;  //Set the direction of the PORTE 4 pin as input
	PORTE = PORTE | 0x20; //Enable internal pull-up for PORTE 4 pin
}
void left_position_encoder_interrupt_init (void) //Interrupt 4 enable
{
	cli(); //Clears the global interrupt
	EICRB = EICRB | 0x02; // INT4 is set to trigger with falling edge
	EIMSK = EIMSK | 0x10; // Enable Interrupt INT4 for left position encoder
	sei();   // Enables the global interrupt
}

void right_position_encoder_interrupt_init (void) //Interrupt 5 enable
{
	cli(); //Clears the global interrupt
	EICRB = EICRB | 0x08; // INT5 is set to trigger with falling edge
	EIMSK = EIMSK | 0x20; // Enable Interrupt INT5 for right position encoder
	sei();   // Enables the global interrupt
}

//ISR for right position encoder
ISR(INT5_vect)
{
	ShaftCountRight++;  //increment right shaft position count
}


//ISR for left position encoder
ISR(INT4_vect)
{
	ShaftCountLeft++;  //increment left shaft position count
}
void motion_pin_config (void)
{
	DDRA = DDRA | 0x0F;
	PORTA = PORTA & 0xF0;
	DDRL = DDRL | 0x18;   //Setting PL3 and PL4 pins as output for PWM generation
	PORTL = PORTL | 0x18; //PL3 and PL4 pins are for velocity control using PWM.
}

//Function used for setting motor's direction
void motion_set (unsigned char Direction)
{
	unsigned char PortARestore = 0;

	Direction &= 0x0F; 		// removing upper nibbel for the protection
	PortARestore = PORTA; 		// reading the PORTA original status
	PortARestore &= 0xF0; 		// making lower direction nibbel to 0
	PortARestore |= Direction; // adding lower nibbel for forward command and restoring the PORTA status
	PORTA = PortARestore; 		// executing the command
}

void forward (void) //both wheels forward
{
	motion_set(0x06);
}

void back (void) //both wheels backward
{
	motion_set(0x09);
}

void left (void) //Left wheel backward, Right wheel forward
{
	velocity(200,200);
	motion_set(0x05);
}

void right (void) //Left wheel forward, Right wheel backward
{
	velocity(200,200);
	motion_set(0x0A);
}

void soft_left (void) //Left wheel stationary, Right wheel forward
{
	motion_set(0x04);
}

void soft_right (void) //Left wheel forward, Right wheel is stationary
{
	motion_set(0x02);
}

void soft_left_2 (void) //Left wheel backward, right wheel stationary
{
	motion_set(0x01);
}

void soft_right_2 (void) //Left wheel stationary, Right wheel backward
{
	motion_set(0x08);
}

void stop (void)
{
	motion_set(0x00);
}
void velocity (unsigned char left_motor, unsigned char right_motor)
{
	OCR5AL = (unsigned char)left_motor;
	OCR5BL = (unsigned char)right_motor;
}


//Function used for turning robot by specified degrees
void angle_rotate(unsigned int Degrees)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = (float) Degrees/ 0.1; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned int) ReqdShaftCount;
	ShaftCountRight = 0;
	ShaftCountLeft = 0;

	while (1)
	{


		if((ShaftCountRight >= ReqdShaftCountInt) | (ShaftCountLeft >= ReqdShaftCountInt))
		{

			break;
		}
	}
	stop(); //Stop robot
}

//Function used for moving robot forward by specified distance

void linear_distance_mm(unsigned int DistanceInMM)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = DistanceInMM / 0.4340; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;

	ShaftCountRight = 0;
	while(1)
	{
		if(ShaftCountRight > ReqdShaftCountInt)
		{
			break;
		}
	}
	stop(); //Stop robot
}



void forward_mm(unsigned int DistanceInMM)
{
	forward();
	linear_distance_mm(DistanceInMM);
}
void back_mm(unsigned int DistanceInMM)
{
	back();
	linear_distance_mm(DistanceInMM);
}

void left_degrees(unsigned int Degrees)
{
	// 88 pulses for 360 degrees rotation 4.090 degrees per count
	left(); //Turn left
	angle_rotate(Degrees);
}



void right_degrees(unsigned int Degrees)
{
	// 88 pulses for 360 degrees rotation 4.090 degrees per count
	right(); //Turn right
	angle_rotate(Degrees);
}


void soft_left_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_left(); //Turn soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_right_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_right();  //Turn soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}
	unsigned char ADC_Conversion(unsigned char Ch)
	{
		unsigned char a;
		if(Ch>7)
		{
			ADCSRB = 0x08;
		}
		Ch = Ch & 0x07;
		ADMUX= 0x20| Ch;
		ADCSRA = ADCSRA | 0x40;		//Set start conversion bit
		while((ADCSRA&0x10)==0);	//Wait for conversion to complete
		a=ADCH;
		ADCSRA = ADCSRA|0x10; //clear ADIF (ADC Interrupt Flag) by writing 1 to it
		ADCSRB = 0x00;
		return a;
	}
	void adc_pin_config (void)
	{
	 DDRF = 0x00;
	 PORTF = 0x00;
	 DDRK = 0x00;
	 PORTK = 0x00;
	}
void adc_init()
	{
		ADCSRA = 0x00;
		ADCSRB = 0x00;		//MUX5 = 0
		ADMUX = 0x20;		//Vref=5V external --- ADLAR=1 --- MUX4:0 = 0000
		ACSR = 0x80;
		ADCSRA = 0x86;		//ADEN=1 --- ADIE=1 --- ADPS2:0 = 1 1 0
	}
	void timer1_init(void)
	{
	 TCCR1B = 0x00; //stop
	 TCNT1H = 0xFC; //Counter high value to which OCR1xH value is to be compared with
	 TCNT1L = 0x01;	//Counter low value to which OCR1xH value is to be compared with
	 OCR1AH = 0x03;	//Output compare Register high value for servo 1
	 OCR1AL = 0xFF;	//Output Compare Register low Value For servo 1
	 OCR1BH = 0x03;	//Output compare Register high value for servo 2
	 OCR1BL = 0xFF;	//Output Compare Register low Value For servo 2
	 OCR1CH = 0x03;	//Output compare Register high value for servo 3
	 OCR1CL = 0xFF;	//Output Compare Register low Value For servo 3
	 ICR1H  = 0x03;
	 ICR1L  = 0xFF;
	 TCCR1A = 0xAB; /*{COM1A1=1, COM1A0=0; COM1B1=1, COM1B0=0; COM1C1=1 COM1C0=0}
	 					For Overriding normal port functionality to OCRnA outputs.
					  {WGM11=1, WGM10=1} Along With WGM12 in TCCR1B for Selecting FAST PWM Mode*/
	 TCCR1C = 0x00;
	 TCCR1B = 0x0C; //WGM12=1; CS12=1, CS11=0, CS10=0 (Prescaler=256)
	}
	void linef(unsigned int DistanceInMM)
	{
		bool s=0;
		
		float ReqdShaftCount = 0;
		unsigned long int ReqdShaftCountInt = 0;

		ReqdShaftCount = DistanceInMM / 5.338; // division by resolution to get shaft count
		ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;
		
		ShaftCountRight = 0;
		while(s!=1)
		{
			s=ShaftCountRight > ReqdShaftCountInt;	 // centre white line sensor sens value
			Left_white_line = ADC_Conversion(3);
			Center_white_line=ADC_Conversion(4);
			Right_white_line= ADC_Conversion(5);
												   

			
			 if( Left_white_line <THRESHOLD && Right_white_line < THRESHOLD && Center_white_line >THRESHOLD && !s ) // if centre white line sensor is on black line than forward bot
			velocity( 255, 255 );
			else if( Center_white_line < THRESHOLD && Right_white_line < THRESHOLD && Left_white_line > THRESHOLD && !s) // if left white line sensor is on black line than stops right wheel and initialze left wheel
			velocity( 0, 255 );
			else if( Center_white_line < THRESHOLD && Left_white_line < THRESHOLD && Right_white_line > THRESHOLD && !s) // if right white line sensor is on black line than stops left wheel and initialze right wheel
			velocity( 255, 0 );
			else if(s==1)
			break;
			
			
		}
		stop();
		velocity(255,255);
	}
	void linef1(void)
	{
		
		while(1)
        { 
	
	      PORTA=0x06;

	 
	 flag=0;

	 if(Center_white_line>THRESHOLD)               // Is middle Whiteline is within threshold limit
	 {                                             
		flag=1;
		velocity(220,220);      // Run robot at max velocity 
		
	 }

	if((Left_white_line<THRESHOLD) && (flag==0))  // Is left Whiteline is not within threshold limit
	//if((Left_white_line>THRESHOLD) && (flag==0))  // Is left Whiteline is not within threshold limit
	{                                             
		flag=1;                       
		velocity(200,0);      // Run robot left wheel at max velocity and right wheel 
		        
	/*	velocity(VELOCITY_MIN,60);      // Run robot right wheel at max velocity and left wheel 
		lcd_print (2,1,VELOCITY_MIN,3);           // at min velocity
		lcd_print (2,5,VELOCITY_MAX,3);*/
	}

	if((Right_white_line<THRESHOLD) && (flag==0)) // Is right Whiteline is not within threshold limit
	//if((Right_white_line>THRESHOLD) && (flag==0)) // Is right Whiteline is not within threshold limit
	{
		flag=1;    
		velocity(0,200);      // Run robot right wheel at max velocity and left wheel 
		
	/*	velocity(60,VELOCITY_MIN);      // Run robot left wheel at max velocity and right wheel 
		lcd_print (2,1,VELOCITY_MAX,3);           // at min velocity
		lcd_print (2,5,VELOCITY_MIN,3);*/
	}

	if(Center_white_line<THRESHOLD && Left_white_line<THRESHOLD && Right_white_line<THRESHOLD && (flag == 0))
	                                // if all Whiteline sensor are not within threshold limit    
	{
		flag=1;
		DDRB=0x01;
		PORTB=0x01;
		velocity(VELOCITY_LOW,VELOCITY_LOW);      // stop the robot
		
	}

		 			 
	 
	
  }
		stop();
		velocity(255,255);
	}
	int blackline(void)
{
	motion_pin_config();
	 timer5_init();
	 adc_pin_config();
 adc_init();
	
	
while(1)
  { Left_white_line = ADC_Conversion(3);
    Center_white_line=ADC_Conversion(2);
	Right_white_line= ADC_Conversion(1);
	
	 PORTA=0x06;

	 
	bool flag=0;

	if(Center_white_line>THRESHOLD)               // Is middle Whiteline is within threshold limit
	{                                             
		flag=1;
		velocity(130,130);      // Run robot at max velocity 
		
	}

	if((Left_white_line>THRESHOLD) )  // Is left Whiteline is not within threshold limit
	//if((Left_white_line>THRESHOLD) && (flag==0))  // Is left Whiteline is not within threshold limit
	{                                             
		flag=1;                       
		velocity(0,130);      // Run robot left wheel at max velocity and right wheel 
		        
	/*	velocity(VELOCITY_MIN,60);      // Run robot right wheel at max velocity and left wheel 
		lcd_print (2,1,VELOCITY_MIN,3);           // at min velocity
		lcd_print (2,5,VELOCITY_MAX,3);*/
	}

	if((Right_white_line>THRESHOLD) )// Is right Whiteline is not within threshold limit
	//if((Right_white_line>THRESHOLD) && (flag==0)) // Is right Whiteline is not within threshold limit
	{
		flag=1;    
		velocity(130,0);      // Run robot right wheel at max velocity and left wheel 
		
	/*	velocity(60,VELOCITY_MIN);      // Run robot left wheel at max velocity and right wheel 
		lcd_print (2,1,VELOCITY_MAX,3);           // at min velocity
		lcd_print (2,5,VELOCITY_MIN,3);*/
	}

	if((Center_white_line>THRESHOLD && Left_white_line>THRESHOLD && Right_white_line>THRESHOLD) )
	                                // if all Whiteline sensor are not within threshold limit    
	{
		flag=1;
		
		velocity(VELOCITY_LOW,VELOCITY_LOW); 
		break;
		
	}

		 			 
	 
	
  }
  






   
	
	 
		
		
	
}

	
	void timer5_init()
	{
		TCCR5B = 0x00;	//Stop
		TCNT5H = 0xFF;	//Counter higher 8-bit value to which OCR5xH value is compared with
		TCNT5L = 0x01;	//Counter lower 8-bit value to which OCR5xH value is compared with
		OCR5AH = 0x00;	//Output compare register high value for Left Motor
		OCR5AL = 0xFF;	//Output compare register low value for Left Motor
		OCR5BH = 0x00;	//Output compare register high value for Right Motor
		OCR5BL = 0xFF;	//Output compare register low value for Right Motor
		OCR5CH = 0x00;	//Output compare register high value for Motor C1
		OCR5CL = 0xFF;	//Output compare register low value for Motor C1
		TCCR5A = 0xA9;	/*{COM5A1=1, COM5A0=0; COM5B1=1, COM5B0=0; COM5C1=1 COM5C0=0}
	 					  For Overriding normal port functionality to OCRnA outputs.
					  	  {WGM51=0, WGM80=1} Along With WGM52 in TCCR5B for Selecting FAST PWM 8-bit Mode*/

		TCCR5B = 0x0B;	//WGM12=1; CS12=0, CS11=1, CS10=1 (Prescaler=64)
	}

int main(void)
{
	
	
	cli();
	 left_encoder_pin_config ();
	 right_encoder_pin_config();
	 adc_pin_config();
	 adc_init();
	 timer1_init();
	 timer5_init();
	 motion_pin_config();
	 
	 
	 
	   right_position_encoder_interrupt_init();
	 left_position_encoder_interrupt_init ();
	 //left_degrees(360);
	

	  sei();
	  
	
	 uart0_init();
	// soft_left_degrees(20);
	
	
	 
	uart_tx('.'); 

	 while(1)
	 {
		 
		 
		 
		 
		 
		 data=uart_rx();
		 

		 
		 if(data=='l')
		 {
	
			  
			soft_left_degrees(20);
			_delay_ms(1000);
			////
			
			blackline();
			
			
			

			/////
			
			
			
			
		
			uart_tx('.');
			_delay_ms(1500);
			continue;
			
			
			
			 
			 
		 }
		 if(data=='r')
		 {
			
			soft_right_degrees(20);
			_delay_ms(1000);
			////
			
			blackline();
			

			/////
		DDRB=0x01;
		PORTB=0x01;
		
			uart_tx('.');
			_delay_ms(1500);
			continue;
			
		
		
			 
			 
		 }
		  if(data=='b')
		  {
			  DDRB =0x01 ;
			  PORTB =0x01 ;
			 
			  _delay_ms(2000);
			    PORTB =0x00 ;
			  uart_tx('.');
			  _delay_ms(50);
		
			  
			  
		  }
		 
	 }

}