# IMPORTS
import unittest as ut
from support.data_upload import DataSheet
import pandas as pd


class TestDataSheet(ut.TestCase):

    def setUp(self) -> None:
        sheet_one_dict = {
            "headers": 0,
            "transpose": 1,
            "filter_cols": [],
            "filter_rows": [
                "AcqMeth",
                "AcqOp",
                "InjDateTime",
                "SampleName"
            ],
            "index_col": "",
            "col_data_map": {},
            "row_data_map": {
                "AcqMeth": "method_nm",
                "AcqOp": "operator_nm",
                "InjDateTime": "dt_tm",
                "SampleName": "sample_nm"
            }
        }

        self.data_sheet_1 = DataSheet("Sheet1", "test_REPORT01.xlsx", sheet_one_dict)

    def tearDown(self) -> None:
        pass

    def test_import_data(self):
        sheet_one_import_data = {['ExtraIndex1', 'AcqMeth', 'AcqOp', 'InjDateTime', 'SampleName', 'ExtraIndex2'],
                                 ['EXTRA_VALUE_1', 'TEST_ACQ_MTH_NM', 'TEST_ACQ_OP_NM', '20-Nov-20', '16:32:32',
                                  'TEST_SAMPLE_NM', 'EXTRA_VALUE_2']}
        sheet_one_import_df = pd.DataFrame(data=sheet_one_import_data)
        print(sheet_one_import_df)

        compound_import_df = []
        pass

    def test_filter_data(self):
        sheet_one_filtered_df = []
        compound_filtered_df = []
        pass


if __name__ == "__main__":
    # ut.main()
    pass
