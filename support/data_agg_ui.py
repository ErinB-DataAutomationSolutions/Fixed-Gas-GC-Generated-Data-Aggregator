# IMPORTS:

from tkinter import *
from tkinter import filedialog, messagebox as mb
import shutil
import os
import easygui
# from PIL import Image, ImageTk


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
        self.input_directory_path = get_directory_path()

    def get_output_directory_path(self):
        self.output_directory_path = get_directory_path()

    def create_config_file(self):
        pass

    def aggregate_data(self):
        pass

    def export_data(self):
        pass


def initiate_gui():

    ui = DAggUserInterface()

    root = Tk()
    # creating a canvas to insert image
    canv = Canvas(root, width=500, height=420, bg='white')
    canv.grid(row=0, column=2)
    # img = ImageTk.PhotoImage(Image.open("D:\\learn\\TechVidvan\\TechVidvan.png"))
    canv.create_image(20, 20, anchor=NW)
    # creating label and buttons to perform operations
    Label(root, text="Fixed Gas GC Data Aggregator", font=("Helvetica", 16), fg="blue").grid(row=5, column=2)
    Button(root, text="Open config file", command=ui.get_config_file_path).grid(row=15, column=2)
    Button(root, text="Get Username", command=ui.get_username).grid(row=25, column=2)
    Button(root, text="Get Input directory Path", command=ui.get_input_directory_path).grid(row=35, column=2)
    Button(root, text="Get Output directory path", command=ui.get_output_directory_path).grid(row=45, column=2)
    Button(root, text="Create Config File", command=ui.create_config_file).grid(row=55, column=2)
    Button(root, text="Aggregate Data", command=ui.aggregate_data).grid(row=65, column=2)
    Button(root, text="Export Data", command=ui.aggregate_data).grid(row=75, column=2)

    root.mainloop()

    return ui.config_file_path, ui.username, ui.input_directory_path, ui.output_directory_path
