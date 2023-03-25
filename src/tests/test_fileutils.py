import unittest
from pathlib import Path
import utils.fileutils


class TestFileUtils(unittest.TestCase):
    def test_validate_import_folder(self):
        # Test case where all needed items are in the input folder
        input_folder = Path('C:/BCIT/Term 4/ACIT 4900(ISSP)/MOT student pilot data/OneDrive_1_2023-01-05')
        expected_output = [input_folder]
        actual_output = fileutils.validate_import_folder(input_folder)
        self.assertEqual(actual_output, expected_output)
        


if __name__ == '__main__':
    unittest.main()
