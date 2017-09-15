import sys
import numpy as np
import matplotlib.pyplot as plt


def txt2np(filename):
    return np.loadtxt(open(filename), delimiter=',')

fig, ax = plt.subplots(2)

glove_labels = ['time', 'thumb rot', 'thumb flex', 'pointer', 'middle', 'ring', 'pinky']
glove_data = txt2np(sys.argv[1] + '_glove.txt')
for i in range(1, glove_data.shape[1]):
    ax[0].plot(glove_data[:, 0], glove_data[:,i], label=glove_labels[i])
ax[0].legend()

hand_labels = ['time', 'button', 'thumb rot', 'thumb prox', 'fake', 'thumb distal', 'index prox',
               'index intermediate', 'middel prox', 'middle intermediate', 'ring prox', 'pinky prox',
                'thumb fsr', 'index fsr', 'middle fsr', 'ring fsr', 'pinky fsr']
hand_data = txt2np(sys.argv[1] + '_hand.txt')
for i in range(1, hand_data.shape[1]):
    ax[1].plot(hand_data[:, 0], hand_data[:, i], label=hand_labels[i])
ax[1].legend()

plt.show()
