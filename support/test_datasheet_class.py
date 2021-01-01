# IMPORTS
import unittest as ut
from support.data_upload import DataSheet
import pandas as pd

# Test Variables - Config Import Values
data_file_nm = "test_REPORT01.xlsx"
sheet_names = ["Sheet1", "Compound"]
sheet_one_dict = {
    "headers": 0,
    "transpose": 1,
    "filter_cols": [],
    "filter_rows":  [
        "AcqMeth",
        "AcqOp",
        "InjDateTime",
        "SampleName"
    ],
    "index_col": "",
    "col_data_map": {},
    "row_data_map": {
        "AcqMeth":  "method_nm",
        "AcqOp": "operator_nm",
        "InjDateTime": "dt_tm",
        "SampleName": "sample_nm"
    }
}

# Test Variables - Expected Data - Sheet1
acq_mth = "TEST_ACQ_MTH_NM"
acq_op = "TEST_ACQ_OP_NM"
InjDateTime = "20-Nov-20, 16:32:32"
sample_name = "TEST_SAMPLE_NM"


class TestDataSheet(ut.TestCase):

    def setUp(self) -> None:
        self.data_sheet_1 = DataSheet(sheet_names[1], data_file_nm, sheet_one_dict)

    def tearDown(self) -> None:
        pass

    def test_import_data(self):
        pass

    def test_filter_data(self):
        pass


if __name__ == "__main__":
    # ut.main()
    pass
