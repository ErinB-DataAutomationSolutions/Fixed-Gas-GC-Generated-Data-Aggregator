# IMPORTS
import json


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
