
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl

plt.style.use('ggplot')
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8


class BasicCanvas(FigureCanvasQTAgg):
    def __init__(self, width: int, height: int, dpi: float):
        px = 1/dpi
        self.fig = Figure(figsize=(width*px, height*px), dpi=dpi)
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot()


class TotalUpDown(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)

    def plot(self, data: dict):
        self.ax.clear()
        self.data = data
        y_ticks = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        x = ['Up', 'Down']
        up = data['up_count']
        down = data['down_count']
        total = data['total']
        y = [up/total, down/total]
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels([str(x) for x in y_ticks])
        self.ax.set_title('Proportion of Time Looking Up vs. Down')
        self.ax.bar(x, y, color=['mediumseagreen', 'firebrick'])
        self.fig.canvas.draw()


class CumulativeUpDown(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)
        self.ax.margins(0.5)

    def plot(self, data: dict, timestamp: float):
        self.ax.clear()
        self.data = data
        y_ticks = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        x = ['Up', 'Down']
        up = data['up_count']
        down = data['down_count']
        total = data['total']
        y = [up/total, down/total]
        self.ax.set_ylim(0, 0.8)
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels([str(x) for x in y_ticks])
        self.ax.set_title(f'Proportion Up/Down at time {timestamp:.1f}')
        self.ax.bar(x, y, color=['mediumseagreen', 'firebrick'])
        self.fig.canvas.draw()
