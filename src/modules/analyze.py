

class HorizonGaze():
    def __init__(self, gaze2d: dict, gaze3d: dict, fused: dict, horizon_offset: float):
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
        if timestamp >= 1:
            closest_fuse = self._get_close_fuse(timestamp)
            slope = self._fused[closest_fuse]['slope']
            y_intercept = self._fused[closest_fuse]['y_intercept']
            closest_gaze3d = self._get_close_3d(timestamp)
            if closest_gaze3d:
                distance = self._gaze3d[closest_gaze3d]
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

    def _get_close_3d(self, timestamp: float) -> float | None:
        for time in self._gaze3d_ts:
            if time >= timestamp:
                if timestamp - time <= 0.05:
                    return time
                else:
                    return None
            else:
                return None

    def _get_close_fuse(self, timestamp: float) -> float:
        for time in self._fused_ts:
            if time >= timestamp:
                return time
        return self._fused_ts[-1]

    def _calculate_up(self, slope: float, y_intercept: float, gaze_x: float, gaze_y: float, gaze_distance: float | None) -> bool:
        # make horizon fuzzy somehow
        if gaze_distance is not None and gaze_distance < 200:
            return False
        elif gaze_y < slope * gaze_x + y_intercept:
            return True
        else:
            return False
