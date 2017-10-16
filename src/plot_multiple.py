import numpy as np
import matplotlib.pyplot as plt

def prepare_data(d):
    d = np.concatenate(tuple(d[:, i*2:i*2+2].reshape(1,-1,2) for i in range(6)))
    d[:,:,0] *= .001
    return d

def calc_error(d, the_return):
    Errors = []
    for i in range(10):
        Errors.append(np.sqrt((d[2:6, l*i + cut_off: l*i + the_return_cut_off, 0] - the_return[2:6, cut_off:the_return_cut_off,0])**2))
    return Errors

print('Loading Data')

the_return = np.load('../data/true_return_trials/for_all.npy')
print('Loaded the_return')
all_data = np.load('results_of_learning/multiple/results_of_all_long_train_all_signals_multiple.npy')
print('Loaded all_data')
finger_data = np.load('results_of_learning/multiple/results_of_fingers_long_train_all_signals_multiple.npy')
print('Loaded finger_data')
camera_data = np.load('results_of_learning/multiple/results_of_camera_long_train_all_signals_multiple.npy')
print('Loaded camera_data')

print('Done Load\nPreparing data')

all_data = prepare_data(all_data)
finger_data = prepare_data(finger_data)
camera_data = prepare_data(camera_data)

print('Done preparing data')

l = all_data.shape[0]
l /= 10
cut_off = 662581
the_return_cut_off = 840000


DATA = [camera_data, finger_data, all_data]
green_cyl_times = [623177, 629770]#[787659, 794244]
orange_step_times = [702126, 708717]
green_step_times = [807428, 814020]
orange_cyl_times = [754798, 761299]
times = [green_cyl_times, orange_step_times, green_step_times, orange_cyl_times]
names = ['Green Cyl', 'Orange Step', 'Green Step', 'Orange Cyl']
blues = ['red', '#07C4EA', '#35B5FF', '#14A8FF', '#5075EA', '#3A4EFF', '#4C40E8', '#004CD1', '#1D10CE','#0000C6']#['#00CDFF', '#07C4EA', '#35B5FF', '#14A8FF', '#5075EA', '#3A4EFF', '#4C40E8', '#004CD1', '#1D10CE','#0000C6']


for i_name in range(len(names)):
    name = names[i_name]

    fig, axes = plt.subplots(4,3, sharex='col', sharey='row', figsize=(20,14))
    glove_labels = ['Index', 'Middle', 'Ring', 'Pinky']

    for ax, col in zip(axes[0], ['Color Only', 'Fingers Only', 'All']):
        ax.set_title(col, fontsize=25, y = 1.08, weight='bold')

    for ax, row in zip(axes[:,0], glove_labels):
        ax.set_ylabel(row, rotation=0, fontsize=25, labelpad=50, weight='bold')
    for i_data in range(3):
        data = DATA[i_data]

        for i_plot in range(4):
            lines = []
            for i_data_loop in range(10):
                l1, = axes[i_plot, i_data].plot(data[i_plot+2, 846540*i_data_loop + times[i_name][0]: 846540*i_data_loop + times[i_name][1], 0] + .001*i_data_loop, label='Prediction ' + str(i_data_loop+1), color=blues[i_data_loop])
                lines.append(l1)

            l2, = axes[i_plot, i_data].plot(data[i_plot + 2, times[i_name][0]: times[i_name][1], 1], label='Sensor', color='#DB733F')
            lines.append(l2)
            l3, = axes[i_plot, i_data].plot(the_return[i_plot + 2, times[i_name][0]:times[i_name][1], 0], label='True Return', color='#9AB503')
            lines.append(l3)
            if i_plot == 0:
                leg = fig.legend(tuple(lines), tuple(['Prediction ' + str(data_iter+1) for data_iter in range(10)] + ['Sensor', 'True Return']), 'upper left', fontsize=20)
                for legobj in leg.legendHandles:
                    legobj.set_linewidth(5.)
                axes[i_plot,0].set_ylim([0,1])

    plt.subplots_adjust(left=0.22)
    plt.text(0.5, 0.96, name, fontsize=30, transform=plt.gcf().transFigure)
    plt.text(0.5, 0.025, 'Timesteps', fontsize=30, transform=plt.gcf().transFigure)
    plt.text(0.025, 0.5, 'Values', fontsize=30, transform=plt.gcf().transFigure)
    plt.show()


# All_Errors = calc_error(all_data, the_return)
# Finger_Errors = calc_error(finger_data, the_return)
# Camera_Errors = calc_error(camera_data, the_return)
