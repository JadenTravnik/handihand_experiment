from glob import glob
import sys
import numpy as np

names = glob(sys.argv[1] + '*.npy')

g_names = ['../data/trials/green-cyl_8.npy',
        '../data/trials/orange-cyl_20.npy',
        '../data/trials/orange-step_16.npy',
        '../data/trials/green-step_21.npy']

#('../data/trials/green-cyl_8.npy', 675604, 682190, 6586)
#('../data/trials/orange-step_16.npy', 695373, 701963, 6590)
#('../data/trials/orange-cyl_20.npy', 741391, 747983, 6592)
#('../data/trials/green-step_21.npy', 767756, 774347, 6591)


mins = np.ones(24)*10000
maxs = np.ones(24)*-10000

t = 0
for name in names:
    data = np.load(name)
    if name in g_names:
        print(name, t, t + data.shape[0], data.shape[0])
    t += data.shape[0]
