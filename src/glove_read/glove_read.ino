
void setup()
{
  Serial.begin(38400);  // Begin the serial monitor at 9600bps
}

void loop() {

  Serial.println(String(analogRead(A0)) + ", " + // Thumb Ad/Ab 
                 String(analogRead(A1)) + ", " + // Thumb F/E
                 String(analogRead(A2)) + ", " + // Index
                 String(analogRead(A3)) + ", " + // Middle
                 String(analogRead(A4)) + ", " + // Ring finger 
                 String(analogRead(A5))); // Pinky
}


