########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.pu
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 12/04/2020
#
#   PROGRAM STEPS
#   ) Set Current path
#   ) Import the following from config_default.json:
#       - data_dir:     Directory housing generated child-directories
#       - report_name:  File name of generated report
#       - report_ext:   File extension of generated report
#       - data_sheets:  Dictionary of sheets to use, each containing a list of required info
#       - data_columns: List of required columns in extracted data
#   ) Construct dir paths
#   ) Get list of all generated child directories
#   ) Create empty master DataFrame
#   ) For each report in directory
#   )   Create pandas ExcelFile object
#   )   For each required sheet
#   )       Create temp_data_df DataFrame from sheet
#   )       Extract specific data slice from DataFrame
#   )       Append data to master table
#
########################################################################################################################

import pandas as pd
from pandas.testing import assert_frame_equal

sheet_one_import_data = {
    'Col1': ['ExtraIndex1', 'AcqMeth', 'AcqOp', 'InjDateTime', 'SampleName', 'ExtraIndex2'],
    'Col2': ['EXTRA_VALUE_1', 'TEST_ACQ_MTH_NM', 'TEST_ACQ_OP_NM', '20-Nov-20, 16:32:32', 'TEST_SAMPLE_NM',
             'EXTRA_VALUE_2']
}

# Create DataFrame of imported data from Sheet1
sheet_one_import_df = pd.DataFrame(data=sheet_one_import_data)
# print(sheet_one_import_df)

sheet_one = pd.read_excel('support\\test_REPORT01.xlsx', header=None, sheet_name='Sheet1')
# sheet_one.set_index('0')
print('Imported data from Sheet1')
print(sheet_one)

# Transpose the data
sheet_one = sheet_one.T

print("\nLet's look at the transposed data, as imported:")
print(sheet_one)

print("\nNow, let's set our columns to the first row")
sheet_one.columns = sheet_one.iloc[0]
sheet_one = sheet_one.drop(index=0)
print(sheet_one)

print("\nNow let's look at each column name to be sure we've got he dataframe we want:")
for column in sheet_one.columns:
    print(column)

# sheet_one.columns = ['Col1', 'Col2']

# print(sheet_one)
# print('\n')

# assert_frame_equal(sheet_one, sheet_one_import_df, check_dtype=False, check_column_type=False)

# sheet_one = sheet_one.set_index('Col1')
# print(sheet_one)
# print('\n')

# sheet_one = sheet_one.T
# print(sheet_one)
# for column in sheet_one.columns:
#     print(column)
# print('\n')

