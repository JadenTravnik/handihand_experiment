import numpy as np
import matplotlib.pyplot as plt
import glob

Etas = [.001, .005, .01, .025, .05, .075, .1, .125, .2, .3, .4, .6]

colors = {'all': plt.cm.Blues(np.linspace(0,1,len(Etas))),
          'fingers': plt.cm.Greens(np.linspace(0,1,len(Etas))),
          'camera': plt.cm.Reds(np.linspace(0,1,len(Etas)))}

def parse_data(d):
    d = np.concatenate(tuple(d[:,i*2:i*2+2].reshape(1,-1,2) for i in range(d.shape[1]/2)))
    d[:,:,0] *= .001
    return d

cut_off, the_return_cut_off = 662581, 840000

finger = 3
for input_setting in ['camera', 'fingers', 'all']:
    for i_eta in range(len(Etas)):
        for i_seed in range(10):
	    filename = 'results_of_learning/eta_sweep_normalized/results_of_' + input_setting + '_all_signals_eta_' + str(Etas[i_eta]) + '_' + str(i_seed) + '.npy'
            try:
                data = np.load(filename)
                data = parse_data(data)
                if i_seed == 0:
                    plt.plot(data[finger, cut_off:the_return_cut_off, 0], label=input_setting + ' Eta ' + str(Etas[i_eta]), color=colors[input_setting][i_eta])
		    print('plotting ' + filename)
                else:
                    plt.plot(data[finger, cut_off:the_return_cut_off, 0], color=colors[input_setting][i_eta])
		    print('plotting ' + filename)
            except:
		print('Error with ' + filename)
                pass

plt.plot(data[finger, cut_off:the_return_cut_off, 1], color='black', label='sensor')

plt.legend(ncol=3)
plt.xlabel('Timesteps')
plt.ylabel('Value')
plt.title('Middle Finger Predictions')
plt.show()




