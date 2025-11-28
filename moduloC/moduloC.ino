//Estrarre "libraries.zip" all'interno della cartella "C:\Users\%USERPROFILE%\Documents\Arduino\", riavviare eventualmente Arduino IDE
//impostare usb to ttl con vdd a 5V
//collegare VDD e GND
//collegare tx(usb to ttl) con rx(Arduino) ed rx(usb to ttl) con tx(Arduino)
//premere il pulsante di reset subito dopo la compilazione del codice per caricare il codice sul Pro Mini e non collegare il pin di reset
//Per info: https://github.com/Simv135/Rivellino-Smart-Sensors

// --- LIBRERIE ---
#include <Wire.h>
#include "DHT.h"
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/wdt.h> 

// --- CONFIGURAZIONI ---
#define WDT_INTERVAL          8     // Ogni ciclo WDT è 8s
#define TEMP_HUM_CYCLES       4     // Leggi ogni 32s Temperatura e Umidità

// --- PIN ---
#define DHT11_DATA_PIN        9
#define BATTERY_READ_EN       5
#define BATTERY_READ_PIN      A2
#define LED_BATTERY           11    //da completare il circuito con il LED nel circuito

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
  Serial.begin(9600);
  while (!Serial);

  pinMode(BATTERY_READ_EN,OUTPUT);

  dht11.begin();

  setupWatchdog();

  powerStateLed();  //visualizza stato della batteria partendo dal LED
  //Implementare un pulsante di reset per visualizzare lo stato della batteria manualmente
}

// --- LOOP PRINCIPALE ---
void loop() {
  sleepUntilNextReading();

  if (time_to_read_temp_hum) {
    readTempHum();
    readBattery();
    sendData(
      "e" + String(temp) + 
      "h" + String(hum) + 
      "b" + String(battery)
    );
    time_to_read_temp_hum = false;
  }
}

// --- INVIO DATI ---
void sendData(String data) {
  Serial.println("AT+MODE=0"); //sleep off
  delay(500);

  Serial.print("AT+SEND=1,");
  Serial.print(data.length());
  Serial.print(",");
  Serial.println(data);

  delay(1000);
  Serial.println("AT+MODE=1"); //sleep on
}

// --- LETTURA TEMPERATURA / UMIDITÀ ---
void readTempHum() {
  temp = dht11.readTemperature();
  hum = dht11.readHumidity();
}

// --- LETTURA BATTERIA ---
void readBattery() {
  digitalWrite(BATTERY_READ_EN,HIGH);
  delay(1000);
  voltage = analogRead(BATTERY_READ_PIN);
  digitalWrite(BATTERY_READ_EN,LOW);

  //da calcolare meglio le soglie in base al partitore di tensione nel circuito
  //                   ^
  //                   |
  if      (voltage < 4600) battery = 0;
  else if (voltage < 4850) battery = 20;
  else if (voltage < 4950) battery = 40;
  else if (voltage < 5000) battery = 60;
  else if (voltage < 5025) battery = 80;
  else                     battery = 100;
}

// --- LED BATTERIA ---
//Indicatore LED per lo stato della batteria
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


