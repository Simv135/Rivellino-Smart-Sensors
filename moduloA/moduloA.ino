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
    Serial.println("Errore inizializzazione IMU!");
    while (1);
  }

  if (!HS300x.begin()) {
    Serial.println("Errore inizializzazione sensore HS300x!");
    while (1);
  }
}

vuoto ciclo di ciclo() {
 currentMillis = millis();

  se (leggiAccelerometro()) {
    // Filtro per stampare solo se:
    // - la vibrazione è cambiata significativamente
    // - la frequenza è cambiata abbondanza da evitare ripetizioni inutili
    // - deltaTime non è esattamente il minimo (50 ms), per evitare falsi 20 Hz
    se (fabs(vibrazione - lastPrintedVibration) >= VIBRAZIONE_SOGLIA E
        fabs(frequenzaVibrazione - lastPrintedFrequenza) >= 0,5 &&
 deltaTime!= VIBRATION_MIN_INTERVAL & &
 frequenzaVibrazione > 0,0 & frequenzaVibrazione < 100,0)
    {
      printVibrationData();
 lastPrintedVibration = vibrazione;
 lastPrintedFrequenza = frequenzaVibrazione;
    }
  }

  se (currentMillis - lastEnvLeggi >= ENV_INTERVAL) {
 lastEnvLeggi = currentMillis;
    printEnvData();
  }
}

// Funzione per lettura accelerometro e calcio frequente
bool leggiAccelerometro() {
  se (IMU.accelerazioneDisponibile()) {
 IMU.leggiAccelerazione(x, y, z);
 vibrazione = sqrt(x * x + y * y + z * z);  //Accelerazione magnitudo

    se (primaLeggi || fabs(vibrazione - lastVibration) >= VIBRATION_THRESHOLD) {
 currentTime = millis();
 deltaTime = currentTime - lastTime;

      se (!primaLeggi e deltaTime >= VIBRATION_MIN_INTERVAL) {
 frequenzaVibrazione = 1000,0 / deltaTime;
      }

 lastTime = currentTime;
 lastVibration = vibrazione;
 primaLeggi = falso;
    }
  }

  ritorno (!isnan(vibrazione) & frequenzaVibrazione > 0,0 & frequenzaVibrazione < 100,0);
}

// Stampa dati vibrazione
vuoto printVibrationData() {
 Serial.stampa("k");  // Frequenza (Hz)
 Serial.stampa(frequenzaVibrazione, 2);
 Serial.stampa("l");  // Intensità vibrazione (m/s²)
 Serial.stampa(vibrazione, 2);
 Serial.stampa();
}

// Stampa temperatura e umidità
vuoto printEnvData() {
 Serial.stampa("c");  // Temperatura
 Serial.stampa(HS300x.readTemperature());
 Serial.stampa("f");  //Umidità
 Serial.stampa(HS300x.leggiUmidità());
 Serial.stampa();
}
