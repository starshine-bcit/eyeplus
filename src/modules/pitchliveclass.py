from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl


plt.style.use('ggplot')
mpl.rcParams['axes.titlesize'] = 10

class BasicCanvas(FigureCanvasQTAgg):
    def __init__(self, width: int, height: int, dpi: float):
        px = 1/dpi
        self.fig = Figure(figsize=(width*px, height*px), dpi=dpi)
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot()

class pitchlive(FigureCanvasQTAgg):
    # def __init__(self, width, height, parent=None, dpi=100):
    #     self.plt = plt
    #     self.fig = self.plt.figure(figsize=(width, height))
    #     super(pitchlive, self).__init__(self.fig)
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)

    def plot(self, data):
        self.ax.clear()
        self.data = data
        y_ticks = [i for i in range (-15,25)]
        y_list = data['y'] 
        x = [i for i in range(0, len(y_list), 100)]

        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels([str(x) for x in y_ticks])
        self.ax.set_title('Live graph of pitch movement values')

        self.ax.scatter(x, y_list)
        self.ax.pause(0.01)
        self.fig.canvas.draw()
    
    # def plotify(self, x_list, y_list):
    #     x = np.array(x_list)
    #     y = np.array(y_list)

    #     ax = plt.axes()
    #     xs = [i for i in range(0, len(y_list), 100)]
    #     self.plt.xlabel("X")
    #     self.plt.ylabel("Y")
    #     self.plt.title("live pitch Scatter Plot")
    #     for i in range(0, len(y_list), 1000):
    #         # self.plt.ylim(-15,25)
    #         self.plt.scatter(i, y[i])
    #         self.plt.plot(i, y[i])
    #         self.plt.pause(0.01)
        


# import sys
# import matplotlib
# matplotlib.use('QtAgg')

# from PyQt6 import QtCore, QtWidgets

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
# import numpy as np

# class pitchlive(FigureCanvasQTAgg):
#     def __init__(self, width, height, parent=None, dpi=100):
#         self.plt = plt
#         self.fig = self.plt.figure(figsize=(width, height))
#         super(pitchlive, self).__init__(self.fig)
    
#     def plotify(self, x_list, y_list):
#         x = np.array(x_list)
#         y = np.array(y_list)

#         ax = plt.axes()
#         xs = [i for i in range(0, len(y_list), 100)]
#         self.plt.xlabel("X")
#         self.plt.ylabel("Y")
#         self.plt.title("live pitch Scatter Plot")
#         for i in range(0, len(y_list), 1000):
#             self.plt.ylim(-15,25)
#             self.plt.scatter(i, y[i])
#             self.plt.plot(i, y[i])
#             self.plt.pause(0.01)
        

