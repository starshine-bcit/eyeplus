import sys
import matplotlib
matplotlib.use('QtAgg')

from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class twodgazescatter(FigureCanvasQTAgg):
    def __init__(self, width, height, parent=None, dpi=100):
        self.plt = plt
        self.fig = self.plt.figure(figsize=(width, height))
        super(twodgazescatter, self).__init__(self.fig)
    
    def plotify(self, x_list, y_list):
        x = np.array(x_list)
        y = np.array(y_list)

        self.plt.scatter(x, y, color='cyan',s=.1)

        # self.plt.bar(x, y, color='maroon',
        #         width=0.4)

        self.plt.xlabel("X")
        self.plt.ylabel("Y")
        self.plt.title("2D gaze Scatter Plot")
