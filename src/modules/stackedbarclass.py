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


class TotalUpDown_stacked(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)

    def plot(self, data):
        self.ax.clear()
        self.data = data
        y_ticks = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        x = ['Up and down']
        up = data['up_count']
        down = data['down_count']
        mean_pitch = data['mean_pitch']
        total = data['total']
        y1 = [mean_pitch, up/total]
        y2 = [0,down/total]
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels([str(x) for x in y_ticks])
        self.ax.set_title('Mean value of Pitch versus the stacked percentage of Up Vs. Down')
        #self.ax.bar(x, y1, color=['mediumseagreen', 'firebrick'])
        self.ax.bar(x, y1)
        self.ax.bar(x, y2, bottom=y1)
        self.fig.canvas.draw()
