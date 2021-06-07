# IMPORTS:

from tkinter import filedialog, messagebox as mb

import shutil

import os

import easygui


def get_user_str_input(prompt_str):
    user_str_input = input(prompt_str + ": ")

    return user_str_input


def get_directory_path():
    directory = filedialog.askdirectory()

    return directory


def create_directory_path():
    # Get folder path

    new_folder_path = get_directory_path()

    # Get new folder name from user

    new_folder_name = get_user_str_input("Enter name of new folder")

    # Build full new folder path

    full_new_folder_path = os.path.join(new_folder_path, new_folder_name)

    # Make the output directory
    os.mkdir(full_new_folder_path)

    mb.showinfo('confirmation', 'Folder created!')

    # Return the full folder path

    return full_new_folder_path


def get_file_path():
    file_path = easygui.fileopenbox()

    return file_path


class DAggUserInterface:

    def __init__(self):
        self.username = None

        self.config_file_path = None

        self.input_directory_path = None

        self.output_directory_path = None

    def get_username(self):
        self.username = get_user_str_input("Enter username")

    def get_config_file_path(self):
        self.config_file_path = get_file_path()

    def get_input_directory_path(self):
        self.output_directory_path = get_directory_path()

    def get_output_directory_path(self):
        self.output_directory_path = get_directory_path()


def initiate_gui():
    pass
