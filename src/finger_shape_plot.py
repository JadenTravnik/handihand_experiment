import numpy as np
from scipy.stats import ttest_ind
import matplotlib
font = {'weight' : 'bold',
        'size'   : 25}

matplotlib.rc('font', **font)

from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches

import matplotlib.pyplot as plt

orange_step_time_arr =  [[662581, 669173],
                        [702126, 708717],
                        [767888, 774477],
                        [774477, 781067],
                        [781067, 794244],
                        [800836, 807428],
                        [814020, 820611],
                        [833793, 840384]]

green_step_time_arr = [[669173, 675764],
                    [695535, 702126],
                    [708717, 715308],
                    [715308, 721898],
                    [728489, 735081],
                    [794244, 800836],
                    [807428, 814020]]

green_cyl_time_arr = [[688948, 695535],
                    [748265, 754798],
                    [761299, 767888]]

orange_cyl_time_arr = [[675764, 682356],
                    [682356, 688948],
                    [721898, 728489],
                    [735081, 741673],
                    [741673, 748265],
                    [754798, 761299],
                    [820611, 827202],
                    [827202, 833793]]

all_time_arrs = [green_cyl_time_arr, orange_step_time_arr, green_step_time_arr, orange_cyl_time_arr]

def get_return():
    # the_return =  np.array([np.load('../data/true_return_trials/for_' + str(i) + '.npy') for i in range(17,23)])
    the_return =  np.load('../data/true_return_trials/for_all.npy')
    return the_return

def get_trial(filename_suffix, the_return):
    data = []
    nice_names = ['Color Only', 'Fingers Only', 'All']
    file_names = ['_colors_', '_fingers_', '_']
    signal_names = ['fingers', 'camera', 'all']

    Errors = []
    T = []
    for i in range(3):
        # sub_data = np.array([np.load('results_of_learning_old/results_of_' + str(i_sensor) + file_names[i] + filename_suffix + '.npy') for i_sensor in range(17,23)])
        sub_data = np.load('results_of_learning/long_train/results_of_' + signal_names[i] + '_long_train' + filename_suffix + '.npy')
        sub_data = np.concatenate(tuple(sub_data[:,i*2:i*2+2].reshape(1,-1,2) for i in range(sub_data.shape[1]/2)))

        try:
            assert(sub_data.shape==the_return.shape)
        except:
            print(sub_data.shape, the_return.shape)
            raise

        sub_data[:,:,0] *= .001
        shape_errors = [[] for k in range(4)]
        for i_time_arr in range(4):
            time_arr = all_time_arrs[i_time_arr]
            for i_time_line in range(len(time_arr)):
                shape_errors[i_time_arr].append( \
                    np.sqrt((\
                        sub_data[2:6, time_arr[i_time_line][0]:time_arr[i_time_line][1], 0] \
                        - \
                        the_return[2:6,time_arr[i_time_line][0]:time_arr[i_time_line][1],0])\
                    **2))
            shape_errors[i_time_arr] = np.hstack(shape_errors[i_time_arr])


        Errors.append(shape_errors)

    return Errors

def get_return():
    # the_return =  np.array([np.load('../data/true_return_trials/for_' + str(i) + '.npy') for i in range(17,23)])
    the_return =  np.load('../data/true_return_trials/for_all.npy')
    return the_return


def plot_all_boxes(input_type, shape):
    glove_labels = ['Index', 'Middle', 'Ring', 'Pinky']
    colors = ['#3393C6', '#F2A45C', '#ABE188']
    nice_names = ['Color Only', 'Fingers Only', 'All']
    shape_names = ['Green Cyl', 'Orange Step', 'Green Step', 'Orange Cyl']

    for i_finger in range(4):
        fig, axes = plt.subplots(figsize=(20, 14))
        axes.set_ylim([0,.5])
        p = []
        e = []
        patch_colors = []
        labels = []

        for i_sensor in range(len(nice_names)):
            for i_shape in range(4):
                error = shape[i_sensor][i_shape][i_finger]
                e.append(error)
                p.append(i_shape*5 + i_sensor)
                patch_colors.append(colors[i_sensor])
                if i_sensor == 1:
                    labels.append(shape_names[i_shape])
                else:
                    labels.append('')

        bplot = axes.boxplot(e, positions=p, patch_artist=True,
                            labels=labels,
                            boxprops=dict(linewidth=3),
                            medianprops = dict(linewidth=2, color='firebrick'),
                            meanprops = dict(linestyle='--', linewidth=2.5, color='black'),
                            meanline=True,
                            showmeans=True,
                            showfliers=False)


        for patch, color in zip(bplot['boxes'], patch_colors):
            patch.set_facecolor(color)

        axes.set_ylabel('Root\nSquared\nError', rotation=0, fontsize=25, labelpad=50, weight='bold')
        axes.set_xlabel('Shape', fontsize=25, labelpad=50, weight='bold')

        #Create custom artists
        artists = [plt.Line2D((0,1),(0,0), color='#3393C6'),
                   plt.Line2D((0,1),(0,0), color='#F2A45C'),
                   plt.Line2D((0,1),(0,0), color='#ABE188'),
                   plt.Line2D((0,1),(0,0), color='firebrick'),
                   plt.Line2D((0,1),(0,0), color='black', linestyle='--')]

        #Create legend from custom artist/label lists
        leg = axes.legend(artists, nice_names + ['Median', 'Mean'],
                          loc='upper left',
                          prop={'size': 25})

        for legobj in leg.legendHandles:
            legobj.set_linewidth(10.0)

        plt.suptitle('Distribution of Root Squared Error between True Return and Predictions\nafter Learning', fontsize=30, weight='bold')
        filename = '../pictures/plots/' + input_type + '_' + glove_labels[i_finger] + '_box_with_lim.pdf'
        plt.savefig(filename, dpi=100)
        print('Saving ' + filename)

the_return = get_return()

for input_type in ['', '_all_signals']: #['good_subset', 'without_glove']:
    shape = get_trial(input_type, the_return)
    plot_all_boxes(input_type, shape)
