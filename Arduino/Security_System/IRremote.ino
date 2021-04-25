#include <IRremote.h>
#define RECV_PIN 6

IRrecv irrecv(RECV_PIN);
decode_results results;
String remote_str = "";

void IRremote_init() {
  irrecv.enableIRIn(); // Start the receiver
  Serial.println("IRremote Ready");
}

String IRremote_receive_sign() { // 리모컨 신호 받으려면 계속 돌려줘야 하는 코드
  if (irrecv.decode(&results)) { //키가 눌러진지 확인
    //Serial.println(results.value, HEX);
    //Serial.println(results.value);
    irrecv.resume(); // Receive the next value

    switch (results.value) {
      case 3238126971: {
          Serial.println("0");
          remote_str += "0";
          break;
        }
      case 2534850111: {
          Serial.println("1");
          remote_str += "1";
          break;
        }
      case 1033561079: {
          Serial.println("2");
          remote_str += "2";
          break;
        }
      case 1635910171: {
          Serial.println("3");
          remote_str += "3";
          break;
        }
      case 2351064443: {
          Serial.println("4");
          remote_str += "4";
          break;
        }
      case 1217346747: {
          Serial.println("5");
          remote_str += "5";
          break;
        }
      case 71952287: {
          Serial.println("6");
          remote_str += "6";
          break;
        }
      case 851901943: {
          Serial.println("7");
          remote_str += "7";
          break;
        }
      case 465573243: {
          Serial.println("8");
          remote_str += "8";
          break;
        }
      case 1053031451: {
          Serial.println("9");
          remote_str += "9";
          break;
        }
      case 4034314555: {
        Serial.println("_");
        remote_str += "_";
        break;
      }
      case 2538093563: {
          Serial.println("지우기");
          if (remote_str.length() > 1) {
            char buf[remote_str.length()];
            remote_str.toCharArray(buf, remote_str.length());
            remote_str = buf;
            //delete buf; //있는 것이 에러남
          } else if (remote_str.length() <= 1) {
            remote_str = "";
          }
          break;
        }
      case 4039382595: {
          Serial.println("끝-------------------------------");
          remote_str = "I" + remote_str;
          BLE_Send(remote_str); //블루투스를 통해 비밀번호 보내기
          remote_str = "";
          break;
        }
      default : {
          Serial.println("다시"); //리모컨 신호가 이상한 값일 때 띄우기, 실제로는 안보임
          break;
        }
    }
    Serial.print("리모컨 : ");
    Serial.println(remote_str);
  }
  return remote_str;
}

// -: 4034314555 F076C13B (,로 파씽)
//  0:  3238126971 C101E57B
//  100+: 2538093563  97483BFB  (지우기)
//  200+: 4039382595  F0C41643  (확인 버튼)
//  1:  2534850111  9716BE3F
//  2:  1033561079  3D9AE3F7
//  3:  1635910171  6182021B
//  4:  2351064443  8C22657B
//  5:  1217346747  488F3CBB
//  6:  71952287    FF5AA5
//  7:  851901943   32C6FDF7
//  8:  465573243   1BC0157B
//  9:  1053031451  3EC3FC1B
