#define UPDATE_INTERVAL 5000  // Tempo di aggiornamento in millisecondi

unsigned long lastUpdate = 0;

// Variabili dinamiche
int batB, batC;
int tempA, tempB, tempC;
int humA, humB, humC;
float CO, NO2;
float Hz, ms2;
int all;

void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0)); // Inizializza il generatore di numeri casuali
}

void loop() {
  if (millis() - lastUpdate >= UPDATE_INTERVAL) {
    lastUpdate = millis();
    updateValues();
    printData();
  }
}

void updateValues() {
  // Aggiorna i valori con range realistici
  batB = random(60, 70);
  batC = random(55, 65);

  tempA = random(20, 30);
  tempB = random(20, 30);
  tempC = random(20, 30);

  humA = random(40, 60);
  humB = random(40, 60);
  humC = random(40, 60);

  CO = random(5, 10) / 100.0;  // 0.05 - 0.10
  NO2 = random(3, 8) / 100.0;  // 0.03 - 0.08

  Hz = random(150, 180) / 10.0; // 15.0 - 18.0
  ms2 = random(10, 20) / 10.0;  // 1.0 - 2.0

  all = random(0, 2); // 0 o 1
}

void printData() {
  //moduloA
  Serial.print("c");
  Serial.print(tempA);
  Serial.print("f");
  Serial.print(humA);

  Serial.print("k");
  Serial.print(Hz, 1);
  Serial.print("l");
  Serial.print(ms2, 1);

  Serial.print("i");
  Serial.println(CO, 2);

  //moduloB

  Serial.print("a");
  Serial.print(batB);

  Serial.print("d");
  Serial.print(tempB);
  Serial.print("g");
  Serial.print(humB);

  Serial.print("j");
  Serial.print(NO2, 2);

  Serial.print("m");
  Serial.println(all);

  //moduloC

  Serial.print("b");
  Serial.print(batC);

  Serial.print("e");
  Serial.print(tempC);
  Serial.print("h");
  Serial.println(humC);
}
