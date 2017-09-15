import numpy as np
from glob import glob
import matplotlib.pyplot as plt

from IPython import embed

def txt2np(filename):
    return np.loadtxt(open(filename), delimiter=',')


def camera_data_gen(camera_prefix):
    names = glob(camera_prefix + '*.npy')
    names.sort()
    for name in names:
        camera_data = np.load(name)
        for i in range(camera_data.shape[0]):
            yield camera_data[i]


# cam feature types: 1x1 histogram (hist1), 3x3 histogram (hist9), convolutional NN (conv)
def merge_data_gen(hand_file, glove_file, camera_prefix, camera_feature_type='hist1'):
    hand = txt2np(hand_file)
    glove = txt2np(glove_file)
    camera_times = txt2np(camera_prefix + '_times.txt')
    camera_gen = camera_data_gen(camera_prefix)

    last_hand, last_camera = hand[0], camera_gen.next()
    last_hand_index = last_camera_index = 0

    for i in range(glove.shape[0]):
        # if new hand data available, get new hand data
        if hand[last_hand_index+1,0] < glove[i,0]:
            last_hand_index += 1
            last_hand = hand[last_hand_index,1:]

        if camera_times[last_camera_index+1] < glove[i,0]:
            last_camera_index += 1
            last_camera = camera_gen.next()

        yield glove[i,1:], last_hand, last_camera


def merge(all_data, hist, cam_time):
    last_cam = hist[0]
    last_cam_index = cam_time.shape[0]
    all_data = np.c_[all_data, np.zeros((all_data.shape[0], hist.shape[1]))]
    for i in range(all_data.shape[0]-1,0,-1):
        if last_cam_index - 1 > 0 and cam_time[last_cam_index - 1] > all_data[i,0]:
            last_cam = hist[last_cam_index - 1]
            last_cam_index -= 1
        all_data[i, -hist.shape[1]:] = last_cam
    return all_data

def get_cam_times(prefix, num_frames):
     cam_times = []
     names = glob('../data/' + prefix + '*camera_times.txt')
     names.sort()
     for name in names:
         print('loading ' + name)
         data = txt2np(name)
         data = data[:(data.shape[0]/200)*200]
         cam_times.append(data)
     cam_times = np.array(cam_times)
     return np.concatenate(cam_times)[:num_frames]


def get_cam_hist(prefix):
     names = glob('../data/' + prefix + '*camera*.npy')
     names.sort()
     hist = []
     for name in names:
         print('loading ' + name)
         cam = np.load(name, 'r')
         hist.append(np.mean(cam, axis=(1,2)))
     return np.vstack(np.array(hist))

def create_trials(prefix):
    cam_hist = get_cam_hist(prefix)
    cam_times = get_cam_times(prefix, cam_hist.shape[0]) # TODO need to push sections over a bit

    print('loading ../data/all_' + prefix.replace('-','_') + '.npy')
    all_data = np.load('../data/all_' + prefix.replace('-','_') + '.npy')
    print('Merging ' + prefix)
    all_data = merge(all_data, cam_hist, cam_times)
    print('Done merge')

    buttons = np.where(all_data[:,1])[0]
    good_trials = 0
    for i in range(len(buttons)):
        start_time = all_data[buttons[i], 0]
        end_time = start_time + 9.

        if i < len(buttons) - 1:
            end = np.argmin(np.abs(all_data[buttons[i]:buttons[i+1],0] - end_time)) + buttons[i]
        else:
            end = np.argmin(np.abs(all_data[buttons[i]:,0] - end_time)) + buttons[i]
        try:
            assert(abs(all_data[end, 0] - start_time - 9) < 0.1)
            np.save('../data/trials/' + prefix + '_' + str(i), all_data[buttons[i]: end])
            good_trials += 1
        except:
            print('Trial ' + str(i) + ' is bad with ' + str(end - buttons[i]) + ' iterations and ' + str(all_data[end, 0] - start_time - 9))
            pass
    print(str(good_trials) + ' trials saved for ' + prefix)

shapes = ['green-cyl', 'orange-cyl', 'green-step', 'orange-step']
for shape in shapes:
    create_trials(shape)
