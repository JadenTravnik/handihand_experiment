
// Recieve buffer
byte const FLAG = 0x2E; //"Ascii period": Flag used to identify start of stream
byte recieveBuffer[12]; // Receive buffer


void setup()
{
  //Set up serial And BT
  Serial.begin(38400);  // Begin the serial monitor at 38400bps
  Serial1.begin(38400);  // Begin Bluetooth

}

int Glove_D0_pos, Glove_D1_pos, Glove_D2_pos, Glove_D3_pos, Glove_D4_pos, Glove_D5_pos;

void loop(){
  read_glove();
  String s = String(Glove_D0_pos) + "," +
             String(Glove_D1_pos) + "," +
             String(Glove_D2_pos) + "," +
             String(Glove_D3_pos) + "," +
             String(Glove_D4_pos) + "," +
             String(Glove_D5_pos);             
  Serial.println(s);
}


void read_glove(){
  // If there's anything to read
  if (Serial1.available() >= sizeof(recieveBuffer)){
    if (Serial1.read() * 256 + Serial1.read() == FLAG) {
      if (Serial1.read() * 256 + Serial1.read() == FLAG){       
        Serial1.readBytes(recieveBuffer, sizeof(recieveBuffer));
        Glove_D0_pos = (int)(recieveBuffer[0] * 256 + recieveBuffer[1]);
        Glove_D1_pos = (int)(recieveBuffer[2] * 256 + recieveBuffer[3]);
        Glove_D2_pos = (int)(recieveBuffer[4] * 256 + recieveBuffer[5]);
        Glove_D3_pos = (int)(recieveBuffer[6] * 256 + recieveBuffer[7]);
        Glove_D4_pos = (int)(recieveBuffer[8] * 256 + recieveBuffer[9]);
        Glove_D5_pos = (int)(recieveBuffer[10] * 256 + recieveBuffer[11]);
      }
    }
  }
}
