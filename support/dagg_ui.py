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
        text="Data Aggregator Help",
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
        text="Config File Builder Help",
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
    # Build Title label
    screen_config_file_builder.build_title_label(
        text="Config File Builder",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    # Create "Coming Soon" child container
    child_container_coming_soon = gb.OldChildContainer(screen_config_file_builder)

    label_coming_soon = tk.Label(
        child_container_coming_soon,
        text="Coming soon!",
        fg="red"
    )

    child_container_coming_soon.add_elements(label_coming_soon)

    # Build Back button
    screen_config_file_builder.build_back_button(screen_start)


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
