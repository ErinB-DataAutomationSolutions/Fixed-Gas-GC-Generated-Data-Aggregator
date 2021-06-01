########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.pu
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 05/31/2021
#
########################################################################################################################

# IMPORTS
import pandas as pd
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
    dt_string = now.strftime("%m%d%Y.%H%M%S")

    return f"{user_name}.{dt_string}.{export_ext}"


def create_export_object(export_data_cols):
    # Build file name
    export_file_name = build_export_file_name()
    return ExportData(export_file_name, export_data_cols)

    # print(f"File {export_file_name} has been exported!")


if __name__ == "__main__":
    # () Get Config File Name
    try:
        config = create_config_object()
        print(config.input_data_dir)
    except FileNotFoundError as e:
        print("The following error occurred:")
        print(e)
        input("Press any key to exit program... ")
        sys.exit(e)

    # config = Config("config_files\\config_default.json")

    # () Get all file paths
    input_data_file_paths = get_input_data_file_paths(config.input_data_dir, config.full_file_name)
    print(input_data_file_paths)

    # () Get All Sheet Metadata
    sheets_metadata = config.data_sheets()
    # print(sheets_metadata)

    # () Create Sheet Objects
    sheet_1 = create_sheet_object(sheets_metadata, "Sheet1")
    compound = create_sheet_object(sheets_metadata, "Compound")

    # () Create Export Table Object
    # Get the mapped export column values for Sheet1
    sheet_1_export_cols = sheet_1.data_map_vals
    # print(sheet_1_export_cols)

    # Get the mapped export column values for
    compound_export_cols = compound.data_map_vals
    # print(compound_export_cols)

    # Combine export column values for both sheets
    export_cols = sheet_1_export_cols + compound_export_cols
    # print(export_cols)

    create_export_object()

    # () Get data in each sheet of each file:
    for input_data_file_path in input_data_file_paths:
        # Get Sheet1 Data
        sheet_1_df = sheet_1.import_data(input_data_file_path)
        sheet_1_df = sheet_1.clean_data(sheet_1_df)
        # print(sheet_1_df)

        # Get Compound Data
        compound_df = compound.import_data(input_data_file_path)
        compound_df = compound.clean_data(compound_df)
        # print(compound_df)

        # Create Export Data
        export_data = create_export_object(export_cols)
