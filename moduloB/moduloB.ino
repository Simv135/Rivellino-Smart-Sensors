#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include "DHT.h"

#define ENV_INTERVAL 5000            // Intervallo lettura (ms)
#define DHT11_VCC_PIN 7              // Pin che alimenta il DHT11
#define DHT11_DATA_PIN 8             // Pin dati del DHT11

// Inizializzazione DHT11
DHT dht11(DHT11_DATA_PIN, DHT11);

// Istanza ADS1115
Adafruit_ADS1X15 ads;

// Variabili Temperatura e umidità
float temp;
float hum;

// Costante R0 per NO2
float R0_NO2 = 20.0;

// Variabili lettura NO2
int16_t no2_raw;
float no2_voltage;
float R_s_NO2;
float ppm_NO2 = 0;

// Variabili timing
unsigned long currentMillis;
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(115200);
  pinMode(DHT11_VCC_PIN, OUTPUT);
  digitalWrite(DHT11_VCC_PIN, LOW); // Tieni spento all'avvio

  ads.begin(); // Inizializza ADS una sola volta
}

void loop() {
  currentMillis = millis();

  if (currentMillis - previousMillis >= ENV_INTERVAL) {
    previousMillis = currentMillis;

    readAirQuality();

    readTempHum();

    printTempHumData();

    printAirData();
  }
}

void readAirQuality() {
  no2_raw = ads.readADC_SingleEnded(1);
  no2_voltage = no2_raw * 6.144 / 32768.0;
  R_s_NO2 = (5.0 - no2_voltage) / no2_voltage * R0_NO2;
  ppm_NO2 = pow((R_s_NO2 / R0_NO2), 1.007) * 6.855;
}

void readTempHum(){
  // Accendi DHT11
  digitalWrite(DHT11_VCC_PIN, HIGH);
  delay(2000); // Attendi stabilizzazione
  dht11.begin();

  // Leggi dati ambiente
  temp = dht11.readTemperature();
  hum = dht11.readHumidity();

  // Spegni DHT11
  digitalWrite(DHT11_VCC_PIN, LOW);
}

// Stampa temperatura e umidità
void printTempHumData() {
  Serial.print("c");  // Temperatura
  Serial.print(temp);
  Serial.print("f");  // Umidità
  Serial.println(hum);
}

void printAirData(){
  Serial.print("j");
  Serial.println(ppm_NO2);
}
