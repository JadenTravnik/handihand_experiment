import numpy as np
import matplotlib.pyplot as plt

Etas = np.array([0.01, .025, .05, 0.1])
Prototypes = [8000] #np.arange(1000, 10000, 1000)
Dims = [8] #np.array([1,2,4,8])

def calcAvgDist(p, eta):
    dist = []
    c = int(p.shape[0]*eta)
    for i in range(p.shape[0]):
        D = p - p[i]
        D = np.sqrt(sum(D.T**2))
        d = np.partition(D, c, axis=0)[:c]
        dist.append(np.mean(d))
    return np.mean(dist)

def runall(Prototypes, Etas, Dims, iterations = 100):
    Data = []
    for i in range(len(Prototypes)):
        Data.append([])
        for j in range(len(Dims)):
            Data[i].append([])
            for k in range(len(Etas)):
                Data[i][j].append([])
                for l in range(iterations):
                    if not l % 5:
                        print(str(Prototypes[i]) + ' ' + str(Dims[j]) + ' ' + str(Etas[k]) + ' ' + str(l) + '/' + str(iterations))

                    Data[i][j][k].append(calcAvgDist(np.random.random((Prototypes[i], Dims[j])), Etas[k]))


    return np.array(Data)

# data = runall(Prototypes, Etas, Dims)
data = np.load('KanervaCodingDistanceDistribution.npy')

fig, axes = plt.subplots(1, 4, figsize=(20,14), sharey=True)
axes[0].boxplot(data[-1, 0].T)
axes[1].boxplot(data[-1, 1].T)
axes[2].boxplot(data[-1,2].T)
axes[3].boxplot(data[-1,3].T)
for i in range(4):
    axes[i].set_xlabel('Eta', fontsize=30)

for i in range(4):
    axes[i].set_title(str(2**i) + ' Dimension' + ''.join(set('s'*i)), fontsize=30)
for i in range(4):
    axes[i].set_xticklabels(['0.01', '0.025', '0.05', '0.1'], fontsize=15)

for i in range(4):
    for tick in axes[i].get_yaxis().get_major_ticks():
        tick.label.set_fontsize(15)
axes[0].set_ylabel('Mean\nEuclidian\nDistance', rotation=0, labelpad=60, fontsize=20)
txt = plt.text(0.175, 0.96, 'Mean Euclidian Distance Between Activated Prototypes', fontsize=35, transform=plt.gcf().transFigure)
plt.savefig('Kanerva_Coding_Distance_Distributions.pdf')
