# IMPORTS
from support.data_upload import DataSheet
import unittest as ut
# import pandas as pd

sheet1_metadata = {
        "headers_bool": 0,
        "transpose_bool": 1,
        "data_map":
        {
            "AcqMeth": "method_nm",
            "AcqOp": "operator_nm",
            "InjDateTime": "dt_tm",
            "SampleName": "sample_nm"
        }}

compound_metadata = {
    "headers_bool": 1,
    "headers_nm": ["Name", "Amount"],
    "transpose_bool": 1,
    "data_map":
    {
        "CARBON DIOXIDE": "CO2_micro_L",
        "HYDROGEN": "H2_micro_L",
        "OXYGEN": "O2_micro_L",
        "NITROGEN": "N2_micro_L",
        "METHANE": "CH4_micro_L",
        "CARBON MONOXIDE": "CO_micro_L"
    }}


compound_missing_cols_metadata = {
    "headers_bool": 1,
    "transpose_bool": 1,
    "data_map":
    {
        "CARBON DIOXIDE": "CO2_micro_L",
        "HYDROGEN": "H2_micro_L",
        "OXYGEN": "O2_micro_L",
        "NITROGEN": "N2_micro_L",
        "METHANE": "CH4_micro_L",
        "CARBON MONOXIDE": "CO_micro_L"
    }}


class TestDataSheet(ut.TestCase):

    def setUp(self) -> None:
        # 'support\\test_REPORT01.xlsx',
        self.sheet_1 = DataSheet('Sheet1', sheet1_metadata)

        # 'support\\test_REPORT01.xlsx',
        self.compound = DataSheet('Compound', compound_metadata)
        self.compound_missing_cols_error = DataSheet('Compound', compound_missing_cols_metadata)

    def tearDown(self) -> None:
        pass

    def test_header(self):
        # Expected Values
        sheet1_headers = None
        compound_headers = 0

        # Tests
        self.assertEqual(self.sheet_1.header, sheet1_headers)
        self.assertEqual(self.compound.header, compound_headers)

    def test_headers_bool(self):
        # Expected Values
        sheet1_headers_bool = False
        compound_headers_bool = True

        # Tests
        self.assertEqual(self.sheet_1.header_bool, sheet1_headers_bool)
        self.assertEqual(self.compound.header_bool, compound_headers_bool)

    def test_transpose_bool(self):
        # Expected Values
        sheet1_transpose_bool = True
        compound_transpose_bool = True

        # Tests
        self.assertEqual(self.sheet_1.transpose_bool, sheet1_transpose_bool)
        self.assertEqual(self.compound.transpose_bool, compound_transpose_bool)

    def test_use_cols(self):
        # Expected Values
        sheet1_use_cols = None
        compound_use_cols = ["Name", "Amount"]

        # Tests
        self.assertEqual(self.sheet_1.use_cols, sheet1_use_cols)
        self.assertEqual(self.compound.use_cols, compound_use_cols)
        # self.assertRaises(KeyError, self.compound_missing_cols_error.use_cols)

    def test_data_map(self):
        # Expected Values
        sheet1_data_map = {
            "AcqMeth": "method_nm",
            "AcqOp": "operator_nm",
            "InjDateTime": "dt_tm",
            "SampleName": "sample_nm"
        }

        compound_data_map = {
            "CARBON DIOXIDE": "CO2_micro_L",
            "HYDROGEN": "H2_micro_L",
            "OXYGEN": "O2_micro_L",
            "NITROGEN": "N2_micro_L",
            "METHANE": "CH4_micro_L",
            "CARBON MONOXIDE": "CO_micro_L"
        }

        # Tests
        self.assertEqual(self.sheet_1.data_map, sheet1_data_map)
        self.assertEqual(self.compound.data_map, compound_data_map)

    def test_data_map_keys(self):
        # Expected Values
        sheet1_data_map_keys = ["AcqMeth", "AcqOp", "InjDateTime", "SampleName"]
        compound_data_map_keys = ["CARBON DIOXIDE", "HYDROGEN", "OXYGEN", "NITROGEN", "METHANE", "CARBON MONOXIDE"]

        # Tests
        self.assertEqual(self.sheet_1.data_map_keys, sheet1_data_map_keys)
        self.assertEqual(self.compound.data_map_keys, compound_data_map_keys)

    def test_data_map_vals(self):
        # Expected Values
        sheet1_data_map_vals = ["method_nm", "operator_nm", "dt_tm", "sample_nm"]
        compound_data_map_vals = ["CO2_micro_L", "H2_micro_L", "O2_micro_L", "N2_micro_L", "CH4_micro_L", "CO_micro_L"]

        # Tests
        self.assertEqual(self.sheet_1.data_map_values, sheet1_data_map_vals)
        self.assertEqual(self.compound.data_map_values, compound_data_map_vals)


if __name__ == '__main__':
    ut.main()
