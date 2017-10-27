import numpy as np
from scipy.stats import ttest_ind
import matplotlib
font = {'weight' : 'bold',
        'size'   : 25}

matplotlib.rc('font', **font)

from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches

import matplotlib.pyplot as plt

def get_trial(filename_suffix, times, the_return):
    data = []
    nice_names = ['Color Only', 'Fingers Only', 'All']
    file_names = ['_colors_', '_fingers_', '_']
    signal_names = ['fingers', 'camera', 'all']

    cut_off = 662581
    the_return_cut_off = 840000 # 662581 #the_return.shape[1]
    # times = [cut_off, the_return_cut_off]
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
        sub_error = np.sqrt((sub_data[2:6, cut_off:the_return_cut_off, 0]-the_return[2:6,cut_off:the_return_cut_off,0])**2)
        T.append(ttest_ind(np.diff(sub_data[2:6, cut_off:the_return_cut_off, 0], axis=1), np.diff(the_return[2:6,cut_off:the_return_cut_off,0], axis=1), axis=1, equal_var=True))
        Errors.append(sub_error)
        sub_data = sub_data[:, times[0]:times[1], :]
        data.append((nice_names[i], sub_data, sub_error, the_return[:, times[0]:times[1], 0]))

    # T = [ttest_ind(Errors[0], Errors[1], axis=1),
    #      ttest_ind(Errors[0], Errors[2], axis=1),
    #      ttest_ind(Errors[1], Errors[2], axis=1)]
    # E = np.hstack(Errors)

    # from IPython import embed
    # embed()

    # fig, ax = plt.subplots(figsize=(20,14))
    # ax.bar(np.arange(4)*4, cohen[0], color='red', label='Color Only and Fingers Only')
    # ax.bar(np.arange(4)*4 + 1, cohen[1], color='blue', label='Color Only and All')
    # ax.bar(np.arange(4)*4 + 2, cohen[2], color='green', label='Fingers Only and All')
    # ax.plot((-2, 20), (.2, .2), color='black', linestyle='--', linewidth=2, label='Small Effect')
    # ax.plot((-2, 20), (.5, .5), 'k', linewidth=2, label='Medium Effect')
    # ax.legend()
    # ax.text(0.175, .94, 'Cohen\'s D Between the Means of the Distributions of Error', fontsize=30, transform=plt.gcf().transFigure)
    # ax.text(.4, .025, 'Glove Potentiometers', fontsize=30, transform=plt.gcf().transFigure)
    # plt.xticks(np.arange(4)*4 + 1, ['Index', 'Middle', 'Ring', 'Pinky'])
    # ax.set_ylim([0,1])
    # ax.set_xlim([-1,15])
    # ax.text(0.025, 0.5, 'Cohen\'s D\nValues', transform=plt.gcf().transFigure)
    # plt.subplots_adjust(left=.175)
    # plt.show()


    return data, T

def get_return():
    # the_return =  np.array([np.load('../data/true_return_trials/for_' + str(i) + '.npy') for i in range(17,23)])
    the_return =  np.load('../data/true_return_trials/for_all.npy')
    return the_return


def plot_all_lines(title, shapes):
    fig, axes = plt.subplots(4, 3, sharex='col', sharey='row', figsize=(20, 14))
    glove_labels = ['Index', 'Middle', 'Ring', 'Pinky']

    for ax, col in zip(axes[0], [shape[0] for shape in shapes]):
        ax.set_title(col, fontsize=25, y=1.08, weight='bold')

    for ax, row in zip(axes[:,0], glove_labels):
        ax.set_ylabel(row, rotation=0, fontsize=25, labelpad=50, weight='bold')

    for i_shape in range(len(shapes)):
        name, shape, _, _return = shapes[i_shape]
        # from IPython import embed
        # embed()
        for i in range(4):
            l1, = axes[i,i_shape].plot(shape[i + 2, :, 0], label='Prediction')
            l2, = axes[i,i_shape].plot(shape[i + 2, :, 1], label='Sensor')
            l3, = axes[i,i_shape].plot(_return[i + 2, :], label='True Return')
            if i_shape == 0 and i == 0:
                leg = fig.legend((l1, l2, l3), ('Prediction', 'Sensor', 'True Return'), 'upper left', fontsize=20)
                for legobj in leg.legendHandles:
                    legobj.set_linewidth(5.0)
            axes[i,i_shape].set_ylim([0,1])
    plt.subplots_adjust(left=0.22)
    plt.text(0.5, 0.96, title, fontsize=30, transform=plt.gcf().transFigure)
    plt.text(0.5, 0.025, 'Timesteps', fontsize=30, transform=plt.gcf().transFigure)
    plt.text(0.025, 0.5, 'Values', fontsize=30, transform=plt.gcf().transFigure)

def plot_all_boxes(input_type, shapes):
    glove_labels = ['Index', 'Middle', 'Ring', 'Pinky']
    glove_labels = [b for i in glove_labels for b in [i]*3]
    nice_names = ['Color Only', 'Fingers Only', 'All']
    fig, axes = plt.subplots(figsize=(20, 14))

    axes.set_ylim([0,.5])
    e = []
    colors = ['#3393C6']*4 + ['#F2A45C']*4 + ['#ABE188'] * 4
    p = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14]
    labels = ['', '', '', '', 'Index', 'Middle', 'Ring', 'Pinky', '', '', '', '']

    for i_shape in range(len(shapes)):
        _, _, error, _ = shapes[i_shape]
        e.extend(error[:, ::1].tolist())
        # axes.boxplot(error[:, ::1].tolist(), positions=p)
    bplot = axes.boxplot(e, positions=p, patch_artist=True,
                        labels=labels,
                        boxprops=dict(linewidth=3),
                        medianprops = dict(linewidth=2, color='firebrick'),
                        meanprops = dict(linestyle='--', linewidth=2.5, color='black'),
                        meanline=True,
                        showmeans=True,
                        showfliers=False)


    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    axes.set_ylabel('Root\nSquared\nError', rotation=0, fontsize=25, labelpad=50, weight='bold')
    axes.set_xlabel('Glove Potentiometers', fontsize=25, labelpad=50, weight='bold')

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

def plot_all_bars(input_type, shapes):
    glove_labels = ['Index', 'Middle', 'Ring', 'Pinky']
    nice_names = ['Color Only', 'Fingers Only', 'All']
    colors = ['#3393C6', '#F2A45C', '#ABE188']
    fig, axes = plt.subplots(figsize=(20, 14))
    for i_shape in range(len(shapes)):

        _, _, error, _ = shapes[i_shape]

        axes.bar(np.arange(4)*4 + i_shape, np.mean(error,axis=1), yerr=np.std(error,axis=1), color=colors[i_shape])
        # axes.set_ylim([0,.5])
        axes.set_title(nice_names[i_shape])

    leg = plt.legend(handles=[mpatches.Patch(color='#3393C6', label='Color Only'),
                   mpatches.Patch(color='#F2A45C', label='Fingers Only'),
                   mpatches.Patch(color='#ABE188', label='All')],
                   loc='upper left')
    for legobj in leg.legendHandles:
        legobj.set_linewidth(5.0)

    plt.suptitle('Error comparison', fontsize=30, weight='bold')

green_cyl_times = [787659, 794244]
orange_step_times = [702126, 708717]
green_step_times = [807428, 814020]
orange_cyl_times = [754798, 761299]
times = [green_cyl_times, orange_step_times, green_step_times, orange_cyl_times]
names = ['Green Cyl', 'Orange Step', 'Green Step', 'Orange Cyl']
the_return = get_return()


for input_type in ['', '_all_signals']: #['good_subset', 'without_glove']:
    shape, T = [], []
    for i in range(4):
        shape, T = get_trial(input_type, times[i], the_return)
        # plot_all_lines(names[i], shape)
        # filename = '../pictures/plots/' + names[i].replace(' ', '_') + '_' + input_type + '_all_signals.pdf'
        # plt.savefig(filename, dpi=100)
        # print('Saving ' + filename)

    # for t, p in T:
    #     print(t,p)

    plot_all_boxes(input_type, shape)
    filename = '../pictures/plots/' + input_type + '_box_with_lim.pdf'
    plt.savefig(filename, dpi=100)
    print('Saving ' + filename)

    # plot_all_bars(input_type, shape)
    # filename = '../pictures/plots/' + input_type + '_bar_all_signals.pdf'
    # plt.savefig(filename, dpi=100)
    # print('Saving ' + filename)
