void setup() {
  Serial.begin(57600);
  Serial1.begin(57600);
  delay(1000);
}

void loop() {
  receiveData();
  delay(1000);
}

void receiveData() {
  if (Serial1.available()) {
    String rawData = Serial1.readStringUntil('\n');  // Legge fino a newline

    if (rawData.startsWith("+RCV=")) {
      int firstComma = rawData.indexOf(',');
      int secondComma = rawData.indexOf(',', firstComma + 1);
      int thirdComma = rawData.indexOf(',', secondComma + 1);

      if (firstComma > 0 && secondComma > 0 && thirdComma > 0) {
        String message = rawData.substring(secondComma + 1, thirdComma);
        Serial.println(message);  // Stampa solo HELLO
      }
    }
  }
}
