########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.py
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 06/01/2021
#
########################################################################################################################

# IMPORTS
import pandas as pd
from support.data_upload import Config, DataSheet, ExportData, re_index_df, add_data_row
import sys
import glob
from datetime import datetime as dt


# METHODS
def create_config_obj():
    config_file_name = input("Enter Config File Name: ")
    config_file_path = f"config_files\\{config_file_name}.json"
    return Config(config_file_path)


def get_input_data_file_paths(input_data_dir, input_data_file_name) -> list:
    return glob.glob(f'./{input_data_dir}/*/{input_data_file_name}')


def create_sheet_obj(config_sheets_metadata, sheet_name):
    sheet_metadata = config_sheets_metadata[sheet_name]
    return DataSheet(sheet_name, sheet_metadata)


def build_export_file_nm() -> str:
    user_name = input("User Name: ")
    export_dir = input("Export directory: ")
    export_ext = "xlsx"

    now = dt.now()
    dt_string = now.strftime("%m%d%Y.%H%M%S")

    return f"{export_dir}\\{user_name}.{dt_string}.{export_ext}"


def create_export_obj(export_data_cols):
    # Build file name
    export_file_name = build_export_file_nm()
    return ExportData(export_file_name, export_data_cols)

    # print(f"File {export_file_name} has been exported!")


def create_sheet_obj_list(sheet_names: list, sheets_metadata_dict: dict):
    # Create empty object list
    sheet_obj_list = []

    # Populate sheet_obj_list with constructed sheet objects
    for sheet_name in sheet_names:
        sheet_obj = create_sheet_obj(sheets_metadata_dict, sheet_name)
        sheet_obj_list.append(sheet_obj)

    return sheet_obj_list


def get_exp_col_list(sheet_obj_list):
    # Create empty export columns list
    exp_col_list = []

    # Get the data values from each sheet
    for sheet_obj in sheet_obj_list:
        data_map_cols = sheet_obj.data_map_vals

        # Append each value to the export column list
        for data_map_col in data_map_cols:
            exp_col_list.append(data_map_col)

    return exp_col_list


def create_export_df(data_file_paths, exp_df, sheet_obj_list):

    for data_file_path in data_file_paths:

        # Create an empty DataFrame to store input data
        temp_df = pd.DataFrame({'temp_col': []})

        # Import data from each sheet
        for sheet_obj in sheet_obj_list:
            sheet_df = sheet_obj.import_data(data_file_path)

            # Clean sheet data
            sheet_df = sheet_obj.clean_data(sheet_df)

            # Add imported data to new data row
            temp_df = pd.concat([temp_df, sheet_df], axis=1)

            # Clean up
            del sheet_df

        # Add new data row
        temp_df = temp_df.drop(columns='temp_col')
        exp_df = add_data_row(exp_df, temp_df)

        # Clean up
        del temp_df

    exp_df = re_index_df(exp_df)

    return exp_df


if __name__ == "__main__":
    # () Get Config File Name
    try:
        config = create_config_obj()
        # print(config.input_data_dir)
    except FileNotFoundError as e:
        print("The following error occurred:")
        print(e)
        input("Press any key to exit program... ")
        sys.exit(e)

    # config = Config("config_files\\config_default.json")

    # () Get all file paths
    input_data_file_paths = get_input_data_file_paths(config.input_data_dir, config.full_file_name)
    # print(input_data_file_paths)

    # () Get All Sheet Metadata
    sheets_metadata = config.data_sheets()
    # print(sheets_metadata)

    # () Dynamically create a list of sheet objects based on config file
    sheet_list = create_sheet_obj_list(config.data_sheet_names, sheets_metadata)

    # () Create Sheet Objects
    sheet_1 = create_sheet_obj(sheets_metadata, "Sheet1")
    compound = create_sheet_obj(sheets_metadata, "Compound")

    # () Create Export Table Object
    # Get the mapped export column values for Sheet1
    sheet_1_export_cols = sheet_1.data_map_vals
    # print(sheet_1_export_cols)

    # Get the mapped export column values for
    compound_export_cols = compound.data_map_vals
    # print(compound_export_cols)

    # Combine export column values for both sheets
    # export_cols = sheet_1_export_cols + compound_export_cols
    export_cols = get_exp_col_list(sheet_list)
    # print(export_cols)

    # Create export object and DataFrame
    export = create_export_obj(export_cols)
    export_df = export.create_export_df()

    # () Get data in each sheet of each file:
    # for input_data_file_path in input_data_file_paths:
        # Get Sheet1 Data
        # sheet_1_df = sheet_1.import_data(input_data_file_path)
        # sheet_1_df = sheet_1.clean_data(sheet_1_df)
        # print(sheet_1_df)

        # Get Compound Data
        # compound_df = compound.import_data(input_data_file_path)
        # compound_df = compound.clean_data(compound_df)
        # print(compound_df)

        # Combine imported data into a single data row
        # new_data_df = pd.concat([sheet_1_df, compound_df], axis=1)

        # Add new row to export data
        # export_df = add_data_row(export_df, new_data_df)
        # print(export_df)

    # Re-Index the export df
    # export_df = re_index_df(export_df)
    # print(export_df)

    export_df = create_export_df(input_data_file_paths, export_df, sheet_list)
    print(export_df)

    # Export data to an xlsx file
    export.export(export_df)
