from sklearn.ensemble import RandomForestRegressor
import numpy as np


class Regression2dGazeModel():
    def __init__(self, run_data: dict) -> None:
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
        self._length = int(round(x[-1] + 0.1, 1) * 10)

    def get_predicted_2d(self) -> dict:
        vals = [round(x / 10, 1) for x in range(self._length)]
        predicted_pos = self._trees.predict(
            np.array(vals).reshape(-1, 1))
        predicted_dict = {}
        for i in range(len(vals)):
            predicted_dict[vals[i]] = [
                predicted_pos[i][0], predicted_pos[i][1]]
        return predicted_dict


class RegressionMagnetometerModel():
    def __init__(self, mag_data: dict, predict_timestamps: list[float]) -> None:
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
        predicted_mag = self._trees.predict(self._p)
        # explained_variance_score on sparse input: 0.9968204315587093
        predicted_dict = {}
        for i in range(len(self._p)):
            predicted_dict[self._p[i][0]] = [
                predicted_mag[i][0], predicted_mag[i][1], predicted_mag[i][2]]
        return predicted_dict


if __name__ == '__main__':
    pass
