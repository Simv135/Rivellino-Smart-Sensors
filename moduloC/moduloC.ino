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
