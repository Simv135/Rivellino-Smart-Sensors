// --- LIBRERIE ---
#include <Wire.h>
#include "DHT.h"
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/wdt.h>

// --- CONFIGURAZIONI ---
#define WDT_INTERVAL          8     // Ogni ciclo WDT è 8s
#define TEMP_HUM_CYCLES       4     // Leggi ogni 32s

// --- PIN ---
#define DHT11_VCC_PIN         7
#define DHT11_DATA_PIN        8
#define LED_BATTERY           11

DHT dht11(DHT11_DATA_PIN, DHT11);

// --- VARIABILI SENSORI ---
float temp, hum;
unsigned short voltage;
byte battery;

// --- VARIABILI TIMER ---
volatile byte temp_hum_counter = 0;
volatile bool time_to_read_temp_hum = false;

// --- SETUP ---
void setup() {
  pinMode(DHT11_VCC_PIN, OUTPUT);
  digitalWrite(DHT11_VCC_PIN, LOW);

  Serial.begin(9600);
  while (!Serial);

  dht11.begin();

  setupWatchdog();

  powerStateLed();  //visualizza stato della batteria da led
}

// --- LOOP PRINCIPALE ---
void loop() {
  sleepUntilNextReading();

  if (time_to_read_temp_hum) {
    readTempHum();
    readBattery();
    sendData(
      "d" + String(temp) + 
      "g" + String(hum) + 
      "a" + String(battery)
    );
    time_to_read_temp_hum = false;
  }
}

// --- INVIO DATI ---
void sendData(String data) {
  Serial.println(F("AT+MODE=0"));  // Wake
  delay(40);
  Serial.print(F("AT+SEND=1,"));
  Serial.print(data.length());
  Serial.print(",");
  Serial.println(data);
  delay(40);
  Serial.println(F("AT+MODE=1"));  // Sleep
}

// --- LETTURA TEMPERATURA / UMIDITÀ ---
void readTempHum() {
  digitalWrite(DHT11_VCC_PIN, HIGH);
  delay(1000);
  temp = dht11.readTemperature();
  hum = dht11.readHumidity();
  digitalWrite(DHT11_VCC_PIN, LOW);
}

// --- LETTURA BATTERIA ---
void readBattery() {
  ADCSRA = (1 << ADEN) | (1 << ADPS0) | (1 << ADPS1) | (1 << ADPS2);
  ADMUX = (1 << REFS0) | (1 << MUX3) | (1 << MUX2) | (1 << MUX1);
  delay(1);
  ADCSRA |= (1 << ADSC);
  while (bit_is_set(ADCSRA, ADSC));
  int result = ADC;
  ADCSRA |= (1 << ADSC);
  while (bit_is_set(ADCSRA, ADSC));
  result = ADC;

  voltage = 1148566UL / (unsigned long)result; // Vcc stimato

  // Percentuale con correzione errore
  if      (voltage >= 3437 && voltage < 3801) battery = 0;   //0.5 s x1
  else if (voltage >= 3801 && voltage < 4165) battery = 20;  //0.5 s x2
  else if (voltage >= 4165 && voltage < 4529) battery = 40;  //1 s x1
  else if (voltage >= 4529 && voltage < 4893) battery = 60;  //1 s x2
  else if (voltage >= 3893 && voltage < 5075) battery = 80;  //2 s x1
  else if (voltage >= 5075)                   battery = 100; //2 s x2
}
//la misura va da 3,300V + errore a 5080 + errore quindi da 3,437V a 5,258
//L'errore applicato agli estremi dell'intervallo applica un errore empirico ai valori mediani concorde con le misure prese
//intervallo 3,300-5,080V diventa quindi 3,437V a 5,258 ed avendo diametro 1821 si hanno 5 sottointervalli da 364V
//rispettivamente 3,438-3,802-4,166-4,530-4,894-5258, nota: si pone limite a 5075 perchè è il valore oltre cui
//la batteria è oltre il 90% ed è quindi conveniente considerarla come pienamente carica.


void powerStateLed(void){
  readBattery();
  if (battery==0){
    digitalWrite(LED_BATTERY, HIGH);
    delay(500);
    digitalWrite(LED_BATTERY, LOW);
  }else if (battery<=20){
    digitalWrite(LED_BATTERY, HIGH);
    delay(500);
    digitalWrite(LED_BATTERY, LOW);
    delay(500);
    digitalWrite(LED_BATTERY, HIGH);
    delay(500);
    digitalWrite(LED_BATTERY, LOW);
  }else if (battery<=40){
    digitalWrite(LED_BATTERY, HIGH);
    delay(1000);
    digitalWrite(LED_BATTERY, LOW);
  }else if (battery<=60){
    digitalWrite(LED_BATTERY, HIGH);
    delay(1000);
    digitalWrite(LED_BATTERY, LOW);
    delay(1000);
    digitalWrite(LED_BATTERY, HIGH);
    delay(1000);
    digitalWrite(LED_BATTERY, LOW);
  }else if (battery<=80){
    digitalWrite(LED_BATTERY, HIGH);
    delay(2000);
    digitalWrite(LED_BATTERY, LOW);
  }else if (battery<=100){
    digitalWrite(LED_BATTERY, HIGH);
    delay(2000);
    digitalWrite(LED_BATTERY, LOW);
    delay(2000);
    digitalWrite(LED_BATTERY, HIGH);
    delay(2000);
    digitalWrite(LED_BATTERY, LOW);
  }
}

// --- WATCHDOG ---
void setupWatchdog() {
  cli();
  wdt_reset();
  MCUSR &= ~(1 << WDRF);
  WDTCSR |= (1 << WDCE) | (1 << WDE);
  WDTCSR = (1 << WDIE) | (1 << WDP3) | (0 << WDP2) | (0 << WDP1) | (1 << WDP0); // 8s
  sei();
}

ISR(WDT_vect) {
  temp_hum_counter++;

  if (temp_hum_counter >= TEMP_HUM_CYCLES) {
    time_to_read_temp_hum = true;
    temp_hum_counter = 0;
  }
}

// --- SLEEP ---
void sleepUntilNextReading() {
  ADCSRA &= ~(1 << ADEN);
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  do {
    sleep_enable();
    sleep_mode();
    sleep_disable();
  } while (!time_to_read_temp_hum);
  ADCSRA |= (1 << ADEN);
}
