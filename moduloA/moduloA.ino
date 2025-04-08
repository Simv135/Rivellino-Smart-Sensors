#include "Arduino_BMI270_BMM150.h"
#include <Arduino_HS300x.h>
#include <math.h>  // Per isnan()

float x, y, z;
float vibration;
float lastVibration;
bool firstRead = true;
const float soglia = 0.03;

unsigned long lastTime = 0;
float frequency = 0.0;
const unsigned long minInterval = 50;  // Minimo intervallo tra due rilevamenti per 20 Hz

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    while (1);
  }
}

void loop() {
  float vib = accelerometer();
  if (!isnan(vib) && frequency != 0.00 && frequency != 20.00) {
    Serial.print("aa");          // Metri al secondo quadro
    Serial.print(vib, 2);           // m/s2
    Serial.print("ab");          // Frequenza oscillazioni
    Serial.print(frequency, 2);   //  Hz
  }
  Serial.print("ac");
  Serial.print(HS300x.readTemperature()); 
  Serial.print("ad");
  Serial.print(HS300x.readHumidity()); 
  Serial.println();
}

float accelerometer() {
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    
    // Calcola la norma del vettore di accelerazione (m/s²)
    vibration = sqrt(x * x + y * y + z * z);

    if (firstRead || abs(vibration - lastVibration) >= soglia) {
      unsigned long currentTime = millis();
      unsigned long deltaTime = currentTime - lastTime;
      
      if (!firstRead) {
        // Se il deltaTime è maggiore di minInterval (50 ms per 20 Hz), calcola la frequenza
        if (deltaTime >= minInterval) {
          frequency = 1000.0 / deltaTime;  // Converti in Hertz (ms → s)
        } else {
          // Se il tempo tra due letture è troppo breve, ignoriamo il dato
          return NAN;
        }
      }
      
      lastTime = currentTime;
      lastVibration = vibration;
      firstRead = false;
      return vibration;  // La vibrazione è ora espressa in m/s²
    }
  }
  return NAN;  // Non ritorna nulla se la soglia non è superata
}
