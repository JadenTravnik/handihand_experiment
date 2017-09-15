from dynamic_plotter import DynamicPlot
from glob import glob
import sys
import numpy as np
names = glob(sys.argv[1] + '*.npy')

d = DynamicPlot(window_x=200, title='Data View', xlabel='time steps', ylabel='values')
for i in range(26):
    d.add_line(str(i))
t = 0
speed = 100
for name in names:
    print('loading ' + name)
    data = np.load(name)

    for i in range(data.shape[0]):
        if not i % speed:
            d.update(t, data[i,1:])
        t += 1
