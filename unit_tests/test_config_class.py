########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               test_config_class.py
#   FILE PURPOSE:       Test the Config class from support.data_upload
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 9/5/21
#
#   DESCRIPTION:
#       This file is used to test the Config class in library file data_upload.py
#
########################################################################################################################

# IMPORTS
import unittest as ut
from support.data_upload import Config

# Set Test Variables
config_file = "../config_files/config_default.json"


class TestConfig(ut.TestCase):

    def setUp(self) -> None:
        self.config = Config()
        self.config.config = config_file
        self.config.config_settings()

    def tearDown(self) -> None:
        del self.config

    def test_report_ext(self):
        # Expected Value
        report_ext = "xls"

        # Test
        self.assertEqual(self.config.report_ext, report_ext)

    def test_is_dict(self):
        # self.assertTrue(type(self.config.input_data_dir), dict)
        pass

    def test_data_sheet_keys(self):
        expected_value = ["Sheet1", "Compound"]

        self.assertEqual(self.config.datasheets_names, expected_value)

    def test_data_sheets(self):
        # Expected Value
        data_sheets = {
            "Sheet1": {
                "headers_bool": 0,
                "transpose_bool": 1,
                "data_map": {
                    "AcqMeth": "method_nm",
                    "AcqOp": "operator_nm",
                    "InjDateTime": "dt_tm",
                    "SampleName": "sample_nm"
                }
            },
            "Compound": {
                "headers_bool": 1,
                "headers_nm": [
                    "Name",
                    "Amount"
                ],
                "transpose_bool": 1,
                "data_map": {
                    "CARBON DIOXIDE": "CO2_micro_L",
                    "HYDROGEN": "H2_micro_L",
                    "OXYGEN": "O2_micro_L",
                    "NITROGEN": "N2_micro_L",
                    "METHANE": "CH4_micro_L",
                    "CARBON MONOXIDE": "CO_micro_L"
                }
            }
        }

        # Test
        self.assertDictEqual(self.config.datasheets_metadata, data_sheets)


if __name__ == '__main__':
    ut.main()
