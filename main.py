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
#   ) For each report in directory
#   )   For each required sheet
#   )       Create temp_data_df DataFrame from sheet
#   )       Extract specific data slice from DataFrame
#   )       Append data to master table
#
########################################################################################################################

# IMPORTS
from support.data_upload import Config
from support.data_upload import DataSheet
from support.data_upload import ExportData
import sys
import glob
from datetime import datetime as dt


# METHODS
def create_config_object():
    config_file_name = input("Enter Config File Name: ")
    config_file_path = f"config_files\\{config_file_name}.json"
    return Config(config_file_path)


def get_input_data_file_paths(input_data_dir, input_data_file_name) -> list:
    return glob.glob(f'./{input_data_dir}/*/{input_data_file_name}')


def create_sheet_object(config_sheets_metadata, sheet_name):
    sheet_metadata = config_sheets_metadata[sheet_name]
    return DataSheet(sheet_name, sheet_metadata)


def build_export_file_name() -> str:
    user_name = input("User Name: ")
    export_dir = input("Export directory: ")
    export_ext = "xlsx"

    now = dt.now()
    dt_string = now.strftime("%d.%m.%Y.%H.%M.%S")

    return f"{user_name}.{dt_string}.{export_ext}"


def create_export_object():
    # Build file name
    export_file_name = build_export_file_name()


if __name__ == "__main__":
    # () Get Config File Name
    config = create_config_object()
    # config = Config("config_files\\config_default.json")

    # () Get all file paths
    input_data_file_paths = get_input_data_file_paths(config.full_file_name)
    # print(input_data_file_dirs)

    # () Get All Sheet Metadata
    sheets_metadata = config.data_sheets()
    # print(sheets_metadata)

    # () Create Sheet Objects
    sheet_1 = create_sheet_object(sheets_metadata, "Sheet1")
    compound = create_sheet_object(sheets_metadata, "Compound")

    # () Create Export Table Object

    # () Get data in each sheet of each file:
    for input_data_file_path in input_data_file_paths:
        pass
