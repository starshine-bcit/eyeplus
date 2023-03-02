import unittest
from modules.regressor import Regression2dGazeModel, Regression3dGazeModel, RegressionMagnetometerModel
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import random

class TestRegressionMagnetometerModel(unittest.TestCase):
    def test_get_predicted_mag(self):
        mag_data = {
            '1.2': {'magnetometer': [1.0, 2.0, 3.0]},
            '2.3': {'magnetometer': [2.0, 3.0, 4.0]},
            '3.4': {'magnetometer': [3.0, 4.0, 5.0]},
            '4.5': {'magnetometer': [4.0, 5.0, 6.0]},
            '5.6': {'magnetometer': [5.0, 6.0, 7.0]},
        }
        predict_timestamps = [1.5, 2.0, 3.5, 4.0, 5.5]

        # create RegressionMagnetometerModel object
        reg_model = RegressionMagnetometerModel(mag_data, predict_timestamps)
        predicted_mag = reg_model.get_predicted_mag()

        # check that predicted mag is a dictionary with correct keys
        self.assertIsInstance(predicted_mag, dict)
        self.assertCountEqual(predicted_mag.keys(), predict_timestamps)

        # check that each value in predicted mag is a list of 3 floats
        for mag_values in predicted_mag.values():
            self.assertIsInstance(mag_values, list)
            self.assertEqual(len(mag_values), 3)
            for value in mag_values:
                self.assertIsInstance(value, float)

class TestRegression3dGazeModel(unittest.TestCase):
    
    def setUp(self):
        self.run_data = {}
        for i in range(50):
            x = round(random.uniform(0, 2.5), 2)
            y = [random.uniform(-1, 1) for j in range(3)]
            self.run_data[str(x)] = {'gaze3d': y}
        
    def test_get_predicted_3d(self):
        model = Regression3dGazeModel(self.run_data)
        predicted_output = model.get_predicted_3d()
        self.assertIsInstance(predicted_output, dict)
        self.assertGreater(len(predicted_output), 0)
        for k, v in predicted_output.items():
            self.assertIsInstance(k, float)
            self.assertIsInstance(v, list)
            self.assertEqual(len(v), 3)

class TestRegression2dGazeModel(unittest.TestCase):
    def test_get_predicted_2d(self):
        model = Regression2dGazeModel({'1': {'gaze2d': (1, 2)}, '2': {'gaze2d': (2, 3)}, '3': {'gaze2d': (3, 4)}})
        result = model.get_predicted_2d()
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), model._length)
        self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main()
