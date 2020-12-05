########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.pu
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 12/04/2020
#
#   PROGRAM STEPS
#   ) Import the following from config.json:
#       - data_dir:     Directory housing generated child-directories
#       - report_name:  File name of generated report
#       - report_ext:   File extension of generated report
#       -
#   ) Get list of all generated child directories
#   ) Create empty master DataFrame
#   ) For each report in directory
#   )   Create pandas ExcelFile object
#   )   Create run_info DataFrame from sheet "Sheet1"
#   )   Extract the following info:
#       - Sample_Name
#       - Date_and_time
#       - Operator_Name3
#       - Method_Name
#   )   Create
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

data_dir_path = f"{curr_dir}\\{data_dir}"           # Construct data dir path
report_file = f"{report_file_name}.{report_ext}"    # Construct report file

# STEP : Get all immediate child directories
child_dirs = os.listdir(f"{data_dir_path}")

# STEP : Create Empty Master DataFrame
pass

# STEP : Access each directory
for child_dir in child_dirs:
    # Create file name
    file_name = f"{data_dir_path}\\{child_dir}\\{report_file}"

# STEP : Create Excel File Object
    file = pd.ExcelFile(file_name)

# STEP : Get run info data
    run_info_df = file.parse(sheet_name="Sheet1", skiprows=1)
    # A) Extract run info from run_info_df
    # run_info_df.set_index(")

    # print(run_info_df)
    pass

    # B) Transpose data
    pass

    # C) Add data to master table
    pass

# STEP : Get compound data
    compound_df = file.parse(sheet_name="Compound")
    # print(compound_df)
    pass
