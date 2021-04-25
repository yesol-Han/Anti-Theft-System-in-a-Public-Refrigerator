#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3); //블루투스의 Tx, Rx핀을 2번 3번핀으로 설정

long time1, time2, time3, time4, time5, time6;
int lcd_turn = 0, lcd_turn_time = 1000; //lcd 넘어기는거, 보이는 시간 조정
bool open_r = false;
String remote_save;
int count2;

void lcd_setMode(int state, String value);  //LCD 함수 선언

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; //시리얼통신이 연결되지 않았다면 코드 실행을 멈추고 무한 반복
  }
  func_init();
  Serial.println("Hello World!");
  Serial.flush();
}

void loop() {
  // 1번 파트: 블루투스 통신
  BLE_conn();

  time1 = millis();

  // 2번 파트: LCD 동작 (내용, 시간은 각 동작에서 지정)
  if (time1 - time3 >= lcd_turn_time) {
    time3 = millis();
    lcd_expr(lcd_turn++);
    if (lcd_turn == 3) {
      lcd_turn = 0;
    }
  }

  // 3번 파트: 닫혀 있을 때 / 열려 있을 때
  if (!open_r) { //1. 닫혀 있을 때의 동작

    if (time1 - time2 >= 100) {   //리모컨 동작
      time2 = millis();
      remote_save = IRremote_receive_sign();
      if (remote_save != "") {
        lcd_setMode(2, remote_save);
      } else {
        if (++count2 == 100) { //100*100 -> 10초
          lcd_setMode(1, "None");
          count2 = 0;
        }
      }
    }

  } else { //2. 열려 있을 때의 동작

    if (time1 - time4 >= 1000) {   //RFID 동작
      time4 = millis();
      RFID_sensing();
    }

    if (time1 - time5 >= 1000 && time1-time6>=3000) {  //1초마다, 문 열림 여부 인식
      time5 = millis();
      Magnetic_check();
    }

  }
}

void func_init() {
  BLE_init();
  lcd_init();
  Magnetic_init();
  IRremote_init();
  Solenoid_init();
  RFID_init();
}

void open_door() {
  open_r = true;
  lcd_setMode(4, "None");
  Solenoid_mode(open_r);
  BLE_Send("O1");
  time6 = millis();
}

void close_door() {
  open_r = false;
  lcd_setMode(5, "None");
  Solenoid_mode(open_r);
  BLE_Send("O0");
}
