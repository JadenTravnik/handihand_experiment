from dynamic_plotter import DynamicPlot, DynamicBar
from glob import glob
import sys
import numpy as np
from horde import OnPolicyGVF
from representation import SelectiveKanervaCoder

names = glob(sys.argv[1] + '*.npy')


hand_labels = ['time', 'button', 'thumb rot D0', 'thumb flex D1P', 'fake',
                'thumb flex D1D', 'index D2P', 'index D2I', 'middle D3P', 'middle D3I',
                'ring D4P', 'pinky D5P', 'FSR thumb', 'FSR index', 'FSR middle',
                'FSR ring', 'FSR pinky'] #16
glove_labels = ['Thumb Ad/Ab', 'Thumb F/E', 'Index', 'Middle', 'Ring', 'Pinky'] # 22
cam_labels = ['blue', 'green', 'red'] # 25
hand_labels.extend(glove_labels)
hand_labels.extend(cam_labels)

# D0  643	383
# D1P	722	536
# D1D	687	508
# D2P	734	511
# D2I	759	505
# D3P	264	493
# D3I	753	523
# D4P	270	523
# D5P	268	455

mins = np.array([0, 0, 350, 500, 0, 550, 550, 500, 400, 500, 300, 300, #hand pots
                0,    0,    0,    0,    0, # hand fsrs
                400, 350, 250, 250, 250, 200, # glove pots
                0,   0,   0]) # cam hist

maxs = np.array([1, 1, 400, 650, 1, 700, 600, 700, 550, 650, 550, 550, # hand pots
                500, 100, 100, 100, 100, # hand fsrs
                850, 900, 650, 950, 950, 950, # glove pots
                255, 255, 255]) # cam hist

ranges = maxs - mins
def normalize(arr, inds):
    n_arr = (arr[inds] - mins[inds])/ranges[inds]
    return n_arr


important_signals = range(23, 26) #[7, 10, 24, 25]

num_features = 8000
skc = SelectiveKanervaCoder(num_features, _dimensions = len(important_signals)*2, _eta = .025, _seed = 2)

#GVFs = [OnPolicyGVF(lamda=0.99, alpha=0.01, numFeatures=num_features) for label in glove_labels] # 6 GVFs, one for each pot on glove
gamma = 0.999

# Z_index = 18 # 19 is hard, 20 also hard
for Z_index in range(17,23):
    gvf = OnPolicyGVF(lamda=0.9, alpha=0.01, numFeatures=num_features)
    test_time = 100000

    # d = DynamicPlot(window_x=75, title='Data View', xlabel='time steps', ylabel='values')
    #
    # d.add_line(hand_labels[Z_index])
    # d.add_line('PRED - ' + hand_labels[Z_index])

    # db = DynamicBar(np.zeros(num_features))

    trace_decay = .999
    traces = np.zeros(len(important_signals))

    t = 0
    speed = 100

    results = []
    for name in names:
        print('loading ' + name)
        data = np.load(name)
        state = normalize(data[0, :], important_signals)

        traces *= trace_decay
        traces += state
        state = state.tolist()
        state.extend(traces*(1-trace_decay))
        phi = skc.getFeatures(state)
        for i in range(data.shape[0]):
            state = normalize(data[i, :], important_signals)
            state = state.tolist()

            traces *= trace_decay
            traces += state
            state.extend(traces*(1-trace_decay))
            plot_data = []

            phi_next = skc.getFeatures(state)
            z = normalize(data[i, :], [Z_index])
            if t > test_time:
                pred = gvf.predict(phi_next)
            else:
                pred = gvf.update(phi, phi_next, z, gamma, gamma)

            results.append([pred, z])

            phi = phi_next

            if not t % 10000:
                print(t)
            # if t > test_time and not i % speed:
            #     # db.update(gvf.w)
            #     plot_data.extend([z, pred*(1.-gamma)])
            #     d.update(t, plot_data)
            t += 1


    np.save('results_of_learning/results_of_' + str(Z_index) + '_colors_without_glove', np.array(results))
