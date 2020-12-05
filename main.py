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
#   ) Get list of all generated child directories
#   ) Create empty master DataFrame
#   ) For each report in directory
#   )   Create pandas ExcelFile object
#   )   Create run_info DataFrame from sheet "Sheet1"
#   )   Extract the following info:
#       - Sample_Name
#       - Date_and_time
#       - Operator_Name
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
data_dir = f"{curr_dir}\\{config['data_dir']}"
report_file_name = config["report_name"]
report_ext = config["report_ext"]
report_file = f"{report_file_name}.{report_ext}"

# STEP : Get all immediate child directories
child_dirs = os.listdir(f"{data_dir}")

# STEP : Create Empty Master DataFrame
pass

# STEP : Access each directory
for child_dir in child_dirs:
    # Create file name
    file_name = f"{data_dir}\\{child_dir}\\{report_file}"

# STEP : Create Excel File Object
    file = pd.ExcelFile(file_name)

# STEP : Get run info data
    run_info_df = file.parse(sheet_name="Sheet1", skiprows=1)
    # A) Extract run info from run_info_df
    pass

    # B) Transpose data
    pass

    # C) Add data to master table
    pass

# STEP : Get compound data
    compound_df = file.parse(sheet_name="Compound")
    pass
