########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               old_main.py
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 06/02/2021
#
########################################################################################################################

# IMPORTS
from support.old_data_upload import Config, create_sheet_obj_list, create_export_obj, create_export_df, get_exp_col_list
from support.old_data_agg_ui import initiate_gui
import sys
import glob


# METHODS
def create_config_obj():
    config_file_name = input("Enter Config File Name: ")
    config_file_path = f"config_files\\{config_file_name}.json"
    return Config(config_file_path)


def get_input_data_file_paths(input_data_dir, input_data_file_name) -> list:
    return glob.glob(f'./{input_data_dir}/**/{input_data_file_name}', recursive=True)


def get_username():
    return input("Enter Username: ")


def main_v1():
    # (1) Get Config File Name
    try:
        config = create_config_obj()
        # print(config.input_data_dir)
    except FileNotFoundError as e:
        print("The following error occurred:")
        print(e)
        input("Press any key to exit program... ")
        sys.exit(e)

    # (2) Get all file paths
    input_data_file_paths = get_input_data_file_paths(config.input_data_dir, config.full_file_name)
    # print(input_data_file_paths)

    # (3) Get All Sheet Metadata
    sheets_metadata = config.data_sheets
    # print(sheets_metadata)

    # (4) Dynamically create a list of sheet objects based on config file
    sheet_list = create_sheet_obj_list(config.data_sheet_names, sheets_metadata)

    # (5) Get export columns
    export_cols = get_exp_col_list(sheet_list)
    # print(export_cols)

    # (6) Create export object and DataFrame
    export = create_export_obj(export_cols, "ErinB", "Export_Files")
    export_df = export.initiate_export_df()

    # (7) Get data in each sheet of each file:
    print("Importing data...")
    export_df = create_export_df(input_data_file_paths, export_df, sheet_list)
    # print(export_df)

    # (8) Export data to an xlsx file
    export.export(export_df)


def main_v2():
    initiate_gui()


if __name__ == "__main__":
    # Data Aggregator V1
    # main_v1()

    # Data Aggregator V2
    main_v2()
