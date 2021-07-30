########################################################################################################################
#                                               FILE DETAILS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
# PROGRAM:  Fixed Gas Data Aggregator                                                                                  #
# Author:   Arin Bryson                                                                                                #
########################################################################################################################

########################################################################################################################
#                                                   Imports                                                            #
# -------------------------------------------------------------------------------------------------------------------- #

import tkinter as tk
import getpass
from typing import Callable
import support.gui_builder as ngb
from tkinter import filedialog as fd
from tkinter import messagebox
import glob


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


def stubbing_func(stub_message: str) -> None:
    print(stub_message)


def get_input_data_file_paths(input_data_dir, input_data_file_name) -> list:
    return glob.glob(f'./{input_data_dir}/**/{input_data_file_name}', recursive=True)


########################################################################################################################
#                                                       CLASSES                                                        #
# -------------------------------------------------------------------------------------------------------------------- #

class InputFormUI:

    def __init__(self):
        # Set the default username
        self.default_user_name = getpass.getuser()

        # Set error bool values
        self.config_file_path_input_error = False
        self.input_dir_input_error = False

        # Set placeholders
        self.username_str = None
        self.config_file_path_str = None
        self.input_dir_path_str = None
        self.output_dir_path_str = None

    def set_username(self, entry: "tk.Entry"):
        username_str = entry.get()

        # If input string is empty:
        #   - Set username to default username
        #   - return
        if username_str == "":
            self.username_str = self.default_user_name
            return

        # ELSE:
        #   - Set username as input string
        #   - return
        self.username_str = username_str

    def set_config_file_path(self, entry: "tk.Entry"):
        config_file_path_str = entry.get()

        # IF the config file path input string is empty:
        #   -
        if config_file_path_str == "":
            self.config_file_path_input_error = True
            return

        # ELSE
        self.config_file_path_str = config_file_path_str

    def set_input_dir_path(self, entry: "tk.Entry"):
        input_dir_path_str = entry.get()

        # IF the input dir entry is missing, raise an error!
        if input_dir_path_str == "":
            self.input_dir_input_error = True
            return

        self.input_dir_path_str = input_dir_path_str

    def set_output_dir_path(self, entry: "tk.Entry"):
        output_dir_path = entry.get()

        if output_dir_path == "":
            self.output_dir_path_str = f"C:\\Users\\{self.default_user_name}\\Documents\\"
            return

        self.output_dir_path_str = output_dir_path


########################################################################################################################
#                                                  BUILD GUI                                                           #
# -------------------------------------------------------------------------------------------------------------------- #

# Create an instance of the UI
input_form_ui = InputFormUI()

# Create an instance of the application
application = ngb.Application()

global_string_var = tk.StringVar()
global_string_var.set("")

global_int_var = tk.IntVar()

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  Create screens                                                      #
# -------------------------------------------------------------------------------------------------------------------- #

# Start Screen
screen_start = ngb.ScreenContainer(application, True)

# Data Aggregator Config Form Screen
screen_dagg_config_form = ngb.ScreenContainer(application)

# Data Aggregator Confirmation Screen
screen_dagg_input_confirmation = ngb.ScreenContainer(application)

# Data Aggregator Importing Loading Screen
screen_data_import = ngb.ScreenContainer(application)

#  Config File Builder Screen
screen_config_file_builder = ngb.ScreenContainer(application)

# Create Help Screen
screen_help = ngb.ScreenContainer(application)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                    Build Screens                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
def build_screen_start():
    """
    Build out the Start Screen
    :return:
    """
    # Build title label
    screen_start.build_title_label(
        text="Fixed Gas GC Data Aggregator",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    # Create a Start Menu child container
    child_container_start_menu = ngb.OldChildContainer(
        screen_start,
        orient=tk.VERTICAL
    )

    child_container_start_menu.set_pack_options(
        pady=10
    )

    # Add button leading to Data Aggregator Form screen
    child_container_start_menu.build_new_screen_button(
        screen_dagg_config_form,
        text="Aggregate Data"
    )

    # Add button leading to Config File Builder
    child_container_start_menu.build_new_screen_button(
        screen_config_file_builder,
        text="Build Config File"
    )

    # Add button leading to Help screen
    child_container_start_menu.build_new_screen_button(
        screen_help,
        text="Help"
    )

    button_quit = tk.Button(
        child_container_start_menu,
        text="Quit",
        command=lambda: application.close_application()
    )

    child_container_start_menu.add_elements(button_quit)


def build_screen_help():
    screen_help.build_title_label(
        text="Help",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    child_container_help_messages = ngb.ChildContainer(
        screen_help
    )

    # Create a child container for the help messages
    child_container_help_messages.set_pack_options(fill=tk.X)
    child_container_help_messages.config_column(0, weight=1)

    # LabelFrame for Data Aggregator help section
    labelframe_data_aggregator = ngb.WidgetBuilder(
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

    labelframe_config_file_builder = ngb.WidgetBuilder(
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


def build_screen_dagg_config_form():
    # Build Title label
    screen_dagg_config_form.build_title_label(
        text="Data Aggregator: Configuration Settings",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    screen_dagg_config_form.columnconfigure(0, weight=1)
    screen_dagg_config_form.columnconfigure(1, weight=3)
    screen_dagg_config_form.columnconfigure(2, weight=1)

    # Create Child Container for Output Directory form row
    child_container_output_dir_row = ngb.OldChildContainer(screen_dagg_config_form)
    # Configure columns
    child_container_output_dir_row.columnconfigure(0, weight=1)
    child_container_output_dir_row.columnconfigure(1, weight=3)
    child_container_output_dir_row.columnconfigure(2, weight=1)

    child_container_output_dir_row.set_pack_options(fill=tk.X)

    label_output_dir = tk.Label(
        child_container_output_dir_row,
        text="Output Dir: "
    )

    entry_output_dir = tk.Entry(
        child_container_output_dir_row
    )

    entry_output_dir.pack(fill=tk.X)

    button_output_dir_row = tk.Button(
        child_container_output_dir_row,
        text="Browse",
        command=lambda: print("Browse directories")
    )

    child_container_output_dir_row.add_elements(
        label_output_dir,
        entry_output_dir,
        button_output_dir_row
    )

    # Create child container for the Submit and Cancel buttons
    child_container_end_form = ngb.OldChildContainer(screen_dagg_config_form)
    child_container_end_form.set_pack_options(
        side=tk.RIGHT
    )

    button_clear = tk.Button(
        child_container_end_form,
        text="Clear"
    )

    button_clear.pack(
        padx=10,
        pady=10
    )

    button_submit = tk.Button(
        child_container_end_form,
        text="Submit"
    )

    button_submit.pack(
        padx=10,
        pady=10
    )

    child_container_end_form.add_elements(
        button_clear,
        button_submit
    )

    screen_dagg_config_form.build_back_button(screen_start)


def new_build_screen_dagg_config_form():
    # Build the Screen Title
    screen_dagg_config_form.build_title_label(
        text="Data Aggregator: Configuration Settings",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    # CHILD CONTAINER 1: FORM ENTRY
    # Create a child container for the Form entry
    child_container_form_input = ngb.ChildContainer(screen_dagg_config_form)
    child_container_form_input.set_pack_options(fill=tk.X)

    # Column configure
    child_container_form_input.config_column(1, weight=3)

    # ROW 0: Username
    # Label
    label_username = ngb.WidgetBuilder(
        child_container_form_input,
        tk.Label,
        text="Username:"
    )

    label_username.set_placement_settings(sticky="e")

    # Entry
    entry_username = ngb.WidgetBuilder(
        child_container_form_input,
        tk.Entry
    )

    entry_username.set_placement_settings(sticky="ew")

    # Build row 1
    child_container_form_input.new_build_row(
        label_username,
        entry_username
    )

    # ROW 2: CONFIG FILE
    # Label
    label_config_file = ngb.WidgetBuilder(
        child_container_form_input,
        tk.Label,
        text="Config File*:",
        fg="red"
    )

    label_config_file.set_placement_settings(sticky="e")

    # Entry
    entry_config_file = ngb.WidgetBuilder(
        child_container_form_input,
        tk.Entry
    )

    entry_config_file.set_placement_settings(sticky="ew")

    # Button
    button_config_file = ngb.WidgetBuilder(
        child_container_form_input,
        tk.Button,
        text="Browse",
        command=lambda: set_entry_value(entry_config_file.widget_object, get_file_path(), 0, True)
    )

    # Build row
    child_container_form_input.new_build_row(
        label_config_file,
        entry_config_file,
        button_config_file
    )

    # ROW 3: INPUT DIRECTORY
    # Label
    label_input_directory = ngb.WidgetBuilder(
        child_container_form_input,
        tk.Label,
        text="Input Folder*:",
        fg="red"
    )

    label_input_directory.set_placement_settings(sticky="e")

    # Entry
    entry_input_directory = ngb.WidgetBuilder(
        child_container_form_input,
        tk.Entry
    )

    entry_input_directory.set_placement_settings(sticky="ew")

    # Button
    button_input_directory = ngb.WidgetBuilder(
        child_container_form_input,
        tk.Button,
        text="Browse",
        command=lambda: set_entry_value(entry_input_directory.widget_object, get_dir_path(), 0, True)
    )

    # Build Row:
    child_container_form_input.new_build_row(
        label_input_directory,
        entry_input_directory,
        button_input_directory
    )

    # CHILD CONTAINER 2: END FORM
    child_container_form_end = ngb.ChildContainer(
        screen_dagg_config_form
    )

    child_container_form_end.set_pack_options(
        side=tk.RIGHT,
        pady=10
    )

    # Button: Clear
    def clear():
        # Clear stored UI values:
        input_form_ui.username_str = None
        input_form_ui.config_file_path_str = None
        input_form_ui.input_dir_path_str = None

        # Clear each entry
        entry_username.widget_object.delete(0, tk.END)
        entry_config_file.widget_object.delete(0, tk.END)
        entry_input_directory.widget_object.delete(0, tk.END)

        print("Form Cleared!")

    button_end_form_clear = ngb.WidgetBuilder(
        child_container_form_end,
        tk.Button,
        text="Clear",
        command=lambda: clear()
    )

    button_end_form_clear.set_placement_settings(padx=5)

    # Button: Submit
    def submit():
        # Reset UI error values:
        input_form_ui.config_file_path_input_error = False
        input_form_ui.input_dir_input_error = False

        # Set Input Form UI Variables
        input_form_ui.set_username(entry_username.widget_object)
        input_form_ui.set_config_file_path(entry_config_file.widget_object)
        input_form_ui.set_input_dir_path(entry_input_directory.widget_object)

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
            f"\nUsername:\t{input_form_ui.username_str}"
            f"\nConfig File:\t{input_form_ui.config_file_path_str}"
            f"\nInput Folder:\t{input_form_ui.input_dir_path_str}"
        )

        application.update_idletasks()

        # Confirm Form Submitted
        print("Form submitted!")

        # Go to the info confirmation screen
        application.show_screen(screen_dagg_input_confirmation)

    button_end_form_submit = ngb.WidgetBuilder(
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
    screen_dagg_config_form.build_back_button(screen_start)


def build_screen_dagg_input_confirmation():
    screen_dagg_input_confirmation.build_title_label(
        text="Input Confirmation",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    child_container_message = ngb.ChildContainer(
        screen_dagg_input_confirmation
    )

    child_container_message.set_pack_options(fill=tk.X)

    text_instructions = "Please review your configuration settings below."

    label_instructions = ngb.WidgetBuilder(
        child_container_message,
        tk.Label,
        text=text_instructions,
        # justify=tk.LEFT
    )

    child_container_message.new_build_row(
        label_instructions
    )

    # Build the Label form input values widget
    label_form_input_values = ngb.WidgetBuilder(
        child_container_message,
        tk.Label,
        # text=text_instructions + text_config_settings
        textvariable=global_string_var,
        justify=tk.LEFT
    )

    child_container_message.new_build_row(
        label_form_input_values
    )

    child_container_confirm_button = ngb.ChildContainer(
        screen_dagg_input_confirmation
    )

    child_container_confirm_button.set_pack_options(
        side=tk.RIGHT,
        padx=5
    )

    def confirm():
        # Set global int var to total number of files
        # NOTE: The below value is a dummy value
        global_int_var.set(10)
        global_string_var.set(f"0 out of {global_int_var.get()} files uploaded...")

        application.update_idletasks()

        # Show the Data Import screen
        application.show_screen(screen_data_import)

    button_confirm = ngb.WidgetBuilder(
        child_container_confirm_button,
        tk.Button,
        text="Confirm",
        command=lambda: confirm()
    )

    child_container_confirm_button.new_build_row(
        button_confirm
    )

    screen_dagg_input_confirmation.build_back_button(screen_dagg_config_form)


def build_screen_data_import():
    # Build Title Label
    screen_data_import.build_title_label(
        text="Importing Data",
        font=(
            'arial',
            15,
            'bold'
        )
    )

    child_container_loading_status = ngb.ChildContainer(
        screen_data_import
    )

    label_loading_status = ngb.WidgetBuilder(
        child_container_loading_status,
        tk.Label,
        textvariable=global_string_var
    )

    child_container_loading_status.new_build_row(
        label_loading_status
    )


def build_screen_config_file_builder():
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
    child_container_coming_soon = ngb.OldChildContainer(screen_config_file_builder)

    label_coming_soon = tk.Label(
        child_container_coming_soon,
        text="Coming soon!",
        fg="red"
    )

    child_container_coming_soon.add_elements(label_coming_soon)

    # Build Back button
    screen_config_file_builder.build_back_button(screen_start)


def build_screens():
    """
    Build all screens
    :return: None
    """
    build_screen_start()
    # build_screen_dagg_config_form()
    new_build_screen_dagg_config_form()
    build_screen_dagg_input_confirmation()
    build_screen_data_import()
    build_screen_config_file_builder()
    build_screen_help()


########################################################################################################################
#                                                   MAIN FUNCTION                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
def main_0():
    build_screens()
    application.initialize()


########################################################################################################################
#                                                   RUN APPLICATION                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    main_0()

########################################################################################################################
#                                                       END FILE                                                       #
########################################################################################################################
