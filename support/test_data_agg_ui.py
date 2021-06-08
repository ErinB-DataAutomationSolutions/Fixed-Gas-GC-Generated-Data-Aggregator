########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               test_data_agg_ui.py
#   FILE PURPOSE:       Test classes and functions from data_agg_ui.py
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 6/7/2021
#
########################################################################################################################

# IMPORTS
import unittest as ut
from support.data_agg_ui import DAggUserInterface as DaUI


class TestDAaggUserInterface(ut.TestCase):

    def setUp(self) -> None:
        self.test_ui = DaUI()
        pass

    def tearDown(self) -> None:
        pass

    def test_get_username(self):
        expected_val = "ErinB"          # Expected Value
        self.test_ui.get_username()     # Execute function
        self.assertEqual(self.test_ui.username, expected_val)

        pass

    def test_get_config_file_path(self):
        pass

    def test_get_input_directory_path(self):
        pass

    def test_get_output_directory_path(self):
        pass


if __name__ == "__main__":
    ut.main()
