#include <SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>
// 引入 SPI 程式庫 與 MFRC522 程式庫
#define RST_PIN 9
#define SS_PIN 53
MFRC522 *mfrc522;
#define R3 32
#define R2 34
#define M 36
#define L2 38
#define L3 30
int PWMA = 11;
int AIN2 = 3;
int AIN1 = 2;
int BIN1 = 5;
int BIN2 = 6;
int PWMB = 12;
double w2=1;
double w3=2;
double Kp=30;
double Tpr=160;
double Tpl=155;

//double Tpr=50;
//double Tpl=50;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  pinMode(R3, INPUT);
  pinMode(R2, INPUT);
  pinMode(M, INPUT);
  pinMode(L2, INPUT);
  pinMode(L3, INPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(PWMB, OUTPUT);
  SPI.begin();
  mfrc522 = new MFRC522(SS_PIN, RST_PIN);
  // 請系統去要一塊記憶體空間，後面呼叫它的建構函式
  // 將(SS, RST) 當成參數傳進去初始化。
  mfrc522->PCD_Init();
  /* 初始化MFRC522讀卡機 PCD_Init 模組。 -> 表示：
  透過記憶體位置，找到 mfrc522 這物件，再翻其內容。*/
  //Serial1.print("Read UID on a MIFARE PICC:\n");
}

void motorcontrol(double VL,double VR) { 
  if(VL<0){
    analogWrite(PWMA,-VL);
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH); 
  }
  else{
    analogWrite(PWMA,VL);
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
  }
  if(VR<0){
    analogWrite(PWMB,-VR);
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH); 
  }
  else{
    analogWrite(PWMB,VR);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);     
  } 
}

void turnleft(){
  motorcontrol(Tpl-95,Tpr+95);
  delay(350);
  return;
}

void turnright(){
  motorcontrol(Tpl+90,Tpr-95);
  delay(350);
  return;
}

void turnback(){
  //delay(300);
  motorcontrol(-Tpl,Tpr);
  
  //Serial1.print(millis());
  delay(300);
  //motorcontrol(-Tpl+20,Tpr-20);
  while(true){ 
    motorcontrol(-Tpl,Tpr);  
    if(digitalRead(L3) == 1||digitalRead(R3)==1){
      //Serial1.print(millis());
      
      motorcontrol(0,0);
      delay(65);
      return;
    }
  }
}
void gostraight(){
  motorcontrol(Tpl, Tpr);
  delay(300);
}
void BT(){
  Serial1.write("node\n"); 
  while(true){
    motorcontrol(0, 0);
    if(Serial1.available()){
      char BTStr= Serial1.read();
      if(BTStr == 'l'){
        turnleft();
        break;
      }
      else if(BTStr == 'r'){
        turnright();
        break;
      }
      else if(BTStr == 'b'){
        turnback();
        break;
      }
      else if(BTStr == 's'){
        gostraight();
        break;
      }
      else{
        Serial1.print("wrongcommand\n");
        break;
      }  
    }
  }
}
void Tracking() {
  //rfid();
  int l3 = digitalRead(L3);
  int l2 = digitalRead(L2);
  int m = digitalRead(M);
  int r2 = digitalRead(R2);
  int r3 = digitalRead(R3);
  if(l3*l2*r2*r3*m==1){   
    BT();
  }
  double error = (l3*(-w3) + l2*(-w2) + r2*w2 + r3*w3)/(l3 + l2 + m + r2 + r3);
  int powerCorrection = Kp * error; // ex. Kp = 100, 也與w2 & w3有關
  int vR = Tpr - powerCorrection; // ex. Tp = 150, 也與w2 & w3有關
  int vL = Tpl + powerCorrection;
  if(vR>255) vR = 255;
  if(vL>255) vL = 255;
  if(vR<-255) vR = -255;
  if(vL<-255) vL = -255;
  motorcontrol(vL, vR); //Feedback to motors
}
void rfid(){ 
  if(!mfrc522->PICC_IsNewCardPresent()) {
    goto FuncEnd;
  } //PICC_IsNewCardPresent()：是否感應到新的卡片?
  motorcontrol(0,0);
  if(!mfrc522->PICC_ReadCardSerial()) {
    goto FuncEnd;
  } //PICC_ReadCardSerial()：是否成功讀取資料?
  Serial1.write("**Card Detected:**\n");
  Serial1.write("uid: \n");
  
  //mfrc522->PICC_DumpDetailsToSerial(&(mfrc522->uid)); //讀出 UID
  byte *id = mfrc522->uid.uidByte;
  byte idSize = mfrc522->uid.size;

  

  //String uidstr = "";
  Serial1.write("card\n");
  for (byte i = 0; i < idSize; i++) {  // 逐一顯示UID碼
    Serial1.write(id[i]);
    //Serial1.write(".");
    //Serial.print("id[");
    //Serial.print(i);
    //Serial.print("]: ");
    //uidstr = uidstr + String(id[i],HEX);
  } 
  Serial1.write("\n");
  
  //char* uid = uidstr.c_str(); 
  //Serial1.write(uid);
  
  mfrc522->PICC_HaltA(); // 讓同一張卡片進入停止模式 (只顯示一次)
  mfrc522->PCD_StopCrypto1(); // 停止 Crypto1
  FuncEnd:; // goto 跳到這
}
int i = 0;
void loop(){
  int l3 = digitalRead(L3);
  int r3 = digitalRead(R3);
  if(Serial1.available()){
    char connect = Serial1.read();   
    if (connect == 'c')
      while(1){
        motorcontrol(95,100);
        int l3 = digitalRead(L3);
        int r3 = digitalRead(R3);
        if(l3 +r3 ==0){
          i = 1;
          break;
        }
      }
      
  }
   
  if(i == 1){ 
    Tracking();
    rfid(); 
  }
  //delay(10);
}
