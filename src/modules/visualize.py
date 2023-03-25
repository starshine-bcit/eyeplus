
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
        """BasicCanvas is used to subclass individual plots off of.

        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        px = 1/dpi
        self.fig = Figure(figsize=(width*px, height*px), dpi=dpi)
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot()


class TotalUpDown(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        """Visual bar plot for time spent looking down versus up for a single run.

        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        super().__init__(width, height, dpi)

    def plot(self, data: dict):
        """Plots time spent looking up versus down and draws it on canvas.

        Args:
            data (dict): Contains cumulative up/down data for a single run.
        """
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
        """Much like TotalUpDown, but is meant to be called on each screen update in playback review.

        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        super().__init__(width, height, dpi)
        self.ax.margins(0.5)

    def plot(self, data: dict, timestamp: float):
        """Plots the up/down cumulative data at a given timestamp.

        Args:
            data (dict): Contains all processed up/down data.
            timestamp (float): Timestamp we wish to plot for.
        """
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
        """Displays a live plot of the rolling calculated pitch over time.

        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
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
        """Adjusts the xlim of the plot based on currently playing timestamp.

        Args:
            frame (float): The frame number provided by funcAnimation..
        """
        if self.current_timestamp + 10 > self.fusion_timestamps[0]:
            x_low = self.current_timestamp - 10
            x_high = self.current_timestamp
        else:
            x_low = self.current_timestamp
            x_high = self.current_timestamp + 10
        self.ax.set_xlim(x_low, x_high)

    def plot(self, fusion: dict, fusion_timestamps: list) -> None:
        """Extracts the pitch data from the fusion data, and plots a
            line covering the entire length of the run.
        Args:
            fusion (dict): Fusion data, grabbed from the database.
            fusion_timestamps (list): A list of the keys from the fusion data.
        """
        self.ax.clear()
        self.current_timestamp = fusion_timestamps[0]
        self.fusion_timestamps = fusion_timestamps
        play_range = int(
            (self.fusion_timestamps[-1] - self.fusion_timestamps[0]) * 10)
        self.frames_range = [
            round(0.1 * x + self.fusion_timestamps[0], 1) for x in range(play_range)]
        self.x = self.fusion_timestamps
        self.y = [v['pitch'] for v in fusion.values()]
        self.ax.set_title('Calculated Head Pitch Over Time')
        self.ax.set_xlim(-2, len(self.frames_range) + 2)
        ymax = max(abs(max(self.y)), abs(min(self.y)))
        ymod = ((ymax // 15) + 1) * 15
        self.ax.set_ylim(-ymod - 2, ymod + 2)
        self.ax.set_yticks(np.arange(-ymod, ymod + 1, 15))
        self.ani = FuncAnimation(
            self.fig, self._draw_next_frame, frames=self.frames_range, init_func=self._init_line, interval=100)
        self.draw()
        self.ax.set_xlim(self.current_timestamp, self.current_timestamp + 10)
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
        """Displays a heatmap indicating how much a user was looking at
            a given 2d gaze point.
        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        super().__init__(width, height, dpi)

    def plot(self, gaze2d: dict) -> None:
        """Creates a 2d heatmap based on the 2d gaze data from Tobii.

        Args:
            gaze2d (dict): Processed 2d gaze data from the database.
        """
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
        self.ax.invert_yaxis()
        self.ax.set_title('Heatmap of 2d Gaze')
        self.fig.canvas.draw()


class TotalUpDownStacked(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        """Displays a comparison bar chart between calculated looking
            up/down versus mean pitch for a given run.

        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        super().__init__(width, height, dpi)

    def plot(self, up_down: dict, fusion: dict, pitch_multi: float) -> None:
        """Plots a chart with two bars, one of them stack up/down data,
            the other the mean pitch (accounting for pitch_multi).
        Args:
            up_down (dict): Contains the final cumulative up/down data.
            fusion (dict): Sensor fusion data from the database.
            pitch_multi (float): The pitch multi to apply to each pitch value.
        """
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
        """Gaze live shows the 2d eye Y values, changing colour
            depending on whether the user is calculated to be looking
            up or down at the given time.
        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        super().__init__(width, height, dpi)

    @property
    def is_paused(self) -> bool:
        return self._pause

    def _draw_single_line(self, x: list, y: list, colour: str) -> None:
        self.ax.plot(x, y, color=colour)

    def _init_line(self) -> None:
        """Creates and draws any number of lines that continous
            on the plot, green if a user is looking "up", red
            if a user is looking "down".
        """
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
        """Adjusts the xlim of the plot based on currently playing timestamp.

        Args:
            frame (float): The frame number provided by funcAnimation.
        """
        if self.current_timestamp + 10 > self.processed_timestamps[0]:
            x_low = self.current_timestamp - 10
            x_high = self.current_timestamp
        else:
            x_low = self.current_timestamp
            x_high = self.current_timestamp + 10
        self.ax.set_xlim(x_low, x_high)

    def plot(self, gaze2d: dict, processed: dict) -> None:
        """Plots the 2d gaze y over time, with the colour changing
            based on whether a user is observed to be looking up
            or down.

        Args:
            gaze2d (dict): Processed 2d gaze values from database.
            processed (dict): Processed horizon data from database.
        """
        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.processed = processed
        self.gaze2d = gaze2d
        self.processed_timestamps = list(processed.keys())
        self.current_timestamp = self.processed_timestamps[0]
        play_range = int(
            (self.processed_timestamps[-1] - self.processed_timestamps[0]) * 10)
        self.frames_range = [
            round(0.1 * x + self.processed_timestamps[0], 1) for x in range(play_range)]
        self.x = self.processed_timestamps
        self.y = [gaze2d[x][1] for x in self.processed_timestamps]
        self.ax.set_xlim(-2, len(self.frames_range) + 2)
        self.ax.set_ylim(0, 1)
        self.ax.set_title('Gaze 2d Y Over Time')
        self.ax.set_yticks(
            [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0])
        self.ax.invert_yaxis()
        self.ani = FuncAnimation(self.fig, self._draw_next_frame,
                                 frames=self.frames_range, init_func=self._init_line, interval=100)
        self.draw()
        self.ax.set_xlim(self.current_timestamp, self.current_timestamp + 10)
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
        """Displays line plot of gaze 2d y points over time, for one
            or more runs at once.

        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        super().__init__(width, height, dpi)
        self.colours = [x for x in colours.XKCD_COLORS]
        shuffle(self.colours)
        self.colour_index = 0
        nothing_patch = mpatches.Patch(color='purple', label=' ')
        self.legend = self.fig.legend(handles=[nothing_patch])

    def plot(self, gaze_data: dict) -> int:
        """Plots a line indicating 2d gaze y over time for each run present in input.
            Colours are randomly chosen from XKCD colours.

        Args:
            gaze_data (dict): Contains processed gaze data for one or more runs.

        Returns:
            int: The max timestamp plotted by this method.
        """
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
        """Called by the gui to update the xlim on Qt scrollbar update.

        Args:
            val (int): The value indicating the furthest right bound of the plot to display.
        """
        self.ax.set_xlim(float(val - 30), float(val))
        self.fig.canvas.draw_idle()


class OverallUpAndDown(BasicCanvas):
    def __init__(self, width: int, height: int, dpi: float):
        """Plots mean Up/Down statistics over multiple runs.

        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        super().__init__(width, height, dpi)

    def plot(self, up_down: dict) -> None:
        """A simple bar chart comparing time spent looking up or down
            for one or more runs.
        Args:
            up_down (dict): Contains mean up/down values, as well as number
                of runs being displayed.
        """
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
        """Displays a histogram of already binned calculated pitch values.

        Args:
            width (int): Width of the plot to make in pixels.
            height (int): Height of the plot to make in pixels.
            dpi (float): DPI of the plot to make.
        """
        super().__init__(width, height, dpi)
        self.ax1 = self.fig.add_subplot(2, 2, 1)
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 2, 3)
        self.ax4 = self.fig.add_subplot(2, 2, 4)

    def plot(self, total_observations: int, pitch_binned: dict) -> None:
        """Plots the already binned pitch values, along with regular
            x and y ticks, including total observations included in title.

        Args:
            total_observations (int): Total number of observations that were binned.
            pitch_binned (dict): Contains relative frequency of each bin.
        """
        self.ax.clear()
        x = []
        y = []
        for k, v in pitch_binned.items():
            x.append(k)
            y.append(v)
        bars = self.ax.bar(x, y, [4.5] * len(pitch_binned),
                           align='edge', edgecolor='black')
        y_max = round(max(y), 1) + 0.1
        y_marks = np.linspace(0, y_max, int(y_max * 20 + 1))
        self.ax.set_yticks(y_marks)
        self.ax.set_yticklabels([str(round(x, 2)) for x in y_marks])
        x_marks = [-36, -31.5, -27, -22.5, -18, -13.5, -
                   9, -4.5, 0, 4.5, 9, 13.5, 18, 22.5, 27, 31.5, 36]
        self.ax.set_xticks(x_marks)
        self.ax.set_xticklabels([str(x) for x in x_marks])
        self.ax.set_title(
            f'Proportion of Pitch over {total_observations} observations')
        self.ax.set_xlim(-30, 30)
        self.fig.canvas.draw()
