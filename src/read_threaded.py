from multiprocessing import Process
import serial
import time
import cv2
import numpy as np
import glob

class RecordCameraProcess(Process):

    def __init__(self, name, cam_id, filename, max_file_size=200):
        self.cam = cv2.VideoCapture(cam_id)
        self.filename = filename
        self.data = []
        self.times = []
        self.time_length = 250
        self.data_points = 0
        self.avg = 0
        super(RecordCameraProcess, self).__init__()
        self.name = name
        self.max_file_size = max_file_size
        self.sections = 0
        self.time_file = open(filename + '_times.txt', 'w')

    def run(self):
        while(self.cam.isOpened()):
            start_time = time.time()
            ret, frame = self.cam.read()

            if len(self.times) > self.time_length:
                del self.times[0]

            if ret==True:
                self.time_file.write(str(time.time()) + '\n')
                self.time_file.flush()
                self.data_points += 1

                self.data.append(cv2.flip(frame,0))
                if len(self.data) >= self.max_file_size:
                    np.save(self.filename + '_' + str(self.sections), np.array(self.data))
                    self.data = []
                    print('Saved ' + self.filename + ' sections ' + str(self.sections))
                    self.sections += 1

                if not self.data_points % 50:
                    self.log()
            else:
                print('\n\n\n RET is FALSE \n\n\n')
                break
            self.times.append(time.time() - start_time)

    def log(self):
        avg = np.mean(self.times)
        print(str(self.data_points) + '\t' +
              '~' + str(round(avg,3)) + ' seconds\t' +
              str(round(1./avg,3)) + 'Hz ' + self.name)

    def terminate(self):
        # print('Termiating ' + self.name)
        # _max = -1
        # for name in glob.glob(self.filename + '*.npy'):
        #     _max = max(_max, int(name.split('camera_')[1].split('.')[0]))
        #
        # np.save(self.filename + '_' + str(_max+1), np.array(self.data))
        # print('Saved ' + self.filename + ' sections ' + str(_max+1))
        self.time_file.close()

        super(RecordCameraProcess, self).terminate()

class GetSerialDataProcess(Process):

    def __init__(self, name, port, expected_length, filename, baudrate=38400, _log=False):
        self.ser = serial.Serial(port, baudrate=baudrate)
        self.file = open(filename + '.txt', 'w')
        self.expected_length = expected_length
        self.times = []
        self.time_length = 250
        self.data_points = 0
        self.avg = 0
        self._log = _log

        super(GetSerialDataProcess, self).__init__()
        self.name = name

    def run(self):
        while True:
            start_time = time.time()
            data = self.ser.readline().rstrip('\r\n')
            if len(data.split(',')) == self.expected_length:
                s = str(time.time()) + ', ' + data + '\n' # need to make sure that data

                self.file.write(s) #  is actually all of the data
                self.file.flush()
                self.data_points += 1

            self.times.append(time.time() - start_time)
            if len(self.times) > self.time_length:
                del self.times[0]
            if self._log:
                self.log()

    def log(self):
        avg = np.mean(self.times)
        if not self.data_points % 500:
            print(str(self.data_points) + '\t' +
                  '~' + str(round(avg,3)) + ' seconds\t' +
                  str(round(1./avg,3)) + 'Hz ' + self.name)

    def terminate(self):
        print('Termiating ' + self.name)
        self.file.close()
        super(GetSerialDataProcess, self).terminate()

def txt2np(filename):
    return np.loadtxt(open(filename), delimiter=',')

if __name__ == '__main__':

    filename_prefix = raw_input('Enter filename prefix (eg cone): ')
    data_folder = '../data/'
    hand_proc = GetSerialDataProcess('hand', "/dev/ttyACM1", 16, data_folder + filename_prefix + '_hand')
    glove_proc = GetSerialDataProcess('glove', "/dev/ttyACM0", 6, data_folder + filename_prefix + '_glove')
    cam_proc = RecordCameraProcess('cam', 1, data_folder + filename_prefix + '_camera')

    cam_proc.start()
    hand_proc.start()
    glove_proc.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        hand_proc.terminate()
        glove_proc.terminate()
        cam_proc.terminate()



    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2)

    glove_labels = ['time', 'thumb rot', 'thumb flex', 'pointer', 'middle', 'ring', 'pinky']
    glove_data = txt2np(data_folder + filename_prefix + '_glove.txt')
    for i in range(1, glove_data.shape[1]):
        ax[0].plot(glove_data[:, 0], glove_data[:,i], label=glove_labels[i])
    ax[0].legend()

    hand_labels = ['time', 'button', 'thumb rot', 'thumb prox', 'fake', 'thumb distal', 'index prox',
                   'index intermediate', 'middel prox', 'middle intermediate', 'ring prox', 'pinky prox',
                    'thumb fsr', 'index fsr', 'middle fsr', 'ring fsr', 'pinky fsr']
    hand_data = txt2np(data_folder + filename_prefix + '_hand.txt')
    for i in range(1, hand_data.shape[1]):
        ax[1].plot(hand_data[:, 0], hand_data[:, i], label=hand_labels[i])
    ax[1].legend()

    camera_times = txt2np(data_folder + filename_prefix + '_camera_times.txt')

    plt.show()

    plt.ion()
    im = plt.imshow(np.zeros((460, 640, 3)))
    section = 0
    while True:
        try:
            data = np.load(data_folder + filename_prefix + '_camera' + '_' + str(section) + '.npy')
            print('loading section ' + str(section))
            for i in range(data.shape[0]):
                im.set_data(data[i])
                plt.pause(0.0001)
            section += 1
        except:
            exit()
