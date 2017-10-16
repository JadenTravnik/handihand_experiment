import numpy as np
import horde

gamma = .999

def normalize(arr):
    arr -= np.min(arr, axis=0)
    arr /= np.max(arr, axis=0)
    return n_arr

data = np.load('results_of_learning/results_of_fingers_long_train.npy')
data = np.concatenate(tuple(data[:,i*2:i*2+2].reshape(1,-1,2) for i in range(data.shape[1]/2)))
for i in range(6):
    print(i)
    result = horde.calculate_discounted_return_backwards(data[i, :, 1], gamma)
    data[i, :len(result),0] = result

data = data[:len(result)]
np.save('../data/true_return_trials/for_all', data)
