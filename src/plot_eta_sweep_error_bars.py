import numpy as np
import matplotlib.pyplot as plt
import glob


# names = glob.glob('results_of_learning/eta_sweep/*.npy')

# the_return = np.load('../data/true_return/for_all.npy')

#Etas = [.005, .01, .015, .02, .024, .025, .026, .027, .028, .029, .03, .035, .04, .045, .05, \
#        .055, .06, .065, .07, .075, .08, .085, .09, .095, .1, \
#        .105, .11, .115, .12, .125, .13, .135, .14, .145, .15]

Etas = [0.001, .005, .01, .025, .05, .075, .1, .125, .2, .3, .4, .6]

def calc_error(d, the_return):
    cut_off, the_return_cut_off = 662581, 840000
    error = np.sqrt((d[2:6, cut_off:the_return_cut_off, 0] - the_return[2:6,cut_off:the_return_cut_off, 0])**2)
    res = [np.mean(error, axis=1), np.std(error, axis=1), np.median(error, axis=1)]
    return res
 
def parse_data(d):
    d = np.concatenate(tuple(d[:,i*2:i*2+2].reshape(1,-1,2) for i in range(d.shape[1]/2)))
    d[:,:,0] *= .001
    return d

divisor = np.sqrt(840000 - 662581.)


Res = {'camera': [], 'fingers': [], 'all': []}
for i in ['camera', 'fingers', 'all']:
    try:
    	Res[i] = np.load(i + '_eta_sweep_data.npy')
	means = [np.mean(np.array(Res[i][j]), axis = 0) for j in range(len(Res[i]))]
    	Res[i] = np.array(means)
    except:
        print(i, Res[i].shape, np.array(Res[i][0]).shape, np.array(Res[i][1]).shape, np.array(Res[i][2]).shape, np.array(Res[i][3]).shape, np.array(Res[i][4]).shape, np.array(Res[i][5]).shape, np.array(Res[i][6]).shape)

finger_names = ['','Middle', 'Ring', 'Pinky']

#print(len(Etas), len(Res['all'][:,0,3]), len(Res['all'][:,1,3]))
for finger in range(1,4):
    plt.errorbar(Etas, Res['all'][:,0,finger], Res['all'][:,1,finger]/divisor, linestyle='None', marker='^', color='green', label='All')
    plt.errorbar(Etas, Res['fingers'][:,0,finger], Res['fingers'][:,1,finger]/divisor, linestyle='None', marker='^', color='red', label='Fingers Only')
    plt.errorbar(Etas, Res['camera'][:,0,finger], Res['camera'][:,1,finger]/divisor, linestyle='None', marker='^', color='blue', label='Color Only')
    plt.xlim([0.0005,1])
    plt.xscale('log')
    title = finger_names[finger] + ' Potentiometer - Mean and Standard Error of Error Distribution of Eta Sweep'
    plt.title(title)
    plt.xlabel('Eta')
    plt.ylabel('Root\nSquared Error', rotation=0)
    plt.legend()
    plt.savefig(title.replace(' ', '_'))
    plt.clf()
