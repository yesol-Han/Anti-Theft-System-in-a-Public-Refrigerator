#include <LiquidCrystal_I2C.h>     //LiquidCrystal 라이브러리 추가 
LiquidCrystal_I2C lcd(0x27, 16, 2);  //lcd 객체 선언

//LCD 핀은 고정

String first, second;
int state_save = 1;

void lcd_init() {
  lcd.begin(); //LCD 사용 시작
  lcd_setMode(1, "None");
  Serial.println("LCD Ready");
}

void lcd_setMode(int state, String value = "None") {
  state_save = state;
  //글짜 바꾸기.....
  switch (state) {
    case 1: { //usually
        first = "Input";
        second = "Your ID!";
        lcd_turn_time = 1000;
        break;
      }
    case 2: { //리모컨:입력 중
        first = "Password is:";
        second = value;
        lcd_turn_time = 500;
        break;
      }
    case 3: { // 리모컨: 다시 입력하세요
        first = "ID is wrong";
        second  = "Input again";
        lcd_turn_time = 1000;
        break;
      }
    case 4: { //문 열때
        first = "Mode: ";
        second = "*** Open ***";
        lcd_turn_time = 1000;
        break;
      }
    case 5: { //문 닫을때
        first = "Mode: ";
        second = "*** Close **";
        lcd_turn_time = 1000;
        break;
      }
    case 6: { // RFID 띄우기
        first = "ID is....";
        second = value;
        lcd_turn_time = 1000;
        break;
      } //ID 맞았을때, 틀렸을때 lcd 만들기---- Ok, Registered. Put it in! / Not your Item! Please get back
    case 7: { //warning
        first = "Warning";
        second = "Return Item!";
        lcd_turn_time = 300;
        break;
      }
    case 8: { //RFID 태깅해주세요
        first = "Please";
        second = "RFID tagging!";
        lcd_turn_time = 1000;
        break;
      }
    case 9: {
      first = "Safe Mode";
      second = "*** rework ***";
      lcd_turn_time = 2000;
    }
    default: {
        //그냥 해놓음...
        break;
      }
  }
}

void lcd_expr(int ver) {  //lcd_expression  ver = 1 -> 2 -> 3
  switch (ver) {
    case 0: {
        lcd.setCursor(2, 0);    // 커서를 5, 0에 가져다 놓아라. (열, 행)
        lcd.print(first);
        break;
      }
    case 1: {
        lcd.setCursor(2, 1);    // 커서를 3, 1로 가져다 놓아라. (열, 행)
        lcd.print(second);
        break;
      }
    case 2: {
        lcd.clear();            // 글자를 모두 지워라.

        //모드변환 - 한번씩만 띄울 수 있게!
        if (state_save == 4)
          lcd_setMode(8, "None");
        if (state_save == 5)
          lcd_setMode(1, "None");

        break;
      }
    default:
      Serial.println("ERROR: lcd_expr");
      break;
  }
}
