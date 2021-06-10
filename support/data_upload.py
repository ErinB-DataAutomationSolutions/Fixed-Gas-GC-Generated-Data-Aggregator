########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               data_upload.py
#   FILE PURPOSE:       Library for interacting with and extracting data from Data Sheets
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 06/02/2021
#
########################################################################################################################


# IMPORTS
import json as js
import pandas as pd
from datetime import datetime as dt


def function_timer(function):

    def function_timer_wrapper(*arg):
        # Start timer
        start_time = dt.now()

        # Execute function being timed
        function_return = function(*arg)

        # Stop timer
        stop_time = dt.now()

        # Get time difference
        time_diff = stop_time - start_time

        # Convert timedelta into string:
        report_time_diff = time_diff.seconds

        print("Execution time: " + str(report_time_diff) + " seconds")

        return function_return

    return function_timer_wrapper


# Config class
class Config:

    """
Class Config accomplishes the following:
1) Reading and parsing a user-defined Config file
2) Parsing and storing report file metadata

Metadata captured from config JSON file:
    - Data Dir:             This is the directory housing generated data sub-directories.
    - Report Name:          This is the name of the generated report file
    - Report Ext:           File extension of the generated report file
    - Data Sheets:          Dictionary containing names, metadata, and import settings for Data Sheets
        - Header Bool:      Bool value indicating whether the input data has a header
            - 1:            Header present
            - 0:            No header present
        - Header Name:      IF a header is present, THEN this is the name of the column headers when imported
        - Transpose Bool:   Bool value indicates whether the data needs to be transposed
            - 1:            Data is to be transposed
            - 0:            Data is not to be transposed
        - Data Map:         Dictionary mapping data label values to export data column names
"""

    def __init__(self, config_file_name):
        self.config_file_name = config_file_name

    @property
    def config(self):
        """Open and read config file"""
        with open(self.config_file_name) as config_file:
            return js.load(config_file)

    @property
    def input_data_dir(self):
        """Store data dir metadata"""
        return self.config["data_dir"]

    # Set Report Name
    @property
    def report_name(self):
        """Store report file name metadata"""
        return self.config["report_name"]

    # Set Report Extension
    @property
    def report_ext(self):
        """Store report file extension"""
        return self.config["report_ext"]

    # Set file name
    @property
    def full_file_name(self):
        """Construct full report file name"""
        return f"{self.report_name}.{self.report_ext}"

    # If specified data sheets are listed, get data sheets
    @property
    def data_sheets(self):
        """Store data sheets dictionary, if specified"""
        if "data_sheets" in self.config:
            return self.config["data_sheets"]

    # Store names of data sheets
    @property
    def data_sheet_names(self):
        names_list = []

        for key in self.config["data_sheets"].keys():
            names_list.append(key)

        return names_list


# Class housing data sheet info
class DataSheet:
    def __init__(self, name: str, sheet_dict: dict):
        self.name = name
        self.sheet_dict = sheet_dict

    @property
    def header_bool(self):
        if self.sheet_dict["headers_bool"] == 1:
            return True
        return False

    @property
    def header(self):
        """This property sets 'header' parameter in read_excel() either to '0' (headers located on top row of excel
        sheet) or 'None'(no headers used in excel sheet)"""
        if self.header_bool:
            return 0
        return None

    @property
    def transpose_bool(self):
        """Store whether data in sheet should be transposed."""
        if self.sheet_dict["transpose_bool"] == 1:
            return True
        return False

    # If data filter columns if specified
    @property
    def use_cols(self):
        if self.header_bool:
            try:
                return self.sheet_dict["headers_nm"]
            except KeyError:
                print("ERROR! Use Cols list missing from config file!")
                # Need to pass error to prevent data import attempt
        return None

    # Get row data map if specified
    @property
    def data_map(self):
        return self.sheet_dict["data_map"]

    @property
    def data_map_keys(self):
        data_map_keys = []

        for key in self.data_map:

            if key.isnumeric():
                final_key = int(key)
            else:
                final_key = key

            data_map_keys.append(final_key)

        return data_map_keys

    @property
    def data_map_vals(self):
        data_map_vals = []

        for key in self.data_map:
            data_map_vals.append(self.data_map[key])

        return data_map_vals

    def import_data(self, file_name) -> pd.DataFrame:
        return pd.read_excel(file_name, sheet_name=self.name, header=self.header, usecols=self.use_cols)

    def clean_data(self, data_df: pd.DataFrame) -> pd.DataFrame:

        if self.use_cols is None:
            use_col_num = 0
        else:
            use_col_num = len(self.use_cols)

        # Drop NA values
        data_df = data_df.dropna()

        # Transpose data, if needed
        if self.transpose_bool:
            data_df = data_df.T.reset_index(drop=True)

        # Filter unwanted data

        if use_col_num != 1:
            data_df.columns = data_df.iloc[0]                       # Set column names to equal to row 1
        # lif self.use_cols is None:
        #    data_df.columns = data_df.iloc[0]

        data_df = data_df.filter(items=self.data_map_keys, axis=1)      # Filter out all undesired columns

        # print(data_df)
        data_df.columns = self.data_map_vals

        if use_col_num != 1:
            data_df = data_df.drop(index=0).reset_index(drop=True)  # Drop the now-redundant first row
        # elif self.use_cols is None:
        #    data_df.columns = data_df.iloc[0]

        data_df = data_df.reset_index(drop=True)                # Reset Index

        data_df.columns = self.data_map_vals

        return data_df


class ExportData:

    def __init__(self, export_data_file_path, export_data_cols):
        self.export_data_file_path = export_data_file_path
        self.export_data_cols = export_data_cols
        # self.export_data = pd.DataFrame

    def initiate_export_df(self):
        return pd.DataFrame(columns=self.export_data_cols)

    def export(self, export_df):
        # self.export_data.to_excel(f"{self.export_file_nm}.{self.export_file_ext}")
        export_df.to_excel(self.export_data_file_path)


def re_index_df(df):
    return df.reset_index(drop=True)


def add_data_row(export_df: pd.DataFrame, temp_data: pd.DataFrame):
    return pd.concat([export_df, temp_data])


def create_sheet_obj(config_sheets_metadata, sheet_name):
    sheet_metadata = config_sheets_metadata[sheet_name]
    return DataSheet(sheet_name, sheet_metadata)


def create_sheet_obj_list(sheet_names: list, sheets_metadata_dict: dict):
    # Create empty object list
    sheet_obj_list = []

    # Populate sheet_obj_list with constructed sheet objects
    for sheet_name in sheet_names:
        sheet_obj = create_sheet_obj(sheets_metadata_dict, sheet_name)
        sheet_obj_list.append(sheet_obj)

    return sheet_obj_list


def build_export_file_nm(user_name, export_dir) -> str:
    # user_name = input("User Name: ")
    # export_dir = input("Export directory: ")
    export_ext = "xlsx"

    now = dt.now()
    dt_string = now.strftime("%m%d%Y.%H%M%S")

    return f"{export_dir}\\{user_name}.{dt_string}.{export_ext}"


def create_export_obj(export_data_cols, user_name, export_dir):
    # Build file name
    export_file_name = build_export_file_nm(user_name, export_dir)
    return ExportData(export_file_name, export_data_cols)


@function_timer
def create_export_df(data_file_paths, exp_df, sheet_obj_list):

    for data_file_path in data_file_paths:

        # Create an empty DataFrame to store input data
        # NOTE: Creating an empty DataFrame with a column allows data to be appended below
        temp_df = pd.DataFrame({'temp_col': []})

        # Import data from each sheet
        for sheet_obj in sheet_obj_list:
            # print(sheet_obj.name)
            sheet_df = sheet_obj.import_data(data_file_path)

            # Clean sheet data
            sheet_df = sheet_obj.clean_data(sheet_df)

            # Add imported data to new data row
            temp_df = pd.concat([temp_df, sheet_df], axis=1)

            # Clean up
            del sheet_df

            # print("Import successful")

        # Drop the temporary column used for work-around
        temp_df = temp_df.drop(columns='temp_col')

        # Add new data row
        exp_df = add_data_row(exp_df, temp_df)

        # Clean up
        del temp_df

    exp_df = re_index_df(exp_df)

    return exp_df


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
