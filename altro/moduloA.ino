#include "Arduino_BMI270_BMM150.h"
#include <Arduino_HS300x.h>
#include <math.h>  // Per isnan()

// Identificativo modulo
const char* modulo = "a";

// VIBRAZIONI
float x, y, z;
float vibration;
float lastVibration;
bool firstRead = true;
const float soglia = 0.03;

// FREQUENZA
unsigned long lastTime = 0;
float frequency = 0.0;
const unsigned long minInterval = 50;  // intervallo minimo per 20 Hz

// TEMPERATURA / UMIDITÀ
unsigned long lastEnvRead = 0;
const unsigned long envInterval = 5000;  // ogni 5 secondi

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    while (1);  // Blocco se IMU non funziona
  }

  HS300x.begin();  // Sensore temperatura/umidità
}

void loop() {
  float vib = accelerometer();

  // VIBRAZIONE + FREQUENZA
  if (!isnan(vib) && frequency != 0.00 && frequency != 20.00) {
    Serial.print(modulo);
    Serial.print(",vibrazione,");
    Serial.print(vib, 2);       // m/s²
    Serial.print(",");
    Serial.println(frequency, 2); // Hz
  }

  // TEMPERATURA + UMIDITÀ
  unsigned long currentMillis = millis();
  if (currentMillis - lastEnvRead >= envInterval) {
    lastEnvRead = currentMillis;

    float temp = HS300x.readTemperature();
    float hum = HS300x.readHumidity();

    if (!isnan(temp) && !isnan(hum)) {
      Serial.print(modulo);
      Serial.print(",ambiente,");
      Serial.print(temp, 2);
      Serial.print(",");
      Serial.println(hum, 2);
    }
  }
}

// Calcolo vibrazione e frequenza con l'accelerometro
float accelerometer() {
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    vibration = sqrt(x * x + y * y + z * z);

    if (firstRead || abs(vibration - lastVibration) >= soglia) {
      unsigned long currentTime = millis();
      unsigned long deltaTime = currentTime - lastTime;

      if (!firstRead && deltaTime >= minInterval) {
        frequency = 1000.0 / deltaTime;
      } else if (!firstRead) {
        return NAN;
      }

      lastTime = currentTime;
      lastVibration = vibration;
      firstRead = false;
      return vibration;
    }
  }
  return NAN;
}
