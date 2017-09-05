
//This script starts the serial monitor, and upon a button press prints a marker, waits 2 seconds, closes the hand, waits 2 seconds, opens the hand.
//All sensor data is recorded in the serial monitor in the order M,D0,D1P,D1I,D1D,D2P,D2I,D3P,D3I,D4P,D5P,D1,D2,D3,D4,D5/n
//31/08/2017

#include <Servo.h>

//servos
Servo D0_servo;  // create servo objects to control servos
Servo D1_servo;
Servo D2_servo;
Servo D3_servo;
Servo D4_servo;
Servo D5_servo;

//Potentiometer Values
int D0 = 0;
int D1P = 0;
int D1I = 0;
int D1D = 0;
int D2P = 0;
int D2I = 0;
int D3P = 0;
int D3I = 0;
int D4P = 0;
int D5P = 0;
//FSR Values
int D1 = 0;
int D2 = 0;
int D3 = 0;
int D4 = 0;
int D5 = 0;
//Servo Positions
int D0_servo_pos = 0;
int D1_servo_pos = 0;
int D2_servo_pos = 0;
int D3_servo_pos = 0;
int D4_servo_pos = 0;
int D5_servo_pos = 0;
//Button Press items
int button = 0;
int M = 0;
int LED = LOW;
const int buttonPin = 2;
const int LEDPin = 40;

// Glove Items
byte const FLAG = 0x2E; //"Ascii period": Flag used to identify start of stream
byte recieveBuffer[16]; // Receive buffer
int Glove_D0_pos, Glove_D1_pos, Glove_D2_pos, Glove_D3_pos, Glove_D4_pos, Glove_D5_pos;

//Timer items
int start = 0;
int start_of_close = 0;
int start_of_open = 0;
int n = 10;


void setup() {
  //Set up serial
  Serial.begin(38400);  // Begin the serial monitor at 38400bps
  Serial1.begin(38400);

  // set servo objects to appropriate pins
  D0_servo.attach(3);
  D1_servo.attach(5);
  D2_servo.attach(6);
  D3_servo.attach(9);
  D4_servo.attach(10);
  D5_servo.attach(11);

  pinMode(LEDPin, OUTPUT); //initialize LED pin as output
  pinMode(buttonPin, INPUT); //initialize button pin as input
}

void loop() {
  //Reset Servo Positions
  open_hand();

  //read the state of the button
  button = digitalRead(buttonPin);

  if (button == HIGH) {
    //turn LED on:
    digitalWrite(LEDPin, HIGH);

    //Marker to show start of trial
    M = 1;
    // Collect and print signals, with M=1 Marker
    collect_and_print_signals();
    //Reset Marker
    M = 0;

    // Collect and print signals, with M=0 Marker
    print_for_n_seconds(n);

    close_hand();

    //Start Closed Timer
    print_for_n_seconds(n);

    open_hand();

    //Start Opened Timer
    print_for_n_seconds(n);

    //turn off LED:
    digitalWrite(LEDPin, LOW);
  }
}

void close_hand() {
  //Set Servo Positions to CLOSED
  D0_servo_pos = 180;
  D1_servo_pos = 0;
  D2_servo_pos = 180;
  D3_servo_pos = 180;
  D4_servo_pos = 180;
  D5_servo_pos = 0;
  D0_servo.write(D0_servo_pos);
  D1_servo.write(D1_servo_pos);
  D2_servo.write(D2_servo_pos);
  D3_servo.write(D3_servo_pos);
  D4_servo.write(D4_servo_pos);
  D5_servo.write(D5_servo_pos);
}


void open_hand() {
  //Set Servo Positions to OPENED
  D0_servo_pos = 180;
  D1_servo_pos = 180;
  D2_servo_pos = 0;
  D3_servo_pos = 0;
  D4_servo_pos = 0;
  D5_servo_pos = 180;
  D0_servo.write(D0_servo_pos);
  D1_servo.write(D1_servo_pos);
  D2_servo.write(D2_servo_pos);
  D3_servo.write(D3_servo_pos);
  D4_servo.write(D4_servo_pos);
  D5_servo.write(D5_servo_pos);
}


void print_for_n_seconds(int seconds) {
  unsigned long start = millis();
  int delay_in_milliseconds = seconds * 1000;
  while (start > millis() - delay_in_milliseconds) {
    collect_and_print_signals();
  }
}

bool read_glove(){
  // If there's anything to read
  if (Serial1.available() >= sizeof(recieveBuffer)){
    // This could be done better, it looks redundant but isnt, please fix, hi from a laxy programmer
    // you could probably use a seperate buffer or something, 
    // or even like a counter that counts the number of "."s or seomthing
    if (Serial1.read() * 256 + Serial1.read() == FLAG) {
      if (Serial1.read() * 256 + Serial1.read() == FLAG) {
        Serial1.readBytes(recieveBuffer, sizeof(recieveBuffer));
        Glove_D0_pos = (int)(recieveBuffer[0] * 256 + recieveBuffer[1]);
        Glove_D1_pos = (int)(recieveBuffer[2] * 256 + recieveBuffer[3]);
        Glove_D2_pos = (int)(recieveBuffer[4] * 256 + recieveBuffer[5]);
        Glove_D3_pos = (int)(recieveBuffer[6] * 256 + recieveBuffer[7]);
        Glove_D4_pos = (int)(recieveBuffer[8] * 256 + recieveBuffer[9]);
        Glove_D5_pos = (int)(recieveBuffer[10] * 256 + recieveBuffer[11]);
        
        //---- This is a hack
        if (abs(Glove_D0_pos) > 1024)
          Glove_D0_pos = Glove_D0_pos >> 8;
          
        if (abs(Glove_D1_pos) > 1024)
          Glove_D1_pos = Glove_D1_pos >> 8;
          
        if (abs(Glove_D2_pos) > 1024)
          Glove_D2_pos = Glove_D2_pos >> 8;
          
        if (abs(Glove_D3_pos) > 1024)
          Glove_D3_pos = Glove_D3_pos >> 8;
          
        if (abs(Glove_D4_pos) > 1024)
          Glove_D4_pos = Glove_D4_pos >> 8;
          
        if (abs(Glove_D5_pos) > 1024)
          Glove_D5_pos = Glove_D5_pos >> 8;              
        //----
        
//            int Check_1_func = Glove_D0_pos * 2 + Glove_D1_pos * -3 + Glove_D2_pos * 3;
//            int Check_2_func = Glove_D3_pos * -3 + Glove_D4_pos * 3 + Glove_D5_pos * -7;
//            
//            int Check_1_actual = (int)(recieveBuffer[12] * 256 + recieveBuffer[13]);
//            int Check_2_actual = (int)(recieveBuffer[14] * 256 + recieveBuffer[15]);
//            
//            return (Check_1_func == Check_1_actual && Check_2_func == Check_2_actual);
        return true;
      }
    }
  }
  return false;
}

void collect_and_print_signals() {
  //Collect Sensor Signals
  D0 = analogRead(A2);
  D1P = analogRead(A3);
  D1D = analogRead(A4);
  D2P = analogRead(A5);
  D2I = analogRead(A6);
  D3P = analogRead(A7);
  D3I = analogRead(A8);
  D4P = analogRead(A9);
  D5P = analogRead(A10);
  D1 = analogRead(A11);
  D2 = analogRead(A12);
  D3 = analogRead(A13);
  D4 = analogRead(A14);
  D5 = analogRead(A15);
//  bool corrupted = read_glove();
//  String s = "";
//  if (corrupted){
//    s = "Corrupted| ";
//  }
  //Print Sensor Signals
  String s = String(M) + "," +
           String(D0) + "," +
           String(D1P) + "," +
           String(D1I) + "," +
           String(D1D) + "," +
           String(D2P) + "," +
           String(D2I) + "," +
           String(D3P) + "," +
           String(D3I) + "," +
           String(D4P) + "," +
           String(D5P) + "," +
           String(D1) + "," +
           String(D2) + "," +
           String(D3) + "," +
           String(D4) + "," +
           String(D5); // + "," +
//           String(Glove_D0_pos) + "," +
//           String(Glove_D1_pos) + "," +
//           String(Glove_D2_pos) + "," +
//           String(Glove_D3_pos) + "," +
//           String(Glove_D4_pos) + "," +
//           String(Glove_D5_pos);               
            
  Serial.println(s);
}


