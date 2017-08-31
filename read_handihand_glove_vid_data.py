import serial
import cv2
import numpy as np
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/tty.usbserial', 9600)
filename_prefix = raw_input('Enter filename prefix (eg cone): ')
num_trials = int(raw_input('Enter number of trials: '))
started = False

cam = cv2.VideoCapture(0)


for i in range(num_trials):
    filename = filename_prefix + '_' + str(i)
    f = open(filename + '.txt', 'w')
    img_data = []
    if not started:
        print('Waiting for button to start...')
        while True:
            data = ser.readline().rstrip('\n')
            if int(data.split(',')[0]):
                started = True
                print('Starting '+ filename_prefix + ' trials')
                break
    while True:
        _, img = cam.read()
        img_data.append(img)

        data = ser.readline().rstrip('\n')
        f.write(data)
        if int(data.split(',')[0]): # new trial
            f.close()
            img_data = np.array(img_data)
            np.save(filename, img_data)
            print('Finished recording ' + filename + '\nRecording trial ' + str(i+1))
            break
