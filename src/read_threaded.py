# from threading import Thread
from multiprocessing import Process
import serial
import time
import numpy as np


class GetSerialDataProcess(Process):

    def __init__(self, port, length, filename, baudrate=38400):
        self.ser = serial.Serial(port, baudrate=baudrate)
        self.file = open(filename + '.txt', 'w')
        self.length = length
        self.times = []
        self.time_length = 250
        self.data_points = 0
        self.avg = 0

        super(GetSerialDataProcess, self).__init__()

    def run(self):
        start_time = time.time()
        data = self.ser.readline().rstrip('\r\n')
        if len(data.split(',')) == self.length:
            self.file.write(str(time.time()) + data + '\n')
            self.data_points += 1
        self.times.append(time.time() - start_time)
        if len(self.times) > self.time_length:
            del self.times[0]
        print(np.mean(self.times))

    def close(self):
        self.file.close()
        return self.data_points

if __name__ == '__main__':
    # hand_ser = GetSerialDataProcess("/dev/ttyACM0", 16, 'hand')
    glove_ser = GetSerialDataProcess("/dev/ttyACM1", 6, 'glove')
    # hand_ser.start()
    glove_ser.start()
    glove_ser.join()
    start_time = time.time()
    while time.time() - 4  < start_time:
        time.sleep(1)

    # h = hand_ser.close()
    # print(h)
    # hand_ser.terminate()

    h = glove_ser.close()
    print(h)
    glove_ser.terminate()
