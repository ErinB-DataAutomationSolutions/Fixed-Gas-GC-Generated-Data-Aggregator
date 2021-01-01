# IMPORTS
import json as js


# Config class
class Config:

    def __init__(self, file_name):
        self.data_file_name = file_name

    @property
    def config(self):
        with open(self.data_file_name) as config_file:
            return js.load(config_file)

    @property
    def data_dir(self):
        return self.config["data_dir"]

    # Set Report Name
    @property
    def report_name(self):
        return self.config["report_name"]

    # Set Report Extension
    @property
    def report_ext(self):
        return self.config["report_ext"]

    # Set file name
    @property
    def full_file_name(self):
        return f"{self.report_name}.{self.report_ext}"

    # If specified data sheets are listed, get data sheets
    def data_sheets(self):
        if "data_sheets" in self.config:
            return self.config["data_sheets"]


# Class housing data sheet info
class DataSheet:
    def __init__(self, name: str, file, sheet_dict: dict):
        self.name = name
        self.sheet_dict = sheet_dict
        self.file = file

    @property
    def headers(self):
        if self.sheet_dict["headers"] == 1:
            return True
        return False

    # If data filter columns if specified
    @property
    def filter_cols(self):
        return self.sheet_dict["filter_cols"]

    # Get data filter rows if specified
    @property
    def filter_rows(self):
        return self.sheet_dict["filter_rows"]

    # Get index column if specified
    @property
    def index_cols(self):
        return self.sheet_dict

    # Get column data map if specified
    @property
    def col_data_map(self):
        return self.sheet_dict["col_data_map"]

    # Get row data map if specified
    @property
    def row_data_map(self):
        return self.sheet_dict["row_data_map"]

    @property
    def import_data(self):
        return self.file.parse(sheet_name=self.name)

    def filtered_data(self):
        pass

    def transpose_data(self):
        self.import_data = self.import_data.transpose()


class DataExport:

    def __init__(self, export_dir: str, export_file_nm: str, export_file_ext: str, export_data):
        self.export_dir = export_dir
        self.export_file_nm = export_file_nm
        self.export_data = export_data
        self.export_file_ext = export_file_ext

    def export(self):
        self.export_data.to_excel(f"{self.export_file_nm}.{self.export_file_ext}")
