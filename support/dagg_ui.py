########################################################################################################################
#                                                   Imports                                                            #
# -------------------------------------------------------------------------------------------------------------------- #

import os
import tkinter as tk
from typing import Callable
import support.gui_builder as gb
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import ttk
import support.data_upload as du
import threading
import json


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

        self._config_file_path_str = ""
        self._input_dir_path_str = ""

        # Set placeholders
        self.output_dir_path_str = None

    @property
    def config_file_path_str(self):
        return self._config_file_path_str

    @config_file_path_str.setter
    def config_file_path_str(self, entry_str: str):
        config_file_path_str = entry_str

        # IF the config file path input string is empty:
        #   -
        if config_file_path_str == "":
            self.config_file_path_input_error = True
            return

        # ELSE
        self._config_file_path_str = config_file_path_str

    @property
    def input_dir_path_str(self):
        return self._input_dir_path_str

    @input_dir_path_str.setter
    def input_dir_path_str(self, entry_str: str):
        input_dir_path_str = entry_str

        # IF the input dir entry is missing, raise an error!
        if input_dir_path_str == "":
            self.input_dir_input_error = True
            return

        self._input_dir_path_str = input_dir_path_str


class DataMapPairUI:
    # Track number of data map pairs
    counter = 0

    def __init__(self):
        # Set ID
        self.id = DataMapPairUI.counter

        # Placeholders
        self._key = ""
        self._value = ""

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key: str) -> None:
        self._key = key

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value


class DataMapPairGUI(DataMapPairUI):
    """
Inherit DataMapPair UI and build the GUI
    """
    def __init__(self, datasheet_gui: "DatasheetGUI"):
        # Create an associated Data Map Pair UI
        super().__init__()

        self.datasheet_gui = datasheet_gui

        # Assign master
        self.master = self.datasheet_gui.frame_data_map

        # Assign Associated Row
        self.row = self.datasheet_gui.data_map_row_counter

        # Create Entry: Key
        self.entry_key = tk.Entry(
            self.master
        )

        # Create Entry: Value
        self.entry_value = tk.Entry(
            self.master
        )

        # Build the row
        self.build_row()

    def build_row(self):
        # 0) Frame: Padding
        frame_padding = tk.Frame(
            self.master,
            width=25
        )

        # Place Padding Frame
        frame_padding.grid(
            row=self.row,
            column=0
        )

        # Place Key Entry
        self.entry_key.grid(
            row=self.row,
            column=1
        )

        # 2) Label: Separator
        label_separator = tk.Label(
            self.master,
            text=":"
        )

        # Place Separator Label
        label_separator.grid(
            row=self.row,
            column=2,
            padx=1
        )

        # Place Value Entry
        self.entry_value.grid(
            row=self.row,
            column=3
        )

        button_remove_row = tk.Button(
            self.master,
            text="-",
            width=2,
            command=lambda: self.delete(
                frame_padding,
                self.entry_key,
                label_separator,
                self.entry_value,
                button_remove_row
            )
        )

        # Place Remove Row Button
        button_remove_row.grid(
            row=self.row,
            column=4,
            padx=1,
        )

    def delete(self, *widgets: tk.Widget):
        self.datasheet_gui.remove_data_map_row(self)

        # Forget each widget in row
        for widget in widgets:
            widget.destroy()

        # Delete DataMapUI object
        del self

    def submit(self):
        # Set Key
        self.key = self.entry_key.get()
        self.value = self.entry_value.get()


class DatasheetUI:
    """
Class to store Datasheet Metadata from Config Builder screen
    """

    def __init__(self) -> None:

        # Set name
        self._name = ""

        # Set placeholders
        self._headers_bool = False
        self.headers = []
        self._transpose_bool = False
        self.data_map = {}

        # Error Bool Values:
        self._name_error_bool = False

        # Increment counter by 1
        DataMapPairUI.counter += 1

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def headers_bool(self) -> bool:
        """
        Return boolean value (True or False) of headers_bool
        :return: Bool
        """
        return self._headers_bool

    @headers_bool.setter
    def headers_bool(self, bool_value: bool) -> None:
        """
        Set the headers_bool value to either True or False; default is False
        :param bool_value:
        :return: None
        """
        self._headers_bool = bool_value

    @property
    def transpose_bool(self) -> bool:
        return self._transpose_bool

    @transpose_bool.setter
    def transpose_bool(self, bool_value: bool) -> None:
        """
        Set the transpose_bool value to either True or False; default is False
        :param bool_value: A boolean value
        :return: None
        """
        self._transpose_bool = bool_value

    @property
    def name_error_bool(self) -> bool:
        return self._name_error_bool

    @name_error_bool.setter
    def name_error_bool(self, error_bool: bool) -> None:
        self._name_error_bool = error_bool


class DatasheetGUI(DatasheetUI):
    # Track number of datasheet objects
    counter = 0

    def __init__(self, config_file_gui: "ConfigFileBuilderGUI"):
        super().__init__()

        # Assign ID, then increment counter by 1
        self.id = DatasheetGUI.counter
        DatasheetGUI.counter += 1

        # Assign the associated config file UI
        self.config_file_gui = config_file_gui

        # Header Row Counter
        self.header_row_counter = 0

        self.notebook_datasheets = self.config_file_gui.notebook_datasheets.widget_object

        self.checkbutton_transpose_bool_var = tk.IntVar()

        # Track number of data map rows
        self.data_map_row_counter = 0

        # Placeholders:
        #   Lists:
        self.entry_headers = []
        self.data_map_pairs = []

        #   Frames:
        self.frame_headers_entry_section = None
        self.frame_data_map = None
        self.frame_tab = None

        #   Widgets:
        self.entry_name = None
        self.checkbutton_transpose_bool = None

    def build_gui(self):
        # Create a frame for the notebook tab
        self.frame_tab = tk.Frame(
            self.notebook_datasheets
        )

        self.frame_tab.pack(fill=tk.X)

        # Add datasheet tab to the datasheet notebook
        self.notebook_datasheets.add(self.frame_tab, text=f"Datasheet {self.id}")

        # Create Frame for Static Metadata
        frame_static_metadata = tk.Frame(
            self.frame_tab
        )

        frame_static_metadata.pack(fill=tk.X)

        # Create Label: Datasheet Name
        label_datasheet_name = tk.Label(
            frame_static_metadata,
            text="Datasheet Name:"
        )

        label_datasheet_name.grid(
            row=0,
            column=0
        )

        # Create Entry: Datasheet Name
        self.entry_name = tk.Entry(
            frame_static_metadata
        )

        self.entry_name.grid(
            row=0,
            column=1
        )

        #

        # RadioButton: Transpose Data
        self.checkbutton_transpose_bool = tk.Checkbutton(
            frame_static_metadata,
            text="Transpose Data",
            variable=self.checkbutton_transpose_bool_var
        )

        self.checkbutton_transpose_bool.grid(
            row=2,
            column=0
        )

        # Create Frame: Headers
        frame_headers_label_section = tk.Frame(
            self.frame_tab
        )

        frame_headers_label_section.pack(fill=tk.X)

        # Create Label: Input Table Headers:
        label_input_table_headers = tk.Label(
            frame_headers_label_section,
            text="Input Table Headers"
        )

        label_input_table_headers.grid(
            row=0,
            column=0
        )

        # Create Button: Add Header Entry
        button_build_input_table_header_row = tk.Button(
            frame_headers_label_section,
            text="+",
            width=2,
            command=lambda: self.build_entry_header_row()
        )

        button_build_input_table_header_row.grid(
            row=0,
            column=1,
            padx=1
        )

        self.frame_headers_entry_section = tk.Frame(
            self.frame_tab
        )

        self.frame_headers_entry_section.pack(fill=tk.X)

        # Create Frame: Data Map Section Label
        frame_data_map_section_label = tk.Frame(
            self.frame_tab
        )

        frame_data_map_section_label.pack(fill=tk.X)

        # Label: Data Map
        label_data_map = tk.Label(
            frame_data_map_section_label,
            text="Data Map:"
        )

        label_data_map.grid(
            row=0,
            column=0
        )

        # Button: Build Data Map Row
        button_build_data_map_row = tk.Button(
            frame_data_map_section_label,
            text="+",
            width=2,
            command=lambda: self.build_data_map_row()
        )

        button_build_data_map_row.grid(
            row=0,
            column=1,
            padx=1
        )

        # Create frame: Data Map
        self.frame_data_map = tk.Frame(
            self.frame_tab
        )

        self.frame_data_map.pack(fill=tk.X)

        # Create Frame: Remove Datasheet
        frame_remove_datasheet = tk.Frame(
            self.frame_tab
        )

        frame_remove_datasheet.pack(fill=tk.X, padx=5, pady=5)

        # Button: Remove Datasheet
        button_remove_datasheet = tk.Button(
            frame_remove_datasheet,
            text="Remove",
            command=lambda: self.delete()
        )

        button_remove_datasheet.pack(side=tk.RIGHT)
        pass

    def build_entry_header_row(self):
        # row = self.header_row_counter.get()
        row = self.header_row_counter

        # Create Frame: Padding
        frame_padding = tk.Frame(
            self.frame_headers_entry_section,
            width=25
        )

        frame_padding.grid(
            row=row,
            column=0
        )

        # Create Entry: Header
        entry_header = tk.Entry(
            self.frame_headers_entry_section
        )

        self.entry_headers.append(entry_header)

        entry_header.grid(
            row=row,
            column=1
        )

        # Create button to remove entry header row
        button_remove_entry_header_row = tk.Button(
            self.frame_headers_entry_section,
            text="-",
            width=2,
            command=lambda: self.remove_entry_header_row(
                frame_padding,
                entry_header,
                button_remove_entry_header_row
            )
        )

        button_remove_entry_header_row.grid(
            row=row,
            column=2,
            padx=1
        )

        # Increment entry_headers_row_num by 1
        self.header_row_counter += 1

        # Update application
        self.config_file_gui.app.update_idletasks()

    def remove_entry_header_row(self, *widgets: tk.Widget):
        # row = self.header_row_counter.get()

        # Destroy all widgets in the row
        for widget in widgets:

            # If the widget is an entry header, remove from the entry headers list
            if widget in self.entry_headers:
                self.entry_headers.pop(
                    self.entry_headers.index(widget)
                )

            # widget.grid_forget()
            widget.destroy()

        # Update application
        self.config_file_gui.app.update_idletasks()

    def build_data_map_row(self):
        self.data_map_pairs.append(DataMapPairGUI(self))

        # Increase Data Map Row by 1
        self.data_map_row_counter += 1

        # Update Application
        self.config_file_gui.app.update_idletasks()

    def remove_data_map_row(self, data_map_pair_gui: "DataMapPairGUI"):
        # Pop data map row from data_map_rows list
        self.data_map_pairs.pop(
            self.data_map_pairs.index(data_map_pair_gui)
        )

        # Update application
        self.config_file_gui.app.update_idletasks()

    def delete(self):
        continue_bool = messagebox.askyesno("Remove Datasheet", "Are you sure you want to remove this datasheet?")

        if continue_bool:
            # Destroy the frame
            self.frame_tab.destroy()

            # Delete self
            self.config_file_gui.remove_datasheet_gui(self)

            del self

    def submit(self):
        # Set the entry name
        name = self.entry_name.get()

        # IF name is an empty string, set name_error_bool to TRUE
        if name == "":
            self.name_error_bool = True

        if self.name_error_bool:
            # End submit function execution
            return

        self.name = name

        # Set the Transpose BOOL
        if self.checkbutton_transpose_bool_var.get():
            self.transpose_bool = True

        # Set the Table Headers
        for entry_header in self.entry_headers:
            header = entry_header.get()
            if header != "":
                self.headers.append(entry_header.get())

        if len(self.headers):
            self.headers_bool = True

        # Set the Data Map Values
        for data_map_pair in self.data_map_pairs:
            # Call submit method in data_map_pair object
            data_map_pair.submit()

            # Add the data map pair to the Data Map dictionary
            self.data_map[data_map_pair.key] = data_map_pair.value


class ConfigFileBuilderUI:
    """
Class to store Config File data form Config Builder screen
    """
    def __init__(self):
        self._report_name = ""
        self._report_ext = ""
        self._report_name_error_bool = False
        self._report_ext_error_bool = False

        self.datasheets = dict()

    @property
    def report_name(self) -> str:
        return self._report_name

    @report_name.setter
    def report_name(self, report_name: str) -> None:
        self._report_name = report_name

    @property
    def report_ext(self) -> str:
        return self._report_ext

    @report_ext.setter
    def report_ext(self, report_ext: str) -> None:
        self._report_ext = report_ext

    @property
    def report_name_error_bool(self) -> bool:
        return self._report_name_error_bool

    @report_name_error_bool.setter
    def report_name_error_bool(self, error_bool: bool) -> None:
        self._report_name_error_bool = error_bool

    @property
    def report_ext_error_bool(self) -> bool:
        return self._report_ext_error_bool

    @report_ext_error_bool.setter
    def report_ext_error_bool(self, error_bool: bool) -> None:
        self._report_ext_error_bool = error_bool


class ConfigFileBuilderGUI(ConfigFileBuilderUI):

    def __init__(self, app: "gb.Application", parent_screen: "gb.ScreenContainer") -> None:
        """
        Initialize the Config File Builder GUI.
        """
        super().__init__()

        # Set application object
        self.app = app

        # Set parent screen
        self.parent_screen = parent_screen

        # Set placeholders
        self.datasheets_gui_list = []

        # Elements Place Holders:
        self.combobox_report_file_ext = None
        self.entry_report_file_name = None
        self.notebook_datasheets = None
        self.button_download = None

    def build_gui(self, screen: "gb.ScreenContainer") -> None:
        # Build Child Containers:
        # 1) Child Container: Report File
        child_container_report_file = gb.ChildContainer(
            screen
        )

        child_container_report_file.set_pack_options(fill=tk.X, padx=5)

        # Label: Report File
        label_report_file = gb.WidgetBuilder(
            child_container_report_file,
            tk.Label,
            text="Report File:"
        )

        label_report_file.set_placement_settings(
            sticky="w"
        )

        # Entry: Report File Name
        self.entry_report_file_name = gb.WidgetBuilder(
            child_container_report_file,
            tk.Entry
        )

        # Label: Report File Ext
        label_report_file_ext = gb.WidgetBuilder(
            child_container_report_file,
            tk.Label,
            text="."
        )

        label_report_file_ext.set_placement_settings(
            padx=1
        )

        # ComboBox: File Ext
        self.combobox_report_file_ext = gb.WidgetBuilder(
            child_container_report_file,
            ttk.Combobox,
            values=(
                "xls",
                "xlsx",
                "csv"
            ),
            width=4,
            state='readonly'
        )

        self.combobox_report_file_ext.set_placement_settings(padx=1)

        child_container_report_file.new_build_row(
            label_report_file,
            self.entry_report_file_name,
            label_report_file_ext,
            self.combobox_report_file_ext
        )

        # 2) Notebook section label
        child_container_datasheets_section_label = gb.ChildContainer(
            screen
        )

        child_container_datasheets_section_label.set_pack_options(fill=tk.X, padx=5)

        # Label: Datasheets Section
        label_datasheets_section = gb.WidgetBuilder(
            child_container_datasheets_section_label,
            tk.Label,
            text="Datasheets"
        )

        # Button: Add Datasheet
        button_add_datasheets = gb.WidgetBuilder(
            child_container_datasheets_section_label,
            tk.Button,
            text="+",
            width=2,
            command=lambda: self.add_datasheet_gui()
        )

        button_add_datasheets.set_placement_settings(padx=1)

        child_container_datasheets_section_label.new_build_row(
            label_datasheets_section,
            button_add_datasheets
        )

        # 3) Child Container: Datasheets Notebook
        child_container_datasheets_notebook = gb.ChildContainer(
            screen
        )

        child_container_datasheets_notebook.set_pack_options(fill=tk.X, padx=5)

        # Notebook:
        self.notebook_datasheets = gb.WidgetBuilder(
            child_container_datasheets_notebook,
            ttk.Notebook
        )

        self.notebook_datasheets.set_placement_settings(fill=tk.X)

        child_container_datasheets_notebook.pack_widget(self.notebook_datasheets)

        # 4) Child Container: Submit
        child_container_submit = gb.ChildContainer(
            screen
        )

        child_container_submit.set_pack_options(side=tk.RIGHT, padx=5)

        # Button: Clear
        button_clear = gb.WidgetBuilder(
            child_container_submit,
            tk.Button,
            text="Clear",
            command=lambda: self.refresh()
        )

        button_clear.set_placement_settings(padx=5)

        # Button: Submit
        button_submit = gb.WidgetBuilder(
            child_container_submit,
            tk.Button,
            text="Submit",
            command=lambda: self.submit()
        )

        button_submit.set_placement_settings(padx=5)

        # Button: Download
        self.button_download = gb.WidgetBuilder(
            child_container_submit,
            tk.Button,
            text="Download",
            state=tk.DISABLED,
            command=lambda: self.download()
        )

        self.button_download.set_placement_settings(padx=5)

        # self.child_container_submit.pack_widget(button_submit)
        child_container_submit.new_build_row(
            button_clear,
            button_submit,
            self.button_download
        )

    def add_datasheet_gui(self) -> None:
        """
        Add a Datasheet GUI object to the Datasheet GUI List
        :return: None
        """
        # Create

        # Add Datasheet object to datasheets list
        datasheet_gui = DatasheetGUI(self)

        self.datasheets_gui_list.append(
            datasheet_gui
        )

        datasheet_gui.build_gui()

        # Update Application
        self.app.update_idletasks()

    def remove_datasheet_gui(self, datasheet_gui: "DatasheetGUI") -> None:
        """
        Remove Datasheet GUI Object from the Datasheet GUI List
        :param datasheet_gui: DatasheetGUI Object
        :return: None
        """

        # Remove Datasheet object from Datasheets
        self.datasheets_gui_list.pop(
            self.datasheets_gui_list.index(datasheet_gui)
        )

        # Update Application
        self.app.update_idletasks()

    def submit(self):
        # Assign Report Name and Ext
        report_name = self.entry_report_file_name.widget_object.get()
        report_ext = self.combobox_report_file_ext.widget_object.get()

        # IF report name is an empty string, set report_name_error_bool to TRUE
        if report_name == "":
            self.report_name_error_bool = True

        # IF report ext is an empty string, set report_ext_error_bool to TRUE
        if report_ext == "":
            self.report_ext_error_bool = True

        if self.report_name_error_bool or self.report_ext_error_bool:
            # Show error message
            messagebox.showerror(
                title="Required Info Missing",
                message="Required fields must be filled before submitting!"
            )

            # Reset error bool values
            self.report_name_error_bool = False
            self.report_ext_error_bool = False

            return

        # Store the Report Name and Report Ext
        self.report_name = report_name
        self.report_ext = report_ext

        # Get info for all Datasheets
        for datasheet_gui in self.datasheets_gui_list:
            # Set datasheet values
            datasheet_gui.submit()

            if datasheet_gui.name_error_bool:
                # Display error message
                messagebox.showerror(
                    title="Required Info Missing",
                    message="Required fields must be filled before submitting!"
                )
                datasheet_gui.name_error_bool = False

                # End submit execution
                return

            metadata_dict = dict()

            metadata_dict["transpose_bool"] = datasheet_gui.transpose_bool
            metadata_dict["headers_bool"] = datasheet_gui.headers_bool

            if datasheet_gui.headers_bool:
                metadata_dict["headers_nm"] = datasheet_gui.headers

            metadata_dict["data_map"] = datasheet_gui.data_map

            datasheet_name = datasheet_gui.name

            # Build Datasheets Dictionary
            self.datasheets[datasheet_name] = metadata_dict
        # Enable download button
        self.button_download.widget_object["state"] = tk.ACTIVE

    def download(self):
        # Create an empty export dictionary
        config_file_dict = {
            "report_name": self.report_name,
            "report_ext": self.report_ext,
            "data_sheets": self.datasheets
        }

        # Get file name
        json_file_name = fd.asksaveasfilename(
                    defaultextension=".json"
                )

        # Write the new JSON file
        with open(
                json_file_name,
                'w'
        ) as new_config_file:
            json.dump(config_file_dict, new_config_file)

        # Open the file
        os.startfile(json_file_name)

        # Refresh the screen
        self.refresh()

        # Show the parent screen
        self.app.show_screen(self.parent_screen)

        # Update Application
        self.app.update_idletasks()

    def refresh(self):

        # Clear Entry Values
        self.entry_report_file_name.widget_object.delete(0, tk.END)
        self.combobox_report_file_ext.widget_object.set('')

        # Set saved values
        self.report_name = ""
        self.report_ext = ""

        # Clear Datasheets
        for datasheet_gui in self.datasheets_gui_list:
            datasheet_gui.delete()

        DatasheetGUI.counter = 0

        # Destroy each remaining tab
        for tab in self.notebook_datasheets.widget_object.winfo_children():
            tab.destroy()

        # Reset Datasheets Dictionary
        self.datasheets = {}

        self.button_download.widget_object['state'] = tk.DISABLED

        self.app.update_idletasks()


########################################################################################################################
#                                                  BUILD GUI                                                           #
# -------------------------------------------------------------------------------------------------------------------- #

# Create an instance of the UI
input_form_ui = InputFormUI()

# Create an instance of the application
application = gb.Application()

# Global string var to be used throughout program
global_string_var = tk.StringVar()
global_string_var.set("")

# Global IntVar to be used throughout program
global_int_var = tk.IntVar()

# Create Config Object
config = du.Config()

# Create Data Importer object
data_importer = du.DataImporter()

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  Create screens                                                      #
# -------------------------------------------------------------------------------------------------------------------- #

# Start Screen
screen_start = gb.ScreenContainer(application, True)

# Data Aggregator Config Form Screen
screen_data_agg_config_form = gb.ScreenContainer(application)

# Data Aggregator Confirmation Screen
screen_data_agg_input_confirmation = gb.ScreenContainer(application)

# Data Aggregator Importing Loading Screen
screen_data_import = gb.ScreenContainer(application)

#  Config File Builder Screen
screen_config_file_builder = gb.ScreenContainer(application)

# Create Help Screen
screen_help = gb.ScreenContainer(application)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                    Build Screens                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
def new_build_screen_start() -> None:
    # Build title label
    screen_start.build_title_label(
        text="Fixed Gas GC Data Aggregator",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    child_container_start_menu = gb.ChildContainer(
        screen_start
    )

    # Button for Data Aggregator Config Form
    button_screen_data_agg_config_form = gb.WidgetBuilder(
        child_container_start_menu,
        tk.Button,
        text="Aggregate Data",
        command=lambda: application.show_screen(screen_data_agg_config_form)
    )

    button_screen_data_agg_config_form.set_placement_settings(sticky="ew", pady=1)

    child_container_start_menu.new_build_row(button_screen_data_agg_config_form)

    # Button for Config File Builder
    button_screen_config_file_builder = gb.WidgetBuilder(
        child_container_start_menu,
        tk.Button,
        text="Build Config File",
        command=lambda: application.show_screen(screen_config_file_builder)
    )

    button_screen_config_file_builder.set_placement_settings(sticky="ew", pady=1)

    child_container_start_menu.new_build_row(button_screen_config_file_builder)

    # Button for Help Screen
    button_screen_help = gb.WidgetBuilder(
        child_container_start_menu,
        tk.Button,
        text="Help",
        command=lambda: application.show_screen(screen_help)
    )

    button_screen_help.set_placement_settings(sticky="ew", pady=1)

    child_container_start_menu.new_build_row(button_screen_help)

    # Button Quit
    button_quit = gb.WidgetBuilder(
        child_container_start_menu,
        tk.Button,
        text="Quit",
        command=lambda: application.close_application()
    )

    button_quit.set_placement_settings(sticky="ew", pady=1)

    child_container_start_menu.new_build_row(button_quit)


def build_screen_help() -> None:
    screen_help.build_title_label(
        text="Help",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    child_container_help_messages = gb.ChildContainer(
        screen_help
    )

    # Create a child container for the help messages
    child_container_help_messages.set_pack_options(fill=tk.X)
    child_container_help_messages.config_column(0, weight=1)

    # LabelFrame for Data Aggregator help section
    labelframe_data_aggregator = gb.WidgetBuilder(
        child_container_help_messages,
        tk.LabelFrame,
        text="Data Aggregator"
    )

    labelframe_data_aggregator.set_placement_settings(
        sticky="ew",
        padx=5
    )

    label_data_aggregator = tk.Label(
        labelframe_data_aggregator.widget_object,
        text="Coming Soon!",
        justify=tk.LEFT
    )

    label_data_aggregator.pack(side=tk.LEFT)

    child_container_help_messages.new_build_row(labelframe_data_aggregator)

    labelframe_config_file_builder = gb.WidgetBuilder(
        child_container_help_messages,
        tk.LabelFrame,
        text="Config File Builder"
    )

    label_config_file_builder = tk.Label(
        labelframe_config_file_builder.widget_object,
        text="Coming Soon!",
        justify=tk.LEFT
    )

    labelframe_config_file_builder.set_placement_settings(
        sticky="ew",
        padx=5,
        pady=10
    )

    label_config_file_builder.pack(side=tk.LEFT)

    child_container_help_messages.new_build_row(labelframe_config_file_builder)

    screen_help.build_back_button(screen_start)


def new_build_screen_data_agg_config_form() -> None:
    # Build the Screen Title
    screen_data_agg_config_form.build_title_label(
        text="Data Aggregator: Configuration Settings",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    # CHILD CONTAINER 1: FORM ENTRY
    # Create a child container for the Form entry
    child_container_form_input = gb.ChildContainer(screen_data_agg_config_form)
    child_container_form_input.set_pack_options(fill=tk.X)

    # Column configure
    child_container_form_input.config_column(1, weight=3)

    # ROW 1: CONFIG FILE
    # Label
    label_config_file = gb.WidgetBuilder(
        child_container_form_input,
        tk.Label,
        text="Config File:"
    )

    label_config_file.set_placement_settings(sticky="e")

    # Entry
    entry_config_file = gb.WidgetBuilder(
        child_container_form_input,
        tk.Entry
    )

    entry_config_file.set_placement_settings(sticky="ew")

    # Button
    button_config_file = gb.WidgetBuilder(
        child_container_form_input,
        tk.Button,
        text="Browse",
        command=lambda: set_entry_value(entry_config_file.widget_object, get_file_path(), 0, True)
    )

    button_config_file.set_placement_settings(padx=5)

    # Build row
    child_container_form_input.new_build_row(
        label_config_file,
        entry_config_file,
        button_config_file
    )

    # ROW 2: INPUT DIRECTORY
    # Label
    label_input_directory = gb.WidgetBuilder(
        child_container_form_input,
        tk.Label,
        text="Input Folder:"
    )

    label_input_directory.set_placement_settings(sticky="e")

    # Entry
    entry_input_directory = gb.WidgetBuilder(
        child_container_form_input,
        tk.Entry
    )

    entry_input_directory.set_placement_settings(sticky="ew")

    # Button
    button_input_directory = gb.WidgetBuilder(
        child_container_form_input,
        tk.Button,
        text="Browse",
        command=lambda: set_entry_value(entry_input_directory.widget_object, get_dir_path(), 0, True)
    )

    button_input_directory.set_placement_settings(padx=5)

    # Build Row:
    child_container_form_input.new_build_row(
        label_input_directory,
        entry_input_directory,
        button_input_directory
    )

    # CHILD CONTAINER 2: END FORM
    child_container_form_end = gb.ChildContainer(
        screen_data_agg_config_form
    )

    child_container_form_end.set_pack_options(
        side=tk.RIGHT,
        pady=10
    )

    # Button: Clear
    def clear() -> None:
        # Clear stored UI values:
        input_form_ui.config_file_path_str = None
        input_form_ui.input_dir_path_str = None

        # Clear each entry
        entry_config_file.widget_object.delete(0, tk.END)
        entry_input_directory.widget_object.delete(0, tk.END)

        print("Form was cleared!")

    button_end_form_clear = gb.WidgetBuilder(
        child_container_form_end,
        tk.Button,
        text="Clear",
        command=lambda: clear()
    )

    button_end_form_clear.set_placement_settings(padx=5)

    # Button: Submit
    def submit() -> None:
        # Reset UI error values:
        input_form_ui.config_file_path_input_error = False
        input_form_ui.input_dir_input_error = False

        # Set Input Form UI Variables
        input_form_ui.config_file_path_str = entry_config_file.widget_object.get()
        input_form_ui.input_dir_path_str = entry_input_directory.widget_object.get()

        # Check if all required entries were filled
        if input_form_ui.config_file_path_input_error or input_form_ui.input_dir_input_error:
            # Don't allow user to continue
            messagebox.showwarning(
                title="Required Input Missing",
                message="Please fill out all required fields!"
            )

            # Don't submit
            return

        # Store the input values to the global_string_var
        global_string_var.set(
            f"\nConfig File:\t{input_form_ui.config_file_path_str}"
            f"\nInput Folder:\t{input_form_ui.input_dir_path_str}"
        )

        application.update_idletasks()

        # Confirm Form Submitted
        print("Form was submitted!")

        # Go to the info confirmation screen
        application.show_screen(screen_data_agg_input_confirmation)

    button_end_form_submit = gb.WidgetBuilder(
        child_container_form_end,
        tk.Button,
        text="Submit",
        command=lambda: submit()
    )

    button_end_form_submit.set_placement_settings(padx=5)

    # Build row
    child_container_form_end.new_build_row(
        button_end_form_clear,
        button_end_form_submit
    )

    # BACK BUTTON
    screen_data_agg_config_form.build_back_button(screen_start)


def build_screen_data_agg_input_confirmation() -> None:
    screen_data_agg_input_confirmation.build_title_label(
        text="Input Confirmation",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    child_container_message = gb.ChildContainer(
        screen_data_agg_input_confirmation
    )

    child_container_message.set_pack_options(fill=tk.X)

    text_instructions = "Please review your configuration settings below."

    label_instructions = gb.WidgetBuilder(
        child_container_message,
        tk.Label,
        text=text_instructions,
        # justify=tk.LEFT
    )

    child_container_message.new_build_row(
        label_instructions
    )

    # Build the Label form input values widget
    label_form_input_values = gb.WidgetBuilder(
        child_container_message,
        tk.Label,
        # text=text_instructions + text_config_settings
        textvariable=global_string_var,
        justify=tk.LEFT
    )

    child_container_message.new_build_row(
        label_form_input_values
    )

    child_container_confirm_button = gb.ChildContainer(
        screen_data_agg_input_confirmation
    )

    child_container_confirm_button.set_pack_options(
        side=tk.RIGHT,
        padx=5
    )

    def confirm() -> None:
        # Import config settings
        config.config = input_form_ui.config_file_path_str

        # Configure settings
        config.config_settings()

        # Get the config data
        data_importer.config = config
        data_importer.root_path = input_form_ui.input_dir_path_str
        data_importer.config_import_settings()

        # Set global int var to total number of files
        global_int_var.set(data_importer.file_count)
        global_string_var.set(f"0 out of {global_int_var.get()} files uploaded...")

        application.update_idletasks()

        # Show the Data Import screen
        application.show_screen(screen_data_import)

    button_confirm = gb.WidgetBuilder(
        child_container_confirm_button,
        tk.Button,
        text="Confirm",
        command=lambda: confirm()
    )

    child_container_confirm_button.new_build_row(
        button_confirm
    )

    screen_data_agg_input_confirmation.build_back_button(screen_data_agg_config_form)


def build_screen_data_import() -> None:
    # Build Title Label
    screen_data_import.build_title_label(
        text="Importing Data",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    child_container_loading_status = gb.ChildContainer(
        screen_data_import
    )

    child_container_loading_status.config_column(0, weight=1)

    label_loading_status = gb.WidgetBuilder(
        child_container_loading_status,
        tk.Label,
        textvariable=global_string_var
    )

    child_container_loading_status.new_build_row(
        label_loading_status
    )

    child_container_loading_status.set_pack_options(fill=tk.X)

    progress_bar_upload = gb.WidgetBuilder(
        child_container_loading_status,
        ttk.Progressbar,
        mode='determinate',
        orient=tk.HORIZONTAL
    )

    progress_bar_upload.set_placement_settings(sticky="ew", padx=5)

    child_container_loading_status.new_build_row(progress_bar_upload)

    # Action Buttons
    child_container_action_buttons = gb.ChildContainer(
        screen_data_import
    )

    # child_container_action_buttons.config_column(0, weight=1)

    child_container_action_buttons.set_pack_options(
        fill=tk.X,
        pady=10
    )

    # Download Buttons
    button_download = gb.WidgetBuilder(
        child_container_action_buttons,
        tk.Button,
        text="Download File",
        state=tk.DISABLED,
        command=lambda: download()
    )

    button_download.set_placement_settings(
        padx=5
    )

    def progress_update(file_num) -> None:
        # Set the progress value equal to the file number processed
        progress_bar_upload.widget_object['value'] += 1
        global_string_var.set(f"{file_num} out of {global_int_var.get()} files uploaded...")

        application.update_idletasks()

    def upload() -> None:
        # Dedicate thread to uploading data
        thread_upload = threading.Thread(
            target=data_importer.aggregate_data(
                status_message_func=progress_update,
                download_button=button_download.widget_object,
                progress_bar=progress_bar_upload.widget_object
            )
        )

        # Start new thread
        thread_upload.start()

        # button_download.widget_object["command"] = lambda: download()

    def download() -> None:
        export_data_full_file_name = fd.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=(
                ("Excel files", "*.xlsx"),
                ("CSV Files", "*.csv")
            )
        )

        # Create the data exporter object
        exporter = du.DataExporter(data_importer.agg_data_df, export_data_full_file_name)

        # Export data
        exporter.export()

        # Clean up importer and exporter values
        # data_importer.reset()
        data_importer.reset()

        # config.reset()
        config.reset()

        del exporter

        # Open the generated file
        os.startfile(export_data_full_file_name)

        # Raise the Start Screen
        application.show_screen(screen_start)

        progress_bar_upload.widget_object['value'] = 0

        # Update Application
        application.update_idletasks()

    # Create Upload Button
    button_upload = gb.WidgetBuilder(
        child_container_action_buttons,
        tk.Button,
        text="Upload Data",
        command=lambda: upload()
    )

    button_upload.set_placement_settings(
        padx=5
    )

    child_container_loading_status.new_build_row(
        button_upload,
        button_download
    )


def build_screen_config_file_builder() -> None:
    config_file_builder_gui = ConfigFileBuilderGUI(application, screen_start)

    screen_config_file_builder.build_title_label(
        text="Test Datasheet Classes",
        font=(
            'arial',
            12,
            'bold'
        )
    )

    config_file_builder_gui.build_gui(screen_config_file_builder)

    screen_config_file_builder.build_back_button(screen_start, config_file_builder_gui.refresh)


def build_screens() -> None:
    """
    Build all screens
    :return: None
    """
    new_build_screen_start()
    new_build_screen_data_agg_config_form()
    build_screen_data_agg_input_confirmation()
    build_screen_data_import()
    build_screen_config_file_builder()
    build_screen_help()


########################################################################################################################
#                                                   MAIN FUNCTION                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
build_screens()

if __name__ == "__main__":
    application.initialize()


########################################################################################################################
#                                                       END FILE                                                       #
########################################################################################################################
