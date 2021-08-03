########################################################################################################################
#                                                   Imports                                                            #
# -------------------------------------------------------------------------------------------------------------------- #

import tkinter as tk
from typing import Callable
import support.gui_builder as ngb
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import ttk
import new_data_upload as du


########################################################################################################################
#                                                  GLOBAL FUNCTIONS                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

def set_entry_value(entry: tk.Entry, get_func: Callable or str, start_pos: int, refresh_bool: bool) -> None:
    """

    :param entry: This is the Entry widget where a value will be copied into
    :param get_func: This is the function used to get the Entry widget value
    :param start_pos: This is the start position for the get function
    :param refresh_bool:
        - IF True:  Delete the current Entry value when executed before inserting the new one

    :return: None
    """
    if refresh_bool:
        entry.delete(0, tk.END)

    entry.insert(start_pos, get_func)


def get_file_path() -> fd.askopenfilename:
    """Get the path of a file selected in a File Selection Window"""
    return fd.askopenfilename()


def get_dir_path() -> fd.askdirectory:
    """get the path of a directory selected in a Directory Selection Window"""
    return fd.askdirectory()


def save_file(export_df):
    # Prompt user to set full file name
    export_data_full_file_name = fd.asksaveasfilename(
        defaultextension='.xlsx',
        filetypes=(
            ("Excel files", "*.xlsx"),
            ("CSV Files", "*.csv")
        )
    )

    # Create a data exporter object with the export_df and acquired full file name
    data_exporter = du.DataExporter(export_df, export_data_full_file_name)

    # Export data
    data_exporter.export()


########################################################################################################################
#                                                       CLASSES                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
class InputFormUI:
    """
This class handles the user input gathered from the Data Aggregator Input Form screen
"""
    def __init__(self):

        # Set error bool values
        self.config_file_path_input_error = False
        self.input_dir_input_error = False

        # Set placeholders
        self.output_dir_path_str = None

    @property
    def config_file_path_str(self):
        return self.config_file_path_str

    @config_file_path_str.setter
    def config_file_path_str(self, entry: "tk.Entry"):
        config_file_path_str = entry.get()

        # IF the config file path input string is empty:
        #   -
        if config_file_path_str == "":
            self.config_file_path_input_error = True
            return

        # ELSE
        self.config_file_path_str = config_file_path_str

    @property
    def input_dir_path_str(self):
        return self.input_dir_path_str

    @input_dir_path_str.setter
    def input_dir_path_str(self, entry: "tk.Entry"):
        input_dir_path_str = entry.get()

        # IF the input dir entry is missing, raise an error!
        if input_dir_path_str == "":
            self.input_dir_input_error = True
            return

        self.input_dir_path_str = input_dir_path_str

########################################################################################################################
#                                                       END FILE                                                       #
########################################################################################################################
