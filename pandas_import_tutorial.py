########################################################################################################################
#
#   PROGRAM:            Rob's Data Collector
#   FILE:               pandas_import_tutorial.py
#   PURPOSE:            To test steps required for data extraction, cleaning, and export
#   AUTHOR:             Erin Bryson
#   DATE LAST MODIFIED: 05.18.2021
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

# Set logic checks for Sheet1.
# These will be extracted form the config file
headers_bool = False
transpose_bool = True

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

if headers_bool:
    header = 0
else:
    header = None

sheet_one = pd.read_excel('support\\test_REPORT01.xlsx', header=header, sheet_name='Sheet1', index_col=None)
sheet_one = sheet_one.dropna()
print('\nImported data from Sheet1:')
print(sheet_one)

# Transpose the data
if transpose_bool:
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
sheet_one = sheet_one.filter(items=data_map_keys)   # Filter out all undesired columns
print(sheet_one)

print("\nFinally, let's rename our columns to match the final export column names:")
sheet_one.columns = data_map_vals   # Rename columns
sheet_one = sheet_one.reset_index(drop=True)
print(sheet_one)

print('\n--- COMPOUND DATA ---')

# Set data map dictionary for Compound.
# This will be extracted from the config file
data_map = {
    "CARBON DIOXIDE": "CO2_micro_L",
    "HYDROGEN": "H2_micro_L",
    "OXYGEN": "O2_micro_L",
    "NITROGEN": "N2_micro_L",
    "METHANE": "CH4_micro_L",
    "CARBON MONOXIDE": "CO_micro_L"
}

headers_bool = True
use_cols = ["Name", "Amount"]
transpose_bool = True

# Set empty lists for data map keys and values
data_map_keys = []
data_map_vals = []

for key in data_map:
    data_map_keys.append(key)
    data_map_vals.append(data_map[key])

print("\nWe need to get the following data from Compound:")
print(data_map_keys)

print("\nWhich will then need to be mapped to the following data:")
print(data_map_vals)

if headers_bool:
    header = 0
else:
    header = None

compound = pd.read_excel('support\\test_REPORT01.xlsx', header=header, sheet_name='Compound', usecols=use_cols)
print(compound)
compound = compound.dropna()
# compound = compound.dropna().set_index(use_cols[0])
print('\nImported data from Compound:')
print(compound)

# Transpose the data
if transpose_bool:
    compound = compound.T.reset_index(drop=True)

print("\nLet's look at the transposed data:")
print(compound)

print("\nFinally, let's rename the columns:")
compound.columns = compound.iloc[0]
compound = compound.filter(items=data_map_keys)   # Filter out all undesired columns
compound.columns = data_map_vals
print(compound)
compound = compound.drop(index=0).reset_index(drop=True)
print(compound)

# --- COMBINE DATA INTO ONE ROW --- #

print("\n--- COMBINED DATA ---")
print("\nWe need to combine the above into a single DataFrame.")
export_data = pd.concat([sheet_one, compound], axis=1)
print(export_data)

print("\nLet's make sure we have all the columns:")
for column in export_data.columns:
    print(column)

print("\nNow to check whether we can combine rows with the same index val")
print("\nLet's make another DataFrame called 'temp_data'")
temp_data = pd.DataFrame({
    'method_nm': ['METH_NM_2'],
    'operator_nm': ['OP_NM_2'],
    'dt_tm': ['20-Nov-20, 16:32:32'],
    'sample_nm': ['SAMPOLE_NM_2'],
    'CO2_micro_L': [0.1],
    'H2_micro_L': [0.2],
    'O2_micro_L': [0.3],
    'N2_micro_L': [0.4],
    'CH4_micro_L': [0.5],
    'CO_micro_L': [0.6]
})

print(temp_data)

print("When we use the concat function on axis=0 (default) we get:")
export_data = pd.concat([export_data, temp_data])
print(export_data)

print("\nWe can do this for each file, and then reset the index like so:")
export_data = export_data.reset_index(drop=True)
print(export_data)

print("\nAnd voila! Now that we know what to do, it's time to clean this up!")
