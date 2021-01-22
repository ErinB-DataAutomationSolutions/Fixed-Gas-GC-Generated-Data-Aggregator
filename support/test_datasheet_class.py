# IMPORTS
from support.data_upload import DataSheet
import unittest as ut
# import pandas as pd

# --- TEST SHEET 1 --- #

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
        self.sheet_1 = DataSheet('Sheet1', 'support\\test_REPORT01.xlsx', sheet1_metadata)
        self.compound = DataSheet('Compound', 'support\\test_REPORT01.xlsx', compound_metadata)
        self.compound_missing_cols_error = DataSheet('Compound', 'support\\test_REPORT01.xlsx',
                                                     compound_missing_cols_metadata)

    def tearDown(self) -> None:
        pass

    def test_header(self):
        # Expected Test Values
        sheet1_headers = None
        compound_headers = 0

        self.assertEqual(self.sheet_1.header, sheet1_headers)
        self.assertEqual(self.compound.header, compound_headers)

    def test_transpose_bool(self):
        # Correct Test Values
        sheet1_transpose_bool = True
        compound_transpose_bool = True

        self.assertEqual(self.sheet_1.transpose_bool, sheet1_transpose_bool)
        self.assertEqual(self.compound.transpose_bool, compound_transpose_bool)

    def test_use_cols(self):
        # Correct Test Values
        sheet1_use_cols = None
        compound_use_cols = ["Name", "Amount"]

        self.assertEqual(self.sheet_1.use_cols, sheet1_use_cols)
        self.assertEqual(self.compound.use_cols, compound_use_cols)
        self.assertRaises(KeyError, self.compound_missing_cols_error.use_cols)

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
        pass

    def test_data_map_vals(self):
        pass

    def test_import_data(self):
        pass

    def test_clean_data(self):
        pass


if __name__ == '__main__':
    ut.main()
