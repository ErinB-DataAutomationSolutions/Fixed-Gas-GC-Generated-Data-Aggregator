########################################################################################################################
#                                               FILE DETAILS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
# PROGRAM:  Fixed Gas Data Aggregator                                                                                  #
# Author:   Erin Bryson                                                                                                #
########################################################################################################################

########################################################################################################################
#                                                   Imports                                                            #
# -------------------------------------------------------------------------------------------------------------------- #

import json as js
import pandas as pd
import glob
from typing import Callable


########################################################################################################################
#                                                  GLOBAL FUNCTIONS                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
def re_index_df(df):
    return df.reset_index(drop=True)


def add_data_row(export_df: pd.DataFrame, temp_data: pd.DataFrame):
    return pd.concat([export_df, temp_data])


def get_input_data_file_paths(input_data_dir, input_data_file_name) -> list:
    return glob.glob(f'{input_data_dir}/**/{input_data_file_name}', recursive=True)

########################################################################################################################
#                                                       CLASSES                                                        #
# -------------------------------------------------------------------------------------------------------------------- #


class Config:
    def __init__(self):
        self._config = None

        self.file_name = None
        self.report_name = None
        self.report_ext = None
        self.datasheets_metadata = None
        self.datasheets_names = []

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config_file_name: str) -> None:
        with open(config_file_name) as config_file:
            self._config = js.load(config_file)

    def config_settings(self):
        self.report_name = self.config["report_name"]
        self.report_ext = self.config["report_ext"]
        self.datasheets_metadata = self.config["data_sheets"]

        # Store datasheet names
        for key in self.config["data_sheets"].keys():
            self.datasheets_names.append(key)

    def reset(self):
        self.__init__()


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
                return KeyError
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
    def data_map_values(self):
        data_map_values = []

        for key in self.data_map:
            data_map_values.append(self.data_map[key])

        return data_map_values

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

        if use_col_num != 1:
            # Set column names to equal to row 1
            data_df.columns = data_df.iloc[0]

        # Filter out all undesired columns
        data_df = data_df.filter(items=self.data_map_keys, axis=1)

        # print(data_df)
        data_df.columns = self.data_map_values

        if use_col_num != 1:
            # Drop the now-redundant first row
            data_df = data_df.drop(index=0).reset_index(drop=True)

        # Reset Index
        data_df = data_df.reset_index(drop=True)

        data_df.columns = self.data_map_values

        return data_df


class DataImporter:

    def __init__(self):
        self._config = None
        self._root_path = ""

        self.import_file_path_list = None
        self.data_map = {}
        self.agg_data_df_cols = []
        self.datasheet_object_list = []
        self.agg_data_df = None
        self.file_count = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config: "Config"):
        self._config = config

    @property
    def root_path(self):
        return self._root_path

    @root_path.setter
    def root_path(self, root_path):
        self._root_path = root_path

    def config_import_settings(self):

        self.import_file_path_list = get_input_data_file_paths(
            self.root_path,
            f"{self.config.report_name}.{self.config.report_ext}"
        )

        self.file_count = len(self.import_file_path_list)

        # Populate sheet_obj_list with constructed sheet objects
        for datasheet_name in self.config.datasheets_names:

            # Get metadata for specific sheet
            datasheet_metadata = self.config.datasheets_metadata[datasheet_name]

            # Create a datasheet object for each datasheet
            sheet_obj = DataSheet(datasheet_name, datasheet_metadata)

            # Build list of aggregated data DataFrame columns
            for data_map_value in sheet_obj.data_map_values:
                self.agg_data_df_cols.append(data_map_value)

            # Add datasheet object to the list of datasheets
            self.datasheet_object_list.append(sheet_obj)

        self.agg_data_df = pd.DataFrame(columns=self.agg_data_df_cols)

    def concat_import_data(self, data_file_path):
        # Create an empty DataFrame to store input data
        # NOTE: Creating an empty DataFrame with a column allows data to be appended below
        temp_df = pd.DataFrame({'temp_col': []})

        # Import data from each sheet
        for datasheet_object in self.datasheet_object_list:
            # print(sheet_obj.name)
            sheet_df = datasheet_object.import_data(data_file_path)

            # Clean sheet data
            sheet_df = datasheet_object.clean_data(sheet_df)

            # Add imported data to new data row
            temp_df = pd.concat([temp_df, sheet_df], axis=1)

            # Clean up
            del sheet_df

        # Drop the temporary column used for work-around
        temp_df = temp_df.drop(columns='temp_col')

        # Add new data row
        self.agg_data_df = add_data_row(self.agg_data_df, temp_df)

        # Clean up
        del temp_df

    def aggregate_data(self, status_message_func: Callable = None, download_button=None, progress_bar=None):
        progress_num = 0

        # progress_bar['maximum'] = self.file_count

        if progress_bar:
            progress_bar['maximum'] = self.file_count

        for data_file_path in self.import_file_path_list:

            # Concat datasheet data
            self.concat_import_data(data_file_path)

            # Increment file_counter by 1
            progress_num += 1

            # Pass file number into Callable Status Message Function
            if status_message_func:
                status_message_func(progress_num)

        # Re-Index Aggregated Data
        self.agg_data_df = re_index_df(self.agg_data_df)

        download_button['state'] = 'active'

    def reset(self):
        self.__init__()


class DataExporter:

    def __init__(self, export_df, export_data_full_file_name):
        self.export_df = export_df
        self.export_data_full_file_name = export_data_full_file_name

        # Fine position of final "."
        ext_start_pos = self.export_data_full_file_name.rfind(".")

        # Get the file extension
        file_ext = self.export_data_full_file_name[ext_start_pos + 1:]

        # IF file extension is supported, set the file_ext property value
        if file_ext in self.supported_ext.keys():
            self.file_ext = file_ext

    @property
    def supported_ext(self):
        return {
            "xlsx": self.export_df.to_excel,
            "csv": self.export_df.to_csv
        }

    def export(self):
        self.supported_ext[self.file_ext](self.export_data_full_file_name)

########################################################################################################################
#                                                       END FILE                                                       #
########################################################################################################################
