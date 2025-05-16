String data;

void setup() {
  Serial1.begin(57600);
  delay(1000);
}   

void loop() {
  sendData("HELLO");
  delay(1000);
}

void sendData(String data){
  Serial1.print("AT+SEND=1,");
  Serial1.print(data.length());
  Serial1.print(",");
  Serial1.println(data);
}
