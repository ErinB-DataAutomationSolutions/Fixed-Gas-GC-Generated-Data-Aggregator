# IMPORTS
import json as js
import pandas as pd


# Config class
class Config:

    """
Class Config accomplishes the following:
1) Reading and parsing a user-defined Config file
2) Parsing and storing report file metadata

Metadata captured from config JSON file:
    - Data Dir:     This is the directory housing generata data sub-directories.
    - Report Name:  This is the name of the generated report file
    - Report Ext:   File extension of the generated report file
    - Data Sheets:  Dictionary containing names, metadata, and import settings for Data Sheets
    """

    def __init__(self, config_file_name):
        self.config_file_name = config_file_name

    @property
    def config(self):
        """Open and read config file"""
        with open(self.config_file_name) as config_file:
            return js.load(config_file)

    @property
    def data_dir(self):
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
    def data_sheets(self):
        """Store data sheets dictionary, if specified"""
        if "data_sheets" in self.config:
            return self.config["data_sheets"]


# Class housing data sheet info
class DataSheet:
    def __init__(self, name: str, file, sheet_dict: dict):
        self.name = name
        self.sheet_dict = sheet_dict
        self.file = file

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
            data_map_keys.append(key)

        return data_map_keys

    @property
    def data_map_vals(self):
        data_map_vals = []

        for key in self.data_map:
            data_map_vals.append(self.data_map[key])

        return data_map_vals

    def import_data(self):
        return pd.read_excel(self.file, sheet_name=self.name, header=self.header, usecols=self.use_cols)

    def clean_data(self, data_df: pd.DataFrame):

        # Drop NA values
        data_df = data_df.dropna()

        # Transpose data, if needed
        if self.transpose_bool:
            data_df = data_df.T

        # Filter unwanted data
        data_df.columns = data_df.iloc[0]                       # Set column names to equal to row 1
        data_df = data_df.filter(items=self.data_map_keys)      # Filter out all undesired columns
        data_df = data_df.drop(index=0).reset_index(drop=True)  # Drop the now-redundant first row
        data_df = data_df.reset_index(drop=True)                # Reset Index

        data_df.columns = self.data_map_vals

        return data_df


class ExportData:

    def __init__(self, export_dir: str, export_file_nm: str, export_file_ext: str, export_data: pd.DataFrame):
        self.export_dir = export_dir
        self.export_file_nm = export_file_nm
        self.export_data = export_data
        self.export_file_ext = export_file_ext

    def add_data_row(self, temp_data: pd.DataFrame):
        self.export_data = pd.concat([self.export_data, temp_data])

    def export(self):
        self.export_data.to_excel(f"{self.export_file_nm}.{self.export_file_ext}")
