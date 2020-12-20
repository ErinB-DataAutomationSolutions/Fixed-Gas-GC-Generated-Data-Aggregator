########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.pu
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 12/20/2020
#
#   DESCRIPTION:
#       This file is used to test the Config class in library file data_upload.py
#
########################################################################################################################

# IMPORTS
import unittest as ut
from support.data_upload import Config

# Set Test Variables
config_file = "../\\config_files\\test_config.json"
data_dir = "Data_Directories"
report_ext = "xls"
data_sheets = {
    "Sheet1":
    [
      "AcqMeth",
      "AcqOp",
      "InjDateTime",
      "SampleName"
      ],
    "Compound":
    [
      "Amount"
    ]
  }


class TestConfig(ut.TestCase):

    def setUp(self) -> None:
        self.config = Config(config_file)

    def tearDown(self) -> None:
        pass

    def test_data_dir(self):
        self.assertEqual(self.config.data_dir, data_dir)

    def test_report_ext(self):
        self.assertEqual(self.config.report_ext, report_ext)

    def test_data_sheets(self):
        print(self.config.data_sheets())
        self.assertDictEqual(self.config.data_sheets, data_sheets)


if __name__ == '__main__':
    ut.main()
