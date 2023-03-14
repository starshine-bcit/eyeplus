
from random import shuffle

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colours
import matplotlib.patches as mpatches
import numpy as np

plt.style.use('ggplot')
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 'small'


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

    def _init_line(self):
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
        # self.ax.set_xlabel('Timestamp')
        # self.ax.set_ylabel('Pitch')
        self.ax.set_title('Calculated Head Pitch Over Time')
        self.ax.set_xlim(-2, len(self.frames_range) + 2)
        ymax = max(abs(max(self.y)), abs(min(self.y)))
        ymod = ((ymax // 15) + 1) * 15
        self.ax.set_ylim(-ymod - 2, ymod + 2)
        self.ax.set_yticks(np.arange(-ymod, ymod + 1, 15))
        self.ani = FuncAnimation(
            self.fig, self._draw_next_frame, frames=self.frames_range, init_func=self._init_line, interval=100)
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


class HeatMap(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)

    def plot(self, gaze2d: dict) -> None:
        self.ax.clear()
        arr_min = 0
        arr_max = 1
        n_rows = 100
        n_cols = 100
        v_min = 0
        v_max = 0
        self.x = np.linspace(arr_min, arr_max, n_rows)
        self.y = np.linspace(arr_min, arr_max, n_cols)
        self.z = np.array([0] * (n_rows * n_cols)).reshape(n_rows, n_cols)
        for v in gaze2d.values():
            x_round = round(v[0] * n_rows)
            y_round = round(v[1] * n_cols)
            if x_round <= n_cols and y_round <= n_rows:
                self.z[y_round][x_round] += 1
                if self.z[y_round][x_round] > v_max:
                    v_max = self.z[y_round][x_round]
        self.heat_map = self.ax.pcolormesh(
            self.x, self.y, self.z, shading='gouraud', cmap='plasma', vmin=v_min, vmax=v_max)
        self.ax.set_title('Heatmap of 2d Gaze')
        self.fig.canvas.draw()


class TotalUpDownStacked(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)

    def plot(self, up_down: dict, fusion: dict, pitch_multi: float) -> None:
        self.ax.clear()
        self.up_down = up_down
        pitch_data = [v['pitch'] * pitch_multi for v in fusion.values()]
        self.mean_pitch = np.mean(pitch_data)
        x = ['Up/Down', 'Avg. Pitch']
        y1 = [up_down['percent_down']]
        y1_2 = [up_down['percent_up']]
        y2 = [(self.mean_pitch + 15) / 30]
        self.ax.set_ybound(0.0, 1.0)
        self.ax.set_title(
            'Total Up/Down vs. Mean Pitch')
        self.ax.bar(x[0], y1, color='firebrick')
        self.ax.bar(x[0], y1_2, bottom=y1, color='mediumseagreen')
        self.ax.bar(x[1], y2, color='darkviolet')
        self.ax.set_yticklabels([])
        self.ax.text(1, y2[0] + 0.05, round(self.mean_pitch, 2), ha='center')
        self.fig.canvas.draw()


class GazeLive(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)

    @property
    def is_paused(self) -> bool:
        return self._pause

    def _draw_single_line(self, x: list, y: list, colour: str) -> None:
        self.ax.plot(x, y, color=colour)

    def _init_line(self) -> None:
        current_up = self.processed[self.processed_timestamps[0]
                                    ]['currently_up']
        inner_x = []
        inner_y = []
        for k, v in self.processed.items():
            if v['currently_up'] == current_up:
                inner_x.append(k)
                inner_y.append(self.gaze2d[k][1])
            elif v['currently_up'] != current_up:
                inner_x.append(k)
                inner_y.append(self.gaze2d[k][1])
                colour = 'mediumseagreen' if current_up else 'firebrick'
                self._draw_single_line(inner_x, inner_y, colour)
                current_up = v['currently_up']
                inner_x.clear()
                inner_y.clear()
                inner_x.append(k)
                inner_y.append(self.gaze2d[k][1])
        if inner_x and inner_y:
            colour = 'mediumseagreen' if not current_up else 'firebrick'
            self._draw_single_line(inner_x, inner_y, colour)

    def _draw_next_frame(self, frame: float):
        if self.current_timestamp > 10:
            x_low = self.current_timestamp - 10
            x_high = self.current_timestamp
        else:
            x_low = 0
            x_high = 10
        self.ax.set_xlim(x_low, x_high)

    def plot(self, gaze2d: dict, processed: dict) -> None:
        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.current_timestamp = 0.0
        self.processed = processed
        self.gaze2d = gaze2d
        self.processed_timestamps = list(processed.keys())
        self.current_timestamp = 0.0
        play_range = int(
            (self.processed_timestamps[-1] - self.processed_timestamps[0]) * 10)
        self.frames_range = [
            round(0.1 * x + self.processed_timestamps[0], 1) for x in range(play_range)]
        self.x = self.processed_timestamps
        self.y = [gaze2d[x][1] for x in self.processed_timestamps]
        self.ax.set_xlim(-2, len(self.frames_range) + 2)
        self.ax.set_ylim(0, 1)
        self.ax.set_title('Gaze 2d Y Over Time')
        # self.ax.set_xlabel('Timestamp')
        # self.ax.set_ylabel('Gaze 2d Y')
        self.ax.set_yticks(
            [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0])
        self.ax.invert_yaxis()
        self.ani = FuncAnimation(self.fig, self._draw_next_frame,
                                 frames=self.frames_range, init_func=self._init_line, interval=100)
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
        pass


class OverallGaze2DY(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)
        self.colours = [x for x in colours.XKCD_COLORS]
        shuffle(self.colours)
        self.colour_index = 0
        nothing_patch = mpatches.Patch(color='purple', label=' ')
        self.legend = self.fig.legend(handles=[nothing_patch])

    def plot(self, gaze_data: dict) -> int:
        self.ax.clear()
        max_len = 0
        for runid, v in gaze_data.items():
            curr_colours = self.colours[self.colour_index]
            self.colour_index += 1
            if self.colour_index >= len(self.colours):
                self.colour_index = 0
            curr_len = v['ts'][-1]
            if curr_len > max_len:
                max_len = curr_len
            self.ax.plot(v['ts'], v['y'],
                         color=curr_colours, linewidth=0.7, label=f'Run {runid[0]}')
        self.ax.set_yticks(
            [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0])
        self.ax.set_xticks(np.arange(0, max_len, 2))
        self.ax.set_title('2D Eye Y Over Time For Selected Runs')
        self.ax.set_ylim(0.0, 1.0)
        self.ax.set_xlim(0.0, 30.0)
        self.ax.invert_yaxis()
        self.legend.remove()
        self.legend = self.fig.legend()
        self.fig.canvas.draw()
        return int(max_len)

    def update_scroll(self, val: int) -> None:
        self.ax.set_xlim(float(val - 30), float(val))
        self.fig.canvas.draw_idle()


class OverallUpAndDown(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)

    def plot(self, up_down: dict) -> None:
        self.ax.clear()
        num_runs = up_down['run_count']
        x = ['Up', 'Down']
        y = [up_down['total_up'], up_down['total_down']]
        y_ticks = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        self.ax.set_ybound(0.0, 1.0)
        self.ax.set_title(f'Total Up/Down Proportion over {num_runs} runs')
        bars = self.ax.bar(x, y, color=['mediumseagreen', 'firebrick'])
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels([str(x) for x in y_ticks])
        self.ax.bar_label(bars, [str(round(z, 2)) for z in y])
        self.fig.canvas.draw()


class PitchHistogram(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        super().__init__(width, height, dpi)

    def plot(self, total_observations: int, pitch_binned: dict) -> None:
        self.ax.clear()
        x = []
        y = []
        for k, v in pitch_binned.items():
            x.append(k)
            y.append(v)
        bars = self.ax.bar(x, y, [4.5] * len(pitch_binned),
                           align='edge', color='darkviolet', edgecolor='deeppink')
        y_max = round(max(y), 1) + 0.1
        y_marks = np.linspace(0, y_max, int(y_max * 20 + 1))
        self.ax.set_yticks(y_marks)
        self.ax.set_yticklabels([str(round(x, 2)) for x in y_marks])
        x_marks = np.arange(-40, 40, 5)
        self.ax.set_xticks(x_marks)
        self.ax.set_xticklabels([str(x) for x in x_marks])
        self.ax.set_title(
            f'Proportion of Pitch over {total_observations} observations')
        self.ax.set_xlim(-30, 30)
        self.fig.canvas.draw()
