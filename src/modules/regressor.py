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
        self._trees = RandomForestRegressor()
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


if __name__ == '__main__':
    pass
    # gaze_file = Path('C:\\Courses\\3900\\sample_data\\gazedata.ndjson')
    # time = []
    # x = []
    # with gaze_file.open('r', encoding='utf8') as fo:
    #     file_data = fo.readlines()
    #     count = 0
    #     for line in file_data:
    #         parsed = json.loads(line)
    #         if 'data' in parsed:
    #             if 'gaze2d' in parsed['data']:
    #                 time.append(parsed['timestamp'])
    #                 x.append([parsed['data']['gaze2d'][0],
    #                           parsed['data']['gaze2d'][1]])

    # npx = np.array(x)
    # npx = npx.reshape(len(x), 2)
    # npz = np.array(time)
    # npz = npz.reshape(-1, 1)

    # trees = RandomForestRegressor()
    # trees.fit(npz, x)
    # predicted = trees.predict(
    #     np.array([x / 10 for x in range(11370)]).reshape(-1, 1))
    # for i, v in enumerate(predicted):
    #     print(f'Time: {round(i * 0.1, 1)} Predicted: {v}')

    # for i in range(5):
    #     print(npx[i])
    #     print(npy[i])
    #     print(npz[i])
    # print(len(npx))
    # print(len(npy))
    # print(len(npz))

    # forest = RandomForestClassifier()
    # forest.fit(npx, npz)
    # print(forest.predict([0.05]))
