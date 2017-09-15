
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
//Button Press items

int button = 0;
int M = 0;
int LED = LOW;
const int buttonPin = 2;
const int LEDPin = 40;


//Timer items
int start = 0;
int start_of_close = 0;
int start_of_open = 0;
int n = 3;


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
  open_hand();
}

void loop() {
  //Reset Servo Positions
  

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
  collect_and_print_signals();
}

void close_hand() {
  //Set Servo Positions to CLOSED
  D0_servo.write(180);
  D1_servo.write(0);
  D2_servo.write(180);
  D3_servo.write(180);
  D4_servo.write(180);
  D5_servo.write(0);
}


void open_hand() {
  //Set Servo Positions to OPENED
  D0_servo.write(180);
  D1_servo.write(180);
  D2_servo.write(0);
  D3_servo.write(0);
  D4_servo.write(0);
  D5_servo.write(180);
}


void print_for_n_seconds(int seconds) {
  unsigned long start = millis();
  int delay_in_milliseconds = seconds * 1000;
  while (start > millis() - delay_in_milliseconds) {
    collect_and_print_signals();
  }
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
           String(D5);            
            
  Serial.println(s);
}


