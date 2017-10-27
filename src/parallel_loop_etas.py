from dynamic_plotter import DynamicPlot, DynamicBar
from glob import glob
import sys
import numpy as np
from horde import OnPolicyGVF
from representation import SelectiveKanervaCoder
import time
import multiprocessing as mp

names = glob(sys.argv[1] + '*.npy')

np.random.seed(1)
green_cyl_filenames = [n for n in names if 'green-cyl' in n]
green_step_filenames = [n for n in names if 'green-step' in n]
orange_cyl_filenames = [n for n in names if 'orange-cyl' in n]
orange_step_filenames = [n for n in names if 'orange-step' in n]


np.random.shuffle(green_cyl_filenames)
np.random.shuffle(green_step_filenames)
np.random.shuffle(orange_cyl_filenames)
np.random.shuffle(orange_step_filenames)

num_train_files = 25
train_filenames = green_cyl_filenames[:num_train_files] +\
                  green_step_filenames[:num_train_files] +\
                  orange_cyl_filenames[:num_train_files] +\
                  orange_step_filenames[:num_train_files]

test_filenames = green_cyl_filenames[num_train_files:] +\
                  green_step_filenames[num_train_files:] +\
                  orange_cyl_filenames[num_train_files:] +\
                  orange_step_filenames[num_train_files:]
num_train_files *= 4



np.random.shuffle(train_filenames)
np.random.shuffle(test_filenames)
try:
    assert(len(train_filenames) == 100)
except:
    print(len(train_filenames))
    raise
names = train_filenames + test_filenames

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
# Signals = [('fingers', [7, 10]), ('camera', [24, 25]), ('all', [7, 10, 24, 25])]
Signals = [('fingers', [2,3] + range(4, 17)), ('camera', [23, 24, 25]), ('all', [2,3] + range(4, 17) + [23, 24, 25])]

def normalize(arr, inds):
    n_arr = (arr[inds] - mins[inds])/ranges[inds]
    return n_arr

num_features = 8000
gamma = 0.999
trace_decay = .999

Z_indexes = range(17,23)



num_seeds = 20
#Etas = [.005, .01, .015, .02, .025, .03, .035, .04, .045, .05]
#Etas = [.055, .06, .065, .07, .075, .08, .085, .09, .095, .1, .105, .11, .115, .12, .125, .13, .135, .14, .145, .15]
#Etas = [.024, .026, .027, .028, .029]


#Etas = [.001, .005, .01, .025, .05, .075, .1, .125, .2]
Etas = [.3, .4, .6]

Inputs = []
iteration = 0
for signal_name_pair in Signals:
    signal_name, signals = signal_name_pair
    for i_eta in Etas:
        for i_seed in range(num_seeds):
            Inputs.append(tuple([signal_name, signals, i_eta, i_seed, iteration]))
            iteration += 1

print('Total Iterations ' + str(iteration))

def do_an_iteration(Input):
    start_time = time.time()
    prev_time = time.time()
    times = []

    signal_name, signals, eta, seed, iteration = Input
    print('Starting ' + str(iteration) + '\t' + signal_name + '\t' + str(signals) + '\t' + str(eta) + '\t' + str(seed))
    traces = np.zeros(len(signals))
    skc = SelectiveKanervaCoder(num_features, _dimensions = len(signals)*2, _eta = eta, _seed = seed)
    GVFs = [OnPolicyGVF(lamda=0.9, alpha=0.01, numFeatures=num_features, numActiveFeatures=skc.c) for label in glove_labels] # 6 GVFs, one for each pot on glove
    t = 0
    results = []
    for filename_index in range(len(names)):

        name = names[filename_index]
        data = np.load(name)
        state = normalize(data[0, :], signals)

        traces *= trace_decay
        traces += state
        state = state.tolist()
        state.extend(traces*(1-trace_decay))
        phi = skc.getFeatures(state)
        for i in range(data.shape[0]):

            state = normalize(data[i, :], signals)
            state = state.tolist()

            traces *= trace_decay
            traces += state
            state.extend(traces*(1-trace_decay))

            phi_next = skc.getFeatures(state)
            Z = normalize(data[i, :], Z_indexes)

            preds = []
            if filename_index > num_train_files:
                # Training
                for i_gvf in range(len(GVFs)):
                    pred = GVFs[i_gvf].predict(phi_next)
                    preds.append(pred)
                    preds.append(Z[i_gvf])
            else:
                # Testing
                for i_gvf in range(len(GVFs)):
                    pred = GVFs[i_gvf].update(phi, phi_next, Z[i_gvf], gamma, gamma)
                    preds.append(pred)
                    preds.append(Z[i_gvf])

            assert(len(preds) == 12)
            results.append(preds)

            phi = phi_next

            if not t % 80000:
                times.append(time.time() - prev_time)
                prev_time = time.time()
                print('\t' + str(t) + '\tEta value is ' + str(eta) +\
                      '\tElapsed : ' + str(time.time() - start_time) +\
                      '\tETA for ' + signal_name + ' : ' + str((np.mean(times)/8000.)*(850000.*(len(Etas) - i_eta) - t)))
            t += 1

    new_file_name = 'results_of_learning/eta_sweep_normalized/results_of_' + signal_name + '_all_signals_eta_' + str(eta) + '_' + str(seed)
    print('Saving ' + new_file_name)
    np.save(new_file_name, np.array(results))

total_workers = mp.cpu_count()
num_workers = int(total_workers*.9)

print(str(iteration/num_workers) + ' ' + str(iteration%num_workers))

print('Starting pool')
pool = mp.Pool(processes=num_workers)
pool.map(do_an_iteration, Inputs)
print('Done')
