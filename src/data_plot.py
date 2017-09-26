import numpy as np
import matplotlib
font = {'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)

from matplotlib.font_manager import FontProperties

import matplotlib.pyplot as plt

def get_trial(filename_suffix, times):
    data = []
    nice_names = ['Color Only', 'Fingers Only', 'All']
    file_names = ['_colors_', '_fingers_', '_']
    for i in range(3):
        sub_data = np.array([np.load('results_of_learning/results_of_' + str(i_sensor) + file_names[i] + filename_suffix + '.npy') for i_sensor in range(17,23)])
        sub_data = sub_data[:, times[0]:times[1], :]
        sub_data[:,:,0] -= np.min(sub_data[:,:,0])
        sub_data[:,:,0] /= np.max(sub_data[:,:,0])
        data.append((nice_names[i], sub_data))
    return data

def plot_all(title, shapes):
    fig, axes = plt.subplots(4, 3, sharex='col', sharey='row', figsize=(20, 14))
    glove_labels = ['Index', 'Middle', 'Ring', 'Pinky']

    for ax, col in zip(axes[0], [shape[0] for shape in shapes]):
        ax.set_title(col, fontsize=25, y=1.08, weight='bold')

    for ax, row in zip(axes[:,0], glove_labels):
        ax.set_ylabel(row, rotation=0, fontsize=25, labelpad=50, weight='bold')

    for i_shape in range(len(shapes)):
        name, shape = shapes[i_shape]
        # from IPython import embed
        # embed()
        for i in range(4):
            l1, = axes[i,i_shape].plot(shape[i + 2, :, 0], label='prediction')
            l2, = axes[i,i_shape].plot(shape[i + 2, :, 1], label='sensor')
            if i_shape == 0 and i == 0:
                leg = fig.legend((l1, l2), ('Prediction', 'Sensor'), 'upper left', fontsize=20)
                for legobj in leg.legendHandles:
                    legobj.set_linewidth(5.0)
            axes[i,i_shape].set_ylim([0,1])
    plt.suptitle(title, fontsize=30, weight='bold')



green_cyl_times = [675604, 682190]
orange_step_times = [695373, 701963]
green_step_times = [767756, 774347]
orange_cyl_times = [741391, 747983]
times = [green_cyl_times, orange_step_times, green_step_times, orange_cyl_times]
names = ['Green Cyl', 'Orange Step', 'Green Step', 'Orange Cyl']



for input_type in ['good_subset', 'without_glove']:

    for i in range(4):
        shape = get_trial(input_type, times[i])
        plot_all(names[i], shape)
        filename = '../pictures/plots/' + names[i].replace(' ', '_') + '_' + input_type + '.pdf'
        plt.savefig(filename, dpi=100)
        print('Saving ' + filename)
