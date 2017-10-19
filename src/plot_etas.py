import numpy as np
import matplotlib.pyplot as plt

def prepare_data(d):
    d = np.concatenate(tuple(d[:, i*2:i*2+2].reshape(1,-1,2) for i in range(6)))
    d[:,:,0] *= .001
    return d

def calc_error(d, the_return):
    return np.sqrt((d[2:6, cut_off: the_return_cut_off, 0] - the_return[2:6, cut_off:the_return_cut_off,0])**2)

print('Loading Data')
cut_off = 662581
the_return_cut_off = 840000

the_return = np.load('../data/true_return_trials/for_all.npy')
print('Loaded the_return')

Etas = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045]
ALL_DATA = []
FINGERS_DATA = []
CAMERA_DATA = []

for eta in Etas:
    all_data = np.load('results_of_learning/eta_sweep/results_of_all_all_signals_eta_' + str(eta) + '.npy')
    print('Loaded all_data ' + str(eta))
    all_data = prepare_data(all_data)
    error = calc_error(all_data, the_return)
    ALL_DATA.append([np.mean(error, axis=1), np.std(error, axis=1)])

    finger_data = np.load('results_of_learning/eta_sweep/results_of_fingers_all_signals_eta_' + str(eta) + '.npy')
    print('Loaded finger_data ' + str(eta))
    finger_data = prepare_data(finger_data)
    error = calc_error(finger_data, the_return)
    FINGERS_DATA.append([np.mean(error, axis=1), np.std(error, axis=1)])

    camera_data = np.load('results_of_learning/eta_sweep/results_of_camera_all_signals_eta_' + str(eta) + '.npy')
    print('Loaded camera_data ' + str(eta))
    camera_data = prepare_data(camera_data)
    error = calc_error(camera_data, the_return)
    CAMERA_DATA.append([np.mean(error, axis=1), np.std(error, axis=1)])

print('Done Load')

ALL_DATA = np.array(ALL_DATA)
FINGERS_DATA = np.array(FINGERS_DATA)
CAMERA_DATA = np.array(CAMERA_DATA)

from IPython import embed
embed()
exit()

# All_Errors = calc_error(all_data, the_return)
# Finger_Errors = calc_error(finger_data, the_return)
# Camera_Errors = calc_error(camera_data, the_return)


glove_labels = ['Index', 'Middle', 'Ring', 'Pinky']
nice_names = ['Color Only', 'Fingers Only', 'All']
colors = ['#3393C6', '#F2A45C', '#ABE188']

# color, fingers, all
for i_glove in range(len(glove_labels)):

    fig, axes = plt.subplots(figsize=(20, 14))
    axes.set_ylabel('Root Mean\nSquared\nError', rotation=0, fontsize=25, labelpad=50, weight='bold')
    axes.set_xlabel('Eta', fontsize=25, labelpad=50, weight='bold')
    plt.plot(ALL_DATA[:, i_glove, 0])


plt.suptitle('Distribution of Root Squared Error between True Return and Predictions\nafter Learning', fontsize=30, weight='bold')
