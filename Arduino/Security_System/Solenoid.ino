#define Solenoid_PIN 4

void Solenoid_init() {
  pinMode(Solenoid_PIN, OUTPUT);
  Serial.println("Solenoid: Ready");
}

void Solenoid_mode(bool mode) { //원 코드에 시리얼 값 읽는 코드 있음
  digitalWrite(Solenoid_PIN, mode);
  Serial.print("Solenoid:");
  Serial.println((int)mode);
}
