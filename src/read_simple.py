import serial

ser = serial.Serial("/dev/ttyACM1", baudrate=38400)

while True:
    try:
        print(ser.readline().rstrip('\r\n').split(','))
    except KeyboardInterrupt:
        break
