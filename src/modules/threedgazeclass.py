import sys
import matplotlib
matplotlib.use('QtAgg')
from PyQt6 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class threedgazeclass(FigureCanvasQTAgg):
    def __init__(self, width, height, parent=None, dpi=100):
        self.plt = plt
        self.fig = self.plt.figure(figsize=(width, height))
        super(threedgazeclass, self).__init__(self.fig)
    
    def plotify(self, data):
        x = np.array(data['x_list'])
        y = np.array(data['y_list'])
        z = np.array(data['z_list'])

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        # self.plt.scatter(x, y, color='cyan',s=.1)
        self.ax.scatter(x, y, z, s=.1, color='cyan')
        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        # self.ax.set_zlabel('Z Label')
        self.ax.set_title('3D Accelerometer Scatterplot')
    
