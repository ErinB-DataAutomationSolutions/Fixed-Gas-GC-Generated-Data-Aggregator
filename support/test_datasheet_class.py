# IMPORTS
from support.data_upload import DataSheet
import pandas as pd

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

sheet_1 = DataSheet('Sheet1', 'support\\test_REPORT01.xlsx', sheet1_metadata)

# --- TEST COMPOUND --- #

compound_metadata = {
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
