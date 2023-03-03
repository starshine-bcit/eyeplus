import unittest
from modules.analyze import HorizonGaze

class TestHorizonGaze(unittest.TestCase):
    def test_calculate_up(self):
        # create HorizonGaze object with dummy values
        horizon_gaze = HorizonGaze(
            {
                0.0: [1, 1],
                1.0: [2, 2],
                2.0: [3, 3],
                3.0: [4, 4],
                4.0: [5, 5]
            },
            {
                0.0: 100,
                1.0: 200,
                2.0: 300,
                3.0: 400,
                4.0: 500
            },
            {
                0.0: {'slope': 1, 'y_intercept': 0},
                1.0: {'slope': 1, 'y_intercept': 0},
                2.0: {'slope': 1, 'y_intercept': 0},
                3.0: {'slope': 1, 'y_intercept': 0},
                4.0: {'slope': 1, 'y_intercept': 0}
            }
        )
        result = horizon_gaze._calculate_up(1, 0, 1, 2, 1000)
        self.assertEqual(result, False)

    def test_calculates_all(self):
        # create HorizonGaze object with dummy values
        # create HorizonGaze object with dummy values
        gaze2d = {}
        gaze3d = {}
        fused = {}
        horizon_gaze = HorizonGaze(gaze2d, gaze3d, fused)
    
        horizon_gaze._gaze2d_ts = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [1.2, 2.2], [1.4, 2.4]]
    
        playback_store = horizon_gaze.calculates_all()
    
        #self.assertIn(1.4, playback_store.keys())
        
    def test_get_close_3d(self):
        # create HorizonGaze object with dummy values
        horizon_gaze = HorizonGaze({}, {}, {})
        horizon_gaze._gaze3d_ts = [1.0, 2.0, 3.0, 4.0, 5.0]
        self.assertEqual(horizon_gaze._get_close_3d(1.1), None)
        self.assertEqual(horizon_gaze._get_close_3d(3.0), None)
        self.assertEqual(horizon_gaze._get_close_3d(5.05), None)
        self.assertEqual(horizon_gaze._get_close_3d(0.9), 1.0)
        
        

    def test_get_close_fuse(self):
        # create HorizonGaze object with dummy values
        horizon_gaze = HorizonGaze({}, {}, {})
        horizon_gaze._fused_ts = [0.0, 1.0, 2.0, 3.0, 4.0]
        
        # Test case 1: timestamp exactly matches a time in the list
        timestamp = 2.0
        result = horizon_gaze._get_close_fuse(timestamp)
        self.assertEqual(result, timestamp)

        # Test case 2: timestamp is between two times in the list
        timestamp = 2.5
        result = horizon_gaze._get_close_fuse(timestamp)
        self.assertEqual(result, 3.0)

        # Test case 3: timestamp is after the last time in the list
        timestamp = 5.0
        result = horizon_gaze._get_close_fuse(timestamp)
        self.assertEqual(result, 4.0)
        

if __name__ == '__main__':
    unittest.main()
