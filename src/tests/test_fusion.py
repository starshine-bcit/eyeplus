import unittest
from modules.fusion import Fusion
import numpy as np

class TestFusion(unittest.TestCase):
    def setUp(self):
        self.imu_data = {}
        self.mag_data = {}
        self.predicted_data = {}
        self.timestamps = []
        self.sample_data = []

        # Create sample data
        for i in range(100):
            timestamp = i / 100
            self.timestamps.append(timestamp)
            sample_imu_data = np.random.uniform(-1, 1, 6)
            self.imu_data[str(timestamp)] = {'gyroscope': sample_imu_data[:3], 'accelerometer': sample_imu_data[3:]}
            sample_mag_data = np.random.uniform(-100, 100, 3)
            self.mag_data[str(timestamp)] = {'magnetometer': sample_mag_data}

            self.sample_data.append({'timestamp': timestamp, 'imu': sample_imu_data, 'mag': sample_mag_data})

        # Instantiate the Fusion object
        self.fusion = Fusion( self.mag_data, self.predicted_data, self.timestamps, roll_offset=90)

    def test_run(self):
        # Run the Fusion algorithm on the test data
        self.fusion.run()
        # Check that the heading, pitch, and roll angles are all set to 0
        self.assertAlmostEqual(self.fusion.heading, 0)
        self.assertAlmostEqual(self.fusion.pitch, 0)
        self.assertAlmostEqual(self.fusion.roll, 0)

if __name__ == '__main__':
    unittest.main()
