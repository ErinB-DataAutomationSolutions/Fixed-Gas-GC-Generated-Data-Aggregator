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
config_file = "config_files\\test_config.json"
test_data_dir = "Data_Directories"
test_report_ext = "xls"
data_sheets = {
    "Sheet1": {
      "filter_cols": [],
      "filter_rows": [],
      "index_cols":
      [
        "AcqMeth",
        "AcqOp",
        "InjDateTime",
        "SampleName"
      ],
      "col_data_map": {},
      "row_data_map": {
        "AcqMeth" : "method_nm",
        "AcqOp": "operator_nm",
        "InjDateTime": "dt_tm",
        "SampleName": "sample_nm"
      }
    },
    "Compound": {
      "filter_cols": [
        "Name",
        "Amount"
      ],
      "filter_rows": [],
      "index_cols": "Name",
      "col_data_map": {},
      "row_data_map": {
        "CARBON DIOXIDE": "CO2_micro_L",
        "HYDROGEN": "H2_micro_L",
        "OXYGEN": "O2_micro_L",
        "NITROGEN": "N2_micro_L",
        "METHANE": "CH4_micro_L",
        "CARBON MONOXIDE": "CO_micro_L"
      }
    }
  }

config = Config(config_file)            # Set config object


class TestConfig(ut.TestCase):

    def test_run(self):
        self.assertEqual("xls", test_report_ext)


if __name__ == '__main__':
    print("Running test")
    ut.main()
