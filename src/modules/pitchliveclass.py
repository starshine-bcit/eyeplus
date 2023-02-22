import sys
import matplotlib
matplotlib.use('QtAgg')

from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class pitchlive(FigureCanvasQTAgg):
    def __init__(self, width, height, parent=None, dpi=100):
        self.plt = plt
        self.fig = self.plt.figure(figsize=(width, height))
        super(pitchlive, self).__init__(self.fig)
    
    def plotify(self, x_list, y_list):
        x = np.array(x_list)
        y = np.array(y_list)

        ax = plt.axes()
        xs = [i for i in range(0, len(y_list), 100)]
        self.plt.xlabel("X")
        self.plt.ylabel("Y")
        self.plt.title("live pitch Scatter Plot")
        for i in range(0, len(y_list), 1000):
            self.plt.ylim(-15,25)
            self.plt.scatter(i, y[i])
            self.plt.plot(i, y[i])
            self.plt.pause(0.01)
        


