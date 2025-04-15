#include <Wire.h>
#include <Adafruit_ADS1X15.h>

// Creazione dell'istanza dell'ADS1115
Adafruit_ADS1X15 ads;

// Valori di R0 (resistenza in aria pulita) per ciascun canale
float R0_CO = 10.0;   // Resistenza in aria pulita per CO
float R0_NO2 = 20.0;  // Resistenza in aria pulita per NO2
float R0_NH3 = 15.0;  // Resistenza in aria pulita per NH3

void setup() {
  Serial.begin(9600);
  Serial.println("Avvio Air Quality 5 Click - Calcolo ppm");

  // Inizializza l'ADS1115
  ads.begin();
}

void loop() {
  // Lettura tensioni dai canali ADC
  int16_t co_raw = ads.readADC_SingleEnded(0);
  int16_t no2_raw = ads.readADC_SingleEnded(1);
  int16_t nh3_raw = ads.readADC_SingleEnded(2);

  // Conversione dei valori raw in tensione (V)
  float co_voltage = co_raw * 6.144 / 32768.0;
  float no2_voltage = no2_raw * 6.144 / 32768.0;
  float nh3_voltage = nh3_raw * 6.144 / 32768.0;

  // Calcolo della resistenza del sensore (R_s)
  float R_s_CO = (5.0 - co_voltage) / co_voltage * R0_CO;
  float R_s_NO2 = (5.0 - no2_voltage) / no2_voltage * R0_NO2;
  float R_s_NH3 = (5.0 - nh3_voltage) / nh3_voltage * R0_NH3;

  // Calcolo delle concentrazioni in ppm usando curve empiriche dal datasheet
  float ppm_CO = pow((R_s_CO / R0_CO), -1.179) * 4.385;   // Formula per CO
  float ppm_NO2 = pow((R_s_NO2 / R0_NO2), 1.007) * 6.855; // Formula per NO2
  float ppm_NH3 = pow((R_s_NH3 / R0_NH3), -1.67) * 1.47;  // Formula per NH3

  // Stampa dei risultati sul monitor seriale
  Serial.print("CO: ");
  Serial.print(ppm_CO);
  Serial.print(" ppm");
  Serial.print("   ");

  Serial.print("NO2: ");
  Serial.print(ppm_NO2);
  Serial.print(" ppm");
  Serial.print("   ");

  Serial.print("NH3: ");
  Serial.print(ppm_NH3);
  Serial.println(" ppm");

  delay(1000); // Attesa di un secondo prima della prossima lettura
}
