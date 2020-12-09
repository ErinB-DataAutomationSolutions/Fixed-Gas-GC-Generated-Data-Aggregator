# IMPORTS
import json as js


# Config class
class Config:
    def __init__(self, file_name: str):
        # Import Config File
        with open("config.json") as config_file:
            config = js.load(config_file)

        # Set Data Directory
        self.data_dir = config["data_dir"]

        # Set Report Name
        self.report_name = config["report_name"]

        # If specified data sheets are listed, get data sheets
        if "data_sheets" in config:
            pass
        pass


# Class housing data sheet info
class DataSheet:
    def __init__(self, name: str, sheet_dict: dict):
        self.name = name
        self.sheet_dict = sheet_dict
        pass

    def print_sheet_dict(self):
        print(self.sheet_dict)
        pass

    def get_filter_cols(self):
        pass

    def get_filter_rows(self):
        pass

    def get_index_col(self):
        pass

    def get_col_data_map(self):
        pass

    def get_row_data_map(self):
        pass
