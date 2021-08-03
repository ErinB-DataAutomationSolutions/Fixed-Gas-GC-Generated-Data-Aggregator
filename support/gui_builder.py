########################################################################################################################
# Screen switching method based on example:
#   https://pythonprogramming.net/change-show-new-frame-tkinter/
#
# ScreenContainer and ChildContainer Classes based on example:
#   https://www.studytonight.com/tkinter/python-tkinter-panedwindow-widget
########################################################################################################################

import tkinter as tk
from typing import Any


class WidgetBuilder:
    """
This class builds widgets based on type, and stores placement settings.
    """
    def __init__(self, master: "ChildContainer", widget_type, **options: [str, Any]):
        # Assign widget type and master
        self.master = master
        self.widget_type = widget_type
        self.handler = master.handler

        # Create widget
        self.widget_object = widget_type(master)

        # Add all options ot the widget object
        for option in options:
            self.widget_object[option] = options[option]

        # Placeholders:
        self.placement_settings = {}

    def set_placement_settings(self, **placement_settings: [str, Any]) -> None:
        """
        Set the placement settings into the placement settings dictionary
        :param placement_settings: Placement Settings Dictionary
        :return: None
        """
        for placement_setting in placement_settings:
            self.placement_settings[placement_setting] = placement_settings[placement_setting]

    def set_next_screen_command(self, next_screen: "ScreenContainer") -> None:
        """

        :param next_screen:
        :return: None
        """
        if "command" in self.placement_settings.keys():
            print("command already set")
            return

        self.placement_settings["command"] = self.handler.show_screen(next_screen)


class ChildContainer(tk.Frame):
    # Track number of child containers that have been created
    counter = 0

    def __init__(self, master, **options):
        super().__init__(master, cnf=options)

        self.master = master

        # Assign Handler
        self.handler = self.master.handler

        # Assign ID number, increase class counter by 1
        self.id = ChildContainer.counter
        ChildContainer.counter += 1

        # Add the child container to its master
        self.master.add_child_container(self)

        # Placeholders
        self.pack_options = {}
        self.next_row_num = 0

    def new_build_row(self, *widget_builders: "WidgetBuilder"):

        for column, widget_builder in enumerate(widget_builders):
            widget_builder.placement_settings["row"] = self.next_row_num
            widget_builder.placement_settings["column"] = column

            # widget_object = widget_builder.create_element()
            widget_object = widget_builder.widget_object

            widget_object.grid(cnf=widget_builder.placement_settings)

        self.next_row_num += 1

    def build_row(self, *widgets) -> None:
        """
        Build a row in the child container frame
        :param widgets: Widget objects
        :return: None
        """
        for column, widget in enumerate(widgets):
            widget.grid(
                row=self.next_row_num,
                column=column
            )

        # FINALLY, increase the next_row_num by 1
        self.next_row_num += 1

    def set_pack_options(self, **options):
        for option in options:
            self.pack_options[option] = options[option]

    def config_column(self, column_num: int, **options):
        self.columnconfigure(column_num, cnf=options)
        self.master.columnconfigure(column_num, cnf=options)


class OldChildContainer(tk.PanedWindow):
    # Track number of child containers that have been created
    counter = 0

    def __init__(self, master, **options):
        super().__init__(master, cnf=options)

        self.master = master

        # Assign Handler
        self.handler = master.handler

        # Assign ID number, increase counter by 1
        self.id = OldChildContainer.counter
        OldChildContainer.counter += 1

        self.master.add_child_container(self)

        # Placeholders
        self.pack_options = {}

    def add_elements(self, *elements):
        """Add element to the child container"""
        for element in elements:
            self.add(element)

    def build_new_screen_button(self, screen: "ScreenContainer", **options):
        """Add a new screen button to the child container"""
        new_screen_button = tk.Button(
            self,
            cnf=options
        )

        new_screen_button["command"] = lambda: self.handler.show_screen(screen)

        self.add(new_screen_button)

    def set_pack_options(self, **options):
        for option in options:
            self.pack_options[option] = options[option]


class ScreenContainer(tk.Frame):
    # Track number of screens that have been created
    screen_object_counter = 0

    def __init__(self, handler: "Application" or "OldApplication", start_screen=False, **options):
        # super().__init__(handler.application_container, cnf=options)
        super().__init__(handler, cnf=options)

        # Assign Screen ID, increase screen counter by 1
        self.id = ScreenContainer.screen_object_counter
        ScreenContainer.screen_object_counter += 1

        # Assign the handler
        self.handler = handler
        # self.handler = master.window_container

        if start_screen:
            self.handler.add_start_screen(self)
        else:
            self.handler.add_screen(self)

        # Create placeholders for Child Container Dict, Title Label, Back Button, and Next Button
        self.child_containers = {}

        self.title_label = None
        self.back_button = None
        self.next_button = None

    def build_title_label(self, **options):
        self.title_label = tk.Label(
            self,
            cnf=options
        )

    def add_child_container(self, child_container: "ChildContainer"):
        self.child_containers[child_container.id] = child_container

    def remove_child_container(self, child_container: "ChildContainer"):
        self.child_containers.pop(child_container.id)
        print(f"Child Container {child_container.id} removed!")

    def build_back_button(self, parent_screen):
        self.back_button = tk.Button(
            self,
            text="Back",
            command=lambda: self.handler.show_screen(parent_screen)
        )

    def remove_back_button(self):
        if self.back_button:
            self.back_button = None

    def build_next_button(self, next_screen):
        self.next_button = tk.Button(
            self,
            text="Next",
            command=lambda: self.handler.show_screen(next_screen)
        )

    def remove_next_button(self):
        if self.next_button:
            self.next_button = None

    def place_elements(self):
        # Place title label, if exists
        if self.title_label:
            self.title_label.pack(fill=tk.X)

        # Place child containers
        for child_container_id in self.child_containers:
            # Get the child container
            child_container = self.child_containers[child_container_id]

            # Get the pack options
            pack_options = child_container.pack_options

            # Pack the Child Container
            child_container.pack(cnf=pack_options)

        # Place Back Button, if exists
        if self.back_button:
            self.back_button.pack(
                side=tk.LEFT,
                padx=5
            )

        if self.next_button:
            self.next_button.pack(
                side=tk.RIGHT,
                padx=5
            )


class OldApplication(tk.Tk):
    """This class manages the Tkinter application."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(1, weight=1)

        # Create a container
        self.application_container = tk.Frame(self)

        # Configure the application such that it's expandable in all directions
        self.application_container.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # self.application_container.pack(fill=tk.BOTH)

        # self.application_container.columnconfigure(1, weight=1)

        # Configure application container row and column weight
        self.application_container.grid_rowconfigure(0, weight=1)
        self.application_container.grid_columnconfigure(1, weight=1)

        # Place holder for the start screen ID
        self.start_screen_id = None

        # Dictionary that maps a screen label with a screen
        self.screen_dict = {}

    def add_start_screen(self, start_screen: "ScreenContainer"):
        """Add the start screen"""

        # IF a Start Screen ID is already stored, return
        if self.start_screen_id:
            return

        # Store the Start Screen ID for later lookup
        self.start_screen_id = start_screen.id

        # Add teh Start Screen ID and Start Screen object to the Screen Dictionary
        self.screen_dict[self.start_screen_id] = start_screen

    def add_screen(self, screen: "ScreenContainer"):
        self.screen_dict[screen.id] = screen

    def remove_screen(self, screen: "ScreenContainer"):
        self.screen_dict.pop(screen.id)
        print(f"Screen # {screen.id} removed!")

    def show_screen(self, screen: "ScreenContainer"):
        # Show the mapped screen
        print(f"Attempting to raise Screen # {screen.id}")
        self.screen_dict[screen.id].tkraise()

    def initialize(self) -> None:
        """
The Application is initialized in the following steps:
    1)  Each Screen is placed in the application via the GRID function
    2)      Elements are placed in each screen
    3)  The Screen designated as the "Start" screen is raised
    4)  The Application Mainloop function is called
:return: None
        """
        # Set Start Screen to be shown first
        for screen_id in self.screen_dict:

            screen = self.screen_dict[screen_id]

            screen.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

            screen.place_elements()

        # Raise the Start Screen
        self.screen_dict[self.start_screen_id].tkraise()

        # Start Application
        self.mainloop()

    def close_application(self):
        self.destroy()


class Application(tk.Tk):
    """
This class creates, maintains, and runs the application.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Give application column 0 a weight so that it's expandable
        self.columnconfigure(0, weight=1)

        # Place holder for the start screen ID
        self.start_screen_id = None

        # Dictionary that maps a screen label with a screen
        self.screen_dict = {}

    def add_start_screen(self, start_screen: "ScreenContainer") -> None:
        """
Saves the Screen.ID of the desired start screen
:param start_screen: This is the Screen to be raised once the application is initialized
:return: None
        """

        # IF a Start Screen ID is already stored, return
        if self.start_screen_id:
            return

        # Store the Start Screen ID for later lookup
        self.start_screen_id = start_screen.id

        # Add teh Start Screen ID and Start Screen object to the Screen Dictionary
        self.screen_dict[self.start_screen_id] = start_screen

    def add_screen(self, screen: "ScreenContainer") -> None:
        """
Add a ScreenContainer object to the screen dictionary; use ScreenContainer object.id as the key.
:param screen: An object of the ScreenContainer class to be added
:return: None
        """
        self.screen_dict[screen.id] = screen

    def remove_screen(self, screen: "ScreenContainer") -> None:
        """
Remove a ScreenContainer object from the screen dictionary using the ScreenContainer object.id
:param screen: ScreenContainer object
:return: None
        """
        self.screen_dict.pop(screen.id)
        print(f"Screen # {screen.id} removed!")

    def show_screen(self, screen: "ScreenContainer") -> None:
        """
Raise the placed ScreenContainer object
:param screen: ScreenContainer object
:return: None
        """
        # Show the mapped screen
        print(f"Attempting to raise Screen # {screen.id}")
        self.screen_dict[screen.id].tkraise()

    def initialize(self) -> None:
        """
The Application is initialized in the following steps:
    1)  Each Screen is placed in the application via the GRID function
    2)      Elements are placed in each screen
    3)  The Screen designated as the "Start" screen is raised
    4)  The Application Mainloop function is called
:return: None
        """
        # Set Start Screen to be shown first
        for screen_id in self.screen_dict:

            screen = self.screen_dict[screen_id]

            screen.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

            screen.columnconfigure(0, weight=1)

            screen.place_elements()

        # Raise the Start Screen
        self.screen_dict[self.start_screen_id].tkraise()

        # Start Application
        self.mainloop()

    def close_application(self):
        """
Close application window
:return: None
        """
        self.destroy()

# END FILE
