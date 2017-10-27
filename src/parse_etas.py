import numpy as np
import matplotlib.pyplot as plt
import glob

names = glob.glob('results_of_learning/eta_sweep_normalized/*.npy')
#Etas = [.005, .01, .015, .02, .024, .025, .026, .027, .028, .029, .03, .035, .04, .045, .05, \
 #       .055, .06, .065, .07, .075, .08, .085, .09, .095, .1, \
  #      .105, .11, .115, .12, .125, .13, .135, .14, .145, .15]

Etas = [.001, .005, .01, .025, .05, .075, .1, .125, .2, .3, .4, .6]

Res = {'camera': [[] for e in Etas], \
       'fingers': [[] for e in Etas],\
       'all':[[] for e in Etas]}


the_return = np.load('../data/true_return/for_all.npy')

def calc_error(d, the_return):
    cut_off, the_return_cut_off = 662581, 840000
    error = np.sqrt((d[2:6, cut_off:the_return_cut_off, 0] - the_return[2:6,cut_off:the_return_cut_off, 0])**2)
    res = [np.mean(error, axis=1), np.std(error, axis=1), np.median(error, axis=1)]
    return res

def parse_data(d):
    d = np.concatenate(tuple(d[:,i*2:i*2+2].reshape(1,-1,2) for i in range(d.shape[1]/2)))
    d[:,:,0] *= .001
    return d


for i in range(len(names)):
    s = ''
    try:
        if not i % 10:
            print(str(round(i/float(len(names)),3)*100.) + '%')
        n = names[i]
        d = n.split('_')
        data_type = d[6]
        eta_index = Etas.index(float(d[10]))
	s += 'parsing data\n'
        data = parse_data(np.load(n))
	s += 'calculating error\n'
        err = calc_error(data, the_return)
        if data_type not in ['camera', 'fingers', 'all']:
            print(d,data_type,n)
            exit()
	s += 'appending to Res[' + data_type + '][' + str(eta_index) + ']\n'
        Res[data_type][eta_index].append(err)
    except Exception as e:
	print(e)
	print(s)
        print(data_type, eta_index, d,n)
        pass

Res['camera'] = np.array(Res['camera'])
Res['fingers'] = np.array(Res['fingers'])
Res['all'] = np.array(Res['all'])

for i in ['camera','fingers','all']:
    np.save(i + '_eta_sweep_data', Res[i])


#for i in ['camera','fingers','all']:
#    Res[i] = np.mean(Res[i], axis=1)
#    plt.plot(Res[i][:, 0], label=i)


#plt.show()


