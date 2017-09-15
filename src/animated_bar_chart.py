import matplotlib.pyplot as plt
import numpy as np

class DynamicBar():

    def __init__(self, y_data):
        plt.ion()
        self.figure, self.ax = plt.subplots()
        self.ax.set_autoscaley_on(True)
        self.ax.grid()
        self.bars = self.ax.bar(range(len(y_data)), y_data)
        for i in self.bars.__dict__:
            print(i)
        self.update(y_data)

    def update(self, _y):
        for i in range(len(_y)):
            self.bars.patches[i].set_height(_y[i])
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

db = DynamicBar([1,2,3])
for i in np.arange(0,10, 0.01):
    db.update([np.sin(i), np.sin(2*i), np.sin(3*i)])
