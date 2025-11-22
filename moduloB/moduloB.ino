// --- LIBRERIE ---
#include <Wire.h>
#include "DHT.h"
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/wdt.h>

// --- CONFIGURAZIONI ---
#define WDT_INTERVAL          8     // Ogni ciclo WDT è 8s
#define TEMP_HUM_CYCLES       4     // Leggi ogni 32s
#define WATER_CYCLES          1     // Leggi ogni 8s
#define WATER_THRESHOLD       10    // Soglia allagamento

// --- PIN ---
#define DHT11_DATA_PIN        6
#define HW038_DATA_PIN        A3
#define LED_BATTERY           11

DHT dht11(DHT11_DATA_PIN, DHT11);

// --- VARIABILI SENSORI ---
float temp, hum;
unsigned short voltage;
byte battery;
bool all;

// --- VARIABILI TIMER ---
volatile byte temp_hum_counter = 0;
volatile byte water_counter = 0;
volatile bool time_to_read_temp_hum = false;
volatile bool time_to_read_water = false;

// --- SETUP ---
void setup() {
  Serial.begin(9600);
  while (!Serial);

  //Imposta la velocità di trasmissione sul modulo Lora
  Serial.println(F("AT+IPR=9600"));
  delay(500);
  Serial.println(F("AT+IPR?"));
  delay(500);

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
      "m" + String(all) + 
      "a" + String(battery)
    );
    time_to_read_temp_hum = false;
  }

  if (time_to_read_water) {
    readWater();
    if (all=1){
      sendData("m" + String(all));
    }
    time_to_read_water = false;
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
  delay(500);
  if (Serial.available()) {
    String rawData = Serial.readStringUntil('\n');  // Legge fino a newline
    Serial.println(rawData);
  }
}

// --- LETTURA TEMPERATURA / UMIDITÀ ---
void readTempHum() {
  temp = dht11.readTemperature();
  hum = dht11.readHumidity();
}

// --- LETTURA ALLAGAMENTO ---
void readWater() {
  int count = 0;
  for (byte i = 0; i < 5; i++) {
    count += (analogRead(HW038_DATA_PIN) >= WATER_THRESHOLD);
    delay(5);
  }

  all = (count >= 3);
}

// --- LETTURA BATTERIA --- //da completare
void readBattery() {        //da completare
  voltage = analogRead(A2); //da completare

  // Percentuale batteria
  if      (voltage < 4600) battery = 0;
  else if (voltage < 4850) battery = 20;
  else if (voltage < 4950) battery = 40;
  else if (voltage < 5000) battery = 60;
  else if (voltage < 5025) battery = 80;
  else                     battery = 100;
}

void powerStateLed(){
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
  water_counter++;

  if (water_counter >= WATER_CYCLES) {
    time_to_read_water = true;
    water_counter = 0;
  }

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
  } while (!time_to_read_temp_hum && !time_to_read_water);
  ADCSRA |= (1 << ADEN);
}
  


