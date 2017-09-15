
import cv2
import numpy as np
import sys

import matplotlib.pyplot as plt

def show_webcam(mirror=False):
    steps = 0
    cam = cv2.VideoCapture(1)
    im = plt.imshow(np.zeros((460, 640, 3)))
    while True:
    	ret_val, img = cam.read()
        img = np.flip(img, 2)
    	if mirror:
    		img = cv2.flip(img, 1)
    	print(img.shape)
        im.set_data(img)
        plt.pause(0.001)

def show_numpy(filename):

    im = plt.imshow(np.zeros((460, 640, 3)))
    section = 0
    while True:
        try:
            data = np.load(filename + '_' + str(section) + '.npy', mmap_mode='r')
            print('loading section ' + str(section) + ' frames: ' + str(data.shape[0]))
            for i in range(data.shape[0]):
                im.set_data(np.flip(data[i],2))
                plt.pause(0.001)
            section += 1
        except:
            exit()

def main():
    plt.ion()
    if len(sys.argv) == 1:
	   show_webcam()
    else:
       show_numpy(sys.argv[1])


if __name__ == '__main__':
	main()
