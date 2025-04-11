#include "Arduino_BMI270_BMM150.h"
#include <Arduino_HS300x.h>
#include <math.h>  // Per isnan()

//MISURA VIBRAZIONI
float x, y, z;
float vibration;
float lastVibration;
bool firstRead = true;
const float soglia = 0.03;
//MISURA FREQUENZA VIBRAZIONI
unsigned long lastTime = 0;
float frequency = 0.0;
const unsigned long minInterval = 50;  // Minimo intervallo tra due rilevamenti per 20 Hz

//TIMER TEMPERATURA E UMIDITA'
unsigned long lastEnvRead = 0;
const unsigned long envInterval = 5000;  // misura temperatura ogni 5 secondi

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    while (1);
  }
  HS300x.begin();  // Inizializza il sensore di temperatura/umidità
}

void loop() {
  //LETTURA VIBRAZIONI
  float vib = accelerometer();
  if (!isnan(vib) && frequency != 0.00 && frequency != 20.00) {
    Serial.print("aa");
    Serial.print(vib, 2);           // m/s²
    Serial.print("ab");
    Serial.print(frequency, 2);     // Hz
  }

  //LETTURA TEMPERATURA
  unsigned long currentMillis = millis();
  if (currentMillis - lastEnvRead >= envInterval) {
    lastEnvRead = currentMillis;

    Serial.print("ac");
    Serial.print(HS300x.readTemperature()); // °C
    Serial.print("ad");
    Serial.print(HS300x.readHumidity());    // %
    Serial.println();
  }
}

//ACCELLEROMETRO MISURA VIBRAZIONI
float accelerometer() {
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    
    // Calcola la norma del vettore di accelerazione (m/s²)
    vibration = sqrt(x * x + y * y + z * z);

    if (firstRead || abs(vibration - lastVibration) >= soglia) {
      unsigned long currentTime = millis();
      unsigned long deltaTime = currentTime - lastTime;
      
      if (!firstRead) {
        if (deltaTime >= minInterval) {
          frequency = 1000.0 / deltaTime;  // Hz
        } else {
          return NAN;
        }
      }

      lastTime = currentTime;
      lastVibration = vibration;
      firstRead = false;
      return vibration;
    }
  }
  return NAN;
}
