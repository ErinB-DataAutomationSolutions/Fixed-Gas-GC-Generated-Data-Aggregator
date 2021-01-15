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
