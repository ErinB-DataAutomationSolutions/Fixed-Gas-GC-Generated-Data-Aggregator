########################################################################################################################
#
#   PROGRAM:            Rob's Data Collector
#   FILE:               pandas_import_tutorial.py
#   PURPOSE:            To test steps required for data extraction, cleaning, and export
#   AUTHOR:             Erin Bryson
#   DATE LAST MODIFIED: 01.15.2021
#
########################################################################################################################
import pandas as pd


print("\n--- SHEET1 DATA ---")

# Set data map dictionary for Sheet1.
# This will be extracted from the config file
data_map = {
    "AcqMeth": "method_nm",
    "AcqOp": "operator_nm",
    "InjDateTime": "dt_tm",
    "SampleName": "sample_nm"
}

# Set empty lists for data map keys and values
data_map_keys = []
data_map_vals = []

# Populate the above lists with keys and values
for key in data_map:
    data_map_keys.append(key)
    data_map_vals.append(data_map[key])

print("\nWe need to get the following data from Sheet1:")
print(data_map_keys)

print("\nWhich will then need to be mapped to the following data:")
print(data_map_vals)

sheet_one = pd.read_excel('support\\test_REPORT01.xlsx', header=None, sheet_name='Sheet1')
# sheet_one.set_index('0')
print('\nImported data from Sheet1:')
print(sheet_one)

# Transpose the data
sheet_one = sheet_one.T

print("\nLet's look at the transposed data, as imported:")
print(sheet_one)

print("\nNow, let's set our columns to the first row:")
sheet_one.columns = sheet_one.iloc[0]   # Set column names equal to first row values
sheet_one = sheet_one.drop(index=0)     # Remove first row
print(sheet_one)

print("\nNow let's look at each column name to be sure we've got he dataframe we want:")
for column in sheet_one.columns:
    print(column)

print("\nLet's get rid of extra columns:")
sheet_one = sheet_one.filter(items=data_map_keys)   # Filter out all but desired columns
print(sheet_one)

print("\nFinally, let's rename our columns to match the final export column names:")
sheet_one.columns = data_map_vals   # Rename columns
print(sheet_one)

print('\n--- COMPOUND DATA ---')
data_map = {
    "CARBON DIOXIDE": "CO2_micro_L",
    "HYDROGEN": "H2_micro_L",
    "OXYGEN": "O2_micro_L",
    "NITROGEN": "N2_micro_L",
    "METHANE": "CH4_micro_L",
    "CARBON MONOXIDE": "CO_micro_L"
}
