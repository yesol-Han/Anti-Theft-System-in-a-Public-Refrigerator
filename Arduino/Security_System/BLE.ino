String serial_read = "";
char temp;

void BLE_init() {
  mySerial.begin(9600);

  while (!mySerial) {
    ; //시리얼통신이 연결되지 않았다면 코드 실행을 멈추고 무한 반복
  }

  BLE_Send("NHello!");
}


void BLE_conn() {
  mySerial.listen();
  if (mySerial.available() > 0) { //블루투스에서 넘어온 데이터가 있다면 (DB 조회 결과, 명령 등)

    while (mySerial.available() > 0) {  // 넘어온 명령어 복원
      temp = mySerial.read();
      Serial.print(temp);
//      Serial.print(temp, OCT);  //디버깅용
//      Serial.print(' ');
      
      //Serial.println( temp );
      if (temp != '/') {
        serial_read += temp;
        continue;
      } else if (temp == '\0' || temp =='\n'){
        continue;
      }
      //if (temp != 10 && temp != 13 && temp != 120)  //CR LF 조심
      
    }
  }
    serial_read += '\0';
    if (serial_read == "open") { //서보모터 문 열릴때는 명령으로, 닫을때는 magnetic로 판정
      open_door();
      //serial_read = "";
      Serial.println("Refrigerator Open");

    } else if (serial_read == "close") {  // 강제 닫기 (닫혀있는게 인식되지 않을 때)
      close_door();
      Serial.print("문 닫기");

    } else if (serial_read == "again") { // 다시 입력하세요!
      lcd_setMode(3, "None");
      Serial.print("다시 입력해");

    } else if (serial_read == "Warning") {
      lcd_setMode(7, "None");
      Serial.print("도난사고 발생");
    } else if (serial_read == "ok"){
      lcd_setMode(9, "None");
      Serial.print("안전모드");
    }
//    } else {
//      Serial.print("Another Order: ");
//      Serial.println(serial_read);
//    }

    serial_read = "";

    //여기에 println 쓰지 않기!!
    Serial.flush();
    mySerial.flush();
  
}

void BLE_Send(String text) {
  mySerial.print(text);
  mySerial.print('/');
  text = "->" + text;
  Serial.print(text);
}
