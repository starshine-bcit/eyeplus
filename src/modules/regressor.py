from sklearn.ensemble import RandomForestRegressor
import numpy as np


class Regression2dGazeModel():
    def __init__(self, run_data: dict) -> None:
        """Uses a regression model to predict the gaze2d data at evenly spaced intervals of 0.05 seconds.

        Args:
            run_data (dict): The raw input gaze2d values from Tobii ndjson file.
        """
        y = []
        x = []
        for key, val in run_data.items():
            if val['gaze2d'][0] is not None and val['gaze2d'][1] is not None:
                y.append(val['gaze2d'])
                x.append(float(key))
        self._x = np.array(x)
        self._x = self._x.reshape(-1, 1)
        self._y = np.array(y)
        # baseline explained_variance_score: 0.8009777683831507
        # tuned explained_variance_score: 0.8479487271201485
        self._trees = RandomForestRegressor(
            n_estimators=200, max_depth=35, n_jobs=-1, max_features=8, random_state=20, max_samples=None, bootstrap=True)
        self._trees.fit(self._x, self._y)
        self._length = int(round(x[-1] + 0.05, 2) * 20)

    def get_predicted_2d(self) -> dict:
        """Predicts and returns the values for each timestamp at 0.05 second intervals.

        Returns:
            dict: Processed 2dgaze data for later use.
        """
        vals = [round(x / 20, 2) for x in range(self._length)]
        predicted_pos = self._trees.predict(
            np.array(vals).reshape(-1, 1))
        predicted_dict = {}
        for i in range(len(vals)):
            predicted_dict[vals[i]] = [
                predicted_pos[i][0], predicted_pos[i][1]]
        return predicted_dict


class RegressionMagnetometerModel():
    def __init__(self, mag_data: dict, predict_timestamps: list[float]) -> None:
        """Uses a regression model in order to predict magnetometer data such that it lines up gyro and accelerometer timestamps.

        Args:
            mag_data (dict): Raw magnetometer data from Tobii ndjson file.
            predict_timestamps (list[float]): List of timestamps to predict for.
        """
        y = []
        x = []
        self._p = np.array(predict_timestamps)
        self._p = self._p.reshape(-1, 1)
        for key, val in mag_data.items():
            x.append(float(key))
            y.append(val['magnetometer'])
        self._x = np.array(x)
        self._x = self._x.reshape(-1, 1)
        self._y = np.array(y)
        self._trees = RandomForestRegressor(n_jobs=-1)
        self._trees.fit(self._x, self._y)

    def get_predicted_mag(self) -> dict:
        """Predicts magnetometer data for each timestamp provided.

        Returns:
            dict: Predicted magnetometer data for each timestamp.
        """
        predicted_mag = self._trees.predict(self._p)
        # explained_variance_score on sparse input: 0.9968204315587093
        predicted_dict = {}
        for i in range(len(self._p)):
            predicted_dict[self._p[i][0]] = [
                predicted_mag[i][0], predicted_mag[i][1], predicted_mag[i][2]]
        return predicted_dict


if __name__ == '__main__':
    pass
