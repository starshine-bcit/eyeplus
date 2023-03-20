from utils.statutils import next_greatest_element


class HorizonGaze():
    def __init__(self, gaze2d: dict, gaze3d: dict, fused: dict, horizon_offset: float):
        """A HorizonGaze object is used to calculate whether a user is looking "up" or "down" at a given time.

        Args:
            gaze2d (dict): gaze2d data for a given run.
            gaze3d (dict): gaze3d data for a given run.
            fused (dict): fusion data for a given run.
            horizon_offset (float): Horizon offset to apply to calculations.
        """
        self._gaze2d = gaze2d
        self._gaze3d = gaze3d
        self._fused = fused
        self._readings_looking_up = 0
        self._readings_looking_down = 0
        self._horizon_offset = horizon_offset
        self._total_readings = 0
        self._currently_up = False
        self._playback_store = {}
        self._count = 0
        self._gaze2d_ts = list(self._gaze2d.keys())
        self._length = len(self._gaze2d_ts) - 2
        self._fused_ts = list(self._fused.keys())
        self._gaze3d_ts = list(self._gaze3d.keys())

    def calculates_all(self) -> dict:
        """Performs a calculation for each timestamp in gaze2d.

        Returns:
            dict: Final results for all timestamps, including cumulative statistics.
        """
        while self._count < self._length:
            current_ts = self._gaze2d_ts[self._total_readings]
            self._playback_store[current_ts] = {
                'total': self._total_readings,
                'percent_up': self._readings_looking_up / self._total_readings if self._total_readings > 1 else 0,
                'percent_down': self._readings_looking_down / self._total_readings if self._total_readings > 1 else 0,
                'down_count': self._readings_looking_down,
                'up_count': self._readings_looking_up,
                'currently_up': self._currently_up
            }
            self._calculate_single(self._gaze2d_ts[self._count])
            self._count += 1
            self._calculate_single(self._gaze2d_ts[self._count])
            self._count += 1
        return self._playback_store

    def _calculate_single(self, timestamp: float) -> None:
        """Uses helper methods to do a single calculation to determine if gaze point is "up" or "down"

        Args:
            timestamp (float): Timestamp to be processed.
        """
        if timestamp >= 1:
            closest_fuse = next_greatest_element(timestamp, self._fused_ts)
            slope = self._fused[closest_fuse]['slope']
            y_intercept = self._fused[closest_fuse]['y_intercept']
            closest_gaze3d = next_greatest_element(timestamp, self._gaze3d_ts)
            if closest_gaze3d:
                if self._gaze3d_ts[closest_gaze3d] - timestamp < 0.05:
                    distance = self._gaze3d[closest_gaze3d]
                else:
                    distance = None
            else:
                distance = None
            gaze_x = self._gaze2d[timestamp][0]
            gaze_y = self._gaze2d[timestamp][1]
            result = self._calculate_up(
                slope, y_intercept, gaze_x, gaze_y, distance)
            if result:
                self._readings_looking_up += 1
                self._currently_up = True
            else:
                self._readings_looking_down += 1
                self._currently_up = False
            self._total_readings += 1

    def _calculate_up(self, slope: float, y_intercept: float, gaze_x: float, gaze_y: float, gaze_distance: float | None) -> bool:
        """Calculates whether the gaze2d point is above or below the provided horizon line.

        Args:
            slope (float): Slope of the calculated horizon line.
            y_intercept (float): Y Intercept of the calculated horizon line.
            gaze_x (float): The gaze2d X point.
            gaze_y (float): The gaze2d Y point.
            gaze_distance (float | None): Gaze3d distance, or None if a close value was not found previously.

        Returns:
            bool: True if user's gaze2d point is above the horizon line and the gaze_distance is greater than 200.
        """
        y_intercept += self._horizon_offset
        if gaze_distance is not None and gaze_distance < 200:
            return False
        elif gaze_y < slope * gaze_x + y_intercept:
            return True
        else:
            return False
