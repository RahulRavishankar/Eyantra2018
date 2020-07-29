int main(void)
{ init_devices();
  lcd_set_4bit();
  lcd_init();
  THRESHOLD=
  velocity(VELOCITY_MAX,VELOCITY_MAX);
  forward();
  while(1)
  { Left_white_line = ADC_Conversion(3);
    Center_white_line=ADC_Conversion(4);
	Right_white_line= ADC_Conversion(5);
	
	//print_sensor(1,1,3);
	//print_sensor(1,5,4);
	//print_sensor(1,9,5);
	
	if(Left_white_line<=THRESHOLD && Center_white_line <=THRESHOLD && Right_white_line>=THRESHOLD)
	 { velocity(250,200);}
	if(Left_white_line<=THRESHOLD && Center_white_line >=THRESHOLD && Right_white_line>=THRESHOLD)
	 { velocity(250,220);}
	if(Left_white_line<=THRESHOLD && Center_white_line >=THRESHOLD && Right_white_line<=THRESHOLD)
	 { velocity(250,250);}
    if(Left_white_line>=THRESHOLD && Center_white_line <=THRESHOLD && Right_white_line<=THRESHOLD)
	 { velocity(200,250);}	 
	if(Left_white_line>=THRESHOLD && Center_white_line >=THRESHOLD && Right_white_line<=THRESHOLD)
	 { velocity(220,250);}
	if(Left_white_line>=THRESHOLD && Center_white_line >=THRESHOLD && Right_white_line>=THRESHOLD)
	 { velocity(0,0);}
	 
	
  }
  
  
  
  
  
}