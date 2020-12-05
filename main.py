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
#   ) Import the following from config.json:
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
#   )       Remove all but data specified in sheet dictionary
#   )       Append data to master table
#
########################################################################################################################

# IMPORT LIBRARIES #
import os
import json as js
import pandas as pd
# import numpy as np

# Get current dir
curr_dir = os.curdir

# Import CONFIG Details
with open("support/config.json") as config_file:
    config = js.load(config_file)

# Assign data directory and report name values
data_dir = config['data_dir']                       # Construct data directory string
report_file_name = config["report_name"]            # Set report file name
report_ext = config["report_ext"]                   # Set report file extension
data_sheets = config["data_sheets"]                 # Get DataSheet dictionary
data_columns = config["data_columns"]               # Set data columns for export

# STEP : Construct Directory Paths
data_dir_path = f"{curr_dir}\\{data_dir}"           # Construct data dir path
report_file = f"{report_file_name}.{report_ext}"    # Construct report file

# STEP : Get all immediate child directories
child_dirs = os.listdir(f"{data_dir_path}")

# STEP : Create Empty Master DataFrame
export_data_df = pd.DataFrame(columns=data_columns)

print(export_data_df)

# STEP : Access each directory
for child_dir in child_dirs:
    file_name = f"{data_dir_path}\\{child_dir}\\{report_file}"  # Create file name

# STEP : Create Excel File Object
    file = pd.ExcelFile(file_name)

# STEP : Extract data per sheet
    for key in data_sheets:
        sheet_cols = data_sheets[key]               # Get list of req columns in sheet
        sheet_data_df = file.parse(sheet_name=key)   # Store sheet data in DataFrame

# STEP :
