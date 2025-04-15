// function to read 1.1V reference against AVcc
// return battery voltage in millivolts
// must be individually calibrated for each CPU
// returns: battery voltage in mV

int readVcc(void) {

  int result;

   ADCSRA = (1<<ADEN);  //enable and
   ADCSRA |= (1<<ADPS0) | (1<<ADPS1) | (1<<ADPS2);  // set prescaler to 128

  // set the reference to Vcc and the measurement to the internal 1.1V reference

   ADMUX = (1<<REFS0) | (1<<MUX3) | (1<<MUX2) | (1<<MUX1);
   delay(1); // Wait for ADC and Vref to settle

   ADCSRA |= (1<<ADSC); // Start conversion
   while (bit_is_set(ADCSRA,ADSC)); // wait until done
   result = ADC;
  
   // second time is a charm

   ADCSRA |= (1<<ADSC); // Start conversion
   while (bit_is_set(ADCSRA,ADSC)); // wait until done
   result = ADC;
  
   // must be individually calibrated for EACH BOARD

  result = 1148566UL / (unsigned long)result; //1126400 = 1.1*1024*1000
  return result; // Vcc in millivolts
}
