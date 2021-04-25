#define Magnetic_PIN 7
int count1 = 0, open_count1 = 0;  //magnetic 스위치 확인

void Magnetic_init() {
  pinMode(Magnetic_PIN, INPUT_PULLUP);             // 디지털 3번핀을 입력모드로 설정
  Serial.println("Magnetic: Ready");
}

int Magnetic_value() {  //열면 0, 붙으면 1
  return digitalRead(Magnetic_PIN);
}

void Magnetic_check() { //@@두번으로 줄임
  count1++;
  open_count1 += Magnetic_value();

  //Serial.print("count1: ");
  //Serial.print(count1);
  //Serial.print(", open_count1: ");
  //Serial.println(open_count1);

  if (open_count1 != 0) {
    if (count1 == 2) {
      if (open_count1 == 2) {  //문이 닫힘을 인식
        Serial.println("Magnetic: door is closed");
        close_door();
      } else
        Serial.println("Magnetic: count again!");
      count1 = 0;
      open_count1 = 0;
    }
  } else {
    count1 = 0;
  }
}
