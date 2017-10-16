import numpy as np
import matplotlib.pyplot as plt

data = np.zeros(5000)
data[1000:1500] = 1
data[3000:3500] = 1

Traces = []

t9, t99, t999 = 0., 0., 0.
for i in range(5000):
    t9 *= .9
    t99 *= .99
    t999 *= .999
    t9 += data[i]
    t99 += data[i]
    t999 += data[i]
    Traces.append([t9, t99, t999])

Traces = np.array(Traces)


Traces[:, 0] *= .1
Traces[:, 1] *= .01
Traces[:, 2] *= .001

plt.plot(data, label='Signal', color='black', linewidth=3)
plt.plot(Traces[:,0], label='Trace Decay = .9', color='#C41F1F', linewidth=3)
plt.plot(Traces[:,1], label='Trace Decay = .99', color='#56A823', linewidth=3)
plt.plot(Traces[:,2], label='Trace Decay = .999', color='#1D69BA', linewidth=3)
plt.legend()
plt.xlabel('Steps', fontweight='bold')
plt.ylabel('Values', rotation=0, fontweight='bold')
plt.title('Trace Example', fontsize=30, fontweight='bold')
plt.show()
