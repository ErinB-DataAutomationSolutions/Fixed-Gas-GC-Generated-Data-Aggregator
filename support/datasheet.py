# IMPORTS
import json as js


# Config class
class Config:
    def __init__(self, file_name: str):
        # Import Config File
        with open(file_name) as config_file:
            config = js.load(config_file)

        # Set Data Directory
        self.data_dir = config["data_dir"]

        # Set Report Name
        self.report_name = config["report_name"]

        # Set report extension
        self.report_ext = config["report_ext"]

        # Set file name
        self.file_name = f"{self.report_name}.{self.report_ext}"

        # If specified data sheets are listed, get data sheets
        if "data_sheets" in config:
            self.data_sheets = config["data_sheets"]


# Class housing data sheet info
class DataSheet:
    def __init__(self, name: str, file, sheet_dict: dict):
        self.name = name
        self.sheet_dict = sheet_dict
        self.file = file

        # If data filter columns if specified
        if "filter_cols" in sheet_dict:
            self.filter_cols = sheet_dict["filter_cols"]

        # Get data filter rows if specified
        if "filter_rows" in sheet_dict:
            self.filter_rows = sheet_dict["filter_rows"]

        # Get index column if specified
        if "index_col" in sheet_dict:
            self.index_col = sheet_dict

        # Get column data map if specified
        if "col_data_map" in sheet_dict:
            self.col_data_map = sheet_dict["col_data_map"]

        # Get row data map if specified
        if "row_data_map" in sheet_dict:
            self.row_data_map = sheet_dict["row_data_map"]

    def import_data(self):
        return self.file.parse(sheet_name=self.name)
