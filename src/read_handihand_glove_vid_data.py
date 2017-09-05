import serial
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

handihand_ser = serial.Serial("/dev/ttyACM0", baudrate=38400)
# glove_ser = serial.Serial("/dev/ttyACM1", baudrate=38400)
cam = cv2.VideoCapture(1)

filename_prefix = raw_input('Enter filename prefix (eg cone): ')
num_trials = int(raw_input('Enter number of trials: '))
started = False
data_folder = 'data/'

display = False
if display:
    plt.ion()
    im = plt.imshow(np.zeros((480, 640, 3)))
    plt.show()

for i in range(num_trials):
    filename = filename_prefix + '_' + str(i)
    f = open(data_folder + filename + '.txt', 'w')
    img_data = []
    if not started:
        print('Waiting for button to start...')
        while True:
            data = handihand_ser.readline().rstrip('\r\n')
            try:
                if int(data.split(',')[0]):
                    started = True
                    print('Starting '+ filename_prefix + ' trials ' + str(data))
                    break
            except:
                pass
    steps = 0
    _, img = cam.read()
    while True:
        try:
            steps += 1
            # img_data.append(img)
            # if display:
            #     im.set_data(img)
            #     plt.pause(0.00001)

            hh_data = handihand_ser.readline().rstrip('\r\n')
            hh_data = hh_data.split(',')
            # gg_data = glove_ser.readline().rstrip('\r\n')
            # gg_data = gg_data.split(',')
            # hh_data.extend(gg_data)
            if len(hh_data) == 16:
                f.write(','.join(hh_data) + '\n')

            print(hh_data)
        except KeyboardInterrupt:
            f.close()
            img_data = np.array(img_data)
            np.save(data_folder + filename, img_data)
            started = False
            print('Saving ' + filename)
            break
