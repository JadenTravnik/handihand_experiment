
import cv2
import numpy as np

import matplotlib.pyplot as plt

def show_webcam(mirror=False):
    steps = 0
    cam = cv2.VideoCapture(0)
    im = plt.imshow(np.zeros((460, 640, 3)))
    while True:
    	ret_val, img = cam.read()
    	if mirror:
    		img = cv2.flip(img, 1)
    	print(img.shape)
        im.set_data(img)
        plt.pause(0.001)


def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()
