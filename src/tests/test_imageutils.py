import unittest
from PIL import Image
from utils.imageutils import create_video_overlay


class TestImageUtils(unittest.TestCase):

    def setUp(self):
        self.dims = {'w': 800, 'h': 600, 'ml': 0, 'mr': 0, 'mt': 0, 'mb': 0}
        self.predict_x = 0.5
        self.predict_y = 0.5
        self.y_intercept = 0.5
        self.x_intercept = 0.5
        self.slope = 0.5
        self.roll = 45
        self.pitch = 45

    def test_create_video_overlay(self):
        img, ml, mt = create_video_overlay(self.dims, self.predict_x, self.predict_y, self.y_intercept, self.x_intercept, self.slope, self.roll, self.pitch)

        # assert the returned object is an instance of PIL.Image
        self.assertIsInstance(img, Image.Image)

        # assert the returned values for ml and mt are integers
        self.assertIsInstance(ml, int)
        self.assertIsInstance(mt, int)

        # assert the image dimensions match the expected values
        self.assertEqual(img.width, 800)
        self.assertEqual(img.height, 600)

        # assert the expected color values are present in the image
        self.assertEqual(img.getpixel((10, 10)), (0, 0, 0, 0))
        self.assertEqual(img.getpixel((400, 300)), (0,0,0,0))


if __name__ == '__main__':
    unittest.main()
