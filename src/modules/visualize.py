
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

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


class PitchLive(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)
        self._pause = False
        self.current_timestamp = 0.0

    @property
    def is_paused(self) -> bool:
        return self._pause

    def _init_scatter(self):
        self.line, = self.ax.plot(self.x, self.y)
        return self.line,

    def _draw_next_frame(self, frame: float):
        if self.current_timestamp > 10:
            x_low = self.current_timestamp - 10
            x_high = self.current_timestamp
        else:
            x_low = 0
            x_high = 10
        self.ax.set_xlim(x_low, x_high)
        return self.line,

    def plot(self, fusion: dict, fusion_timestamps: list) -> None:
        self.ax.clear()
        self.current_timestamp = 0.0
        self.fusion_timestamps = fusion_timestamps
        play_range = int(
            (self.fusion_timestamps[-1] - self.fusion_timestamps[0]) * 10)
        self.frames_range = [
            round(0.1 * x + self.fusion_timestamps[0], 1) for x in range(play_range)]
        self.x = self.fusion_timestamps
        self.y = [v['pitch'] for v in fusion.values()]
        self.ax.set_xlabel('Timestamp')
        self.ax.set_ylabel('Pitch')
        self.ax.set_title('Calculated Head Pitch Over Time')
        self.ax.set_xlim(-2, len(self.frames_range) + 2)
        ymax = max(abs(max(self.y)), abs(min(self.y)))
        ymod = ((ymax // 15) + 1) * 15
        self.ax.set_ylim(-ymod - 2, ymod + 2)
        print(ymod)
        self.ax.set_yticks(np.arange(-ymod, ymod + 1, 15))
        self.ani = FuncAnimation(
            self.fig, self._draw_next_frame, frames=self.frames_range, init_func=self._init_scatter, interval=100)
        self.draw()
        self._pause = True
        self.ani.pause()

    def start(self) -> None:
        self._pause = False
        self.ani.resume()

    def pause(self) -> None:
        self._pause = True
        self.ani.pause()

    def stop(self) -> None:
        self.ax.clear()

    def seek(self) -> None:
        pass
        # xs = [i for i in range(0, len(y_list), 100)]
        # x = np.array(xs)
        # y = np.array(y_list)

        # self.ax.set_xlabel("X")
        # self.ax.set_ylabel("Y")
        # self.ax.set_title("live pitch Scatter Plot")
        # for i in range(0, len(y_list), 1000):
        #     self.ax.set_ylim(-15, 25)
        #     self.ax.scatter(i, y[i])
        #     self.ax.plot(i, y[i])
        #     self.ax.pause(0.01)
