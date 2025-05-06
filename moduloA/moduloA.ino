#include "Arduino_BMI270_BMM150.h"
#include <Arduino_HS300x.h>
#include <math.h>  // Per fabs() e isnan()

// Costanti di configurazione
#define VIBRATION_THRESHOLD 0.03            // Soglia variazione accelerazione per stampare
#define VIBRATION_MIN_INTERVAL 50           // Minimo tempo tra rilevazioni valide (ms)
#define ENV_INTERVAL 5000                   // Intervallo lettura temperatura/umidità (ms)

// Variabili vibrazione
float x, y, z;
float vibration = 0.0;
float lastVibration = 0.0;
float lastPrintedVibration = 0.0;
float lastPrintedFrequency = 0.0;
bool firstRead = true;

// Variabili frequenza
unsigned long lastTime = 0;
unsigned long currentTime = 0;
unsigned long deltaTime = 0;
float frequencyVibration = 0.0;

// Timer temperatura/umidità
unsigned long lastEnvRead = 0;
unsigned long currentMillis = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("[A] Errore inizializzazione IMU!");
    while (1);
  }

  if (!HS300x.begin()) {
    Serial.println("[A] Errore inizializzazione sensore HS300x!");
    while (1);
  }
}

void loop() {
  currentMillis = millis();

  if (readAccelerometer()) {
    // Filtro per stampare solo se:
    // - la vibrazione è cambiata significativamente
    // - la frequenza è cambiata abbastanza da evitare ripetizioni inutili
    // - deltaTime non è esattamente il minimo (50 ms), per evitare falsi 20 Hz
    if (fabs(vibration - lastPrintedVibration) >= VIBRATION_THRESHOLD &&
        fabs(frequencyVibration - lastPrintedFrequency) >= 0.5 &&
        deltaTime != VIBRATION_MIN_INTERVAL &&
        frequencyVibration > 0.0 && frequencyVibration < 100.0)
    {
      printVibrationData();
      lastPrintedVibration = vibration;
      lastPrintedFrequency = frequencyVibration;
    }
  }

  if (currentMillis - lastEnvRead >= ENV_INTERVAL) {
    lastEnvRead = currentMillis;
    printTempHumData();
  }
}

// Funzione per lettura accelerometro e calcolo frequenza
bool readAccelerometer() {
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    vibration = sqrt(x * x + y * y + z * z);  // Magnitudo accelerazione

    if (firstRead || fabs(vibration - lastVibration) >= VIBRATION_THRESHOLD) {
      currentTime = millis();
      deltaTime = currentTime - lastTime;

      if (!firstRead && deltaTime >= VIBRATION_MIN_INTERVAL) {
        frequencyVibration = 1000.0 / deltaTime;
      }

      lastTime = currentTime;
      lastVibration = vibration;
      firstRead = false;
    }
  }

  return (!isnan(vibration) && frequencyVibration > 0.0 && frequencyVibration < 100.0);
}

// Stampa dati vibrazione
void printVibrationData() {
  Serial.print("k");  // Frequenza (Hz)
  Serial.print(frequencyVibration, 2);
  Serial.print("l");  // Intensità vibrazione (m/s²)
  Serial.println(vibration, 2);
}

// Stampa temperatura e umidità
void printTempHumData() {
  Serial.print("c");  // Temperatura
  Serial.print(HS300x.readTemperature());
  Serial.print("f");  // Umidità
  Serial.println(HS300x.readHumidity());
}
