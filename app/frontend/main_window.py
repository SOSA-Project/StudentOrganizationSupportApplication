"""
This file contains main window script
"""
from PIL import Image

import customtkinter as ctk


class GridMaker:
    def __init__(self, parent, rows: int, columns: int) -> None:
        self.parent = parent
        self.create_grid(rows, columns)

    def create_grid(self, rows: int, columns: int) -> None:
        [self.parent.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(rows)]
        [self.parent.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(columns)]


class IconsHolder:
    def __init__(self):
        self.calendar_icon = ctk.CTkImage(light_image=Image.open("./app/assets/calendar.png"),
                                          dark_image=Image.open("./app/assets/calendar.png"), size=(20, 20))
        self.notification_icon = ctk.CTkImage(light_image=Image.open("./app/assets/bell.png"),
                                              dark_image=Image.open("./app/assets/bell.png"), size=(20, 20))
        self.notes_icon = ctk.CTkImage(light_image=Image.open("./app/assets/notes.png"),
                                       dark_image=Image.open("./app/assets/notes.png"), size=(20, 20))
        self.grades_icon = ctk.CTkImage(light_image=Image.open("./app/assets/grades.png"),
                                        dark_image=Image.open("./app/assets/grades.png"), size=(20, 20))
        self.average_icon = ctk.CTkImage(light_image=Image.open("./app/assets/chart.png"),
                                         dark_image=Image.open("./app/assets/chart.png"), size=(20, 20))
        self.settings_icon = ctk.CTkImage(light_image=Image.open("./app/assets/settings.png"),
                                          dark_image=Image.open("./app/assets/settings.png"), size=(20, 20))


class ButtonsCreator:
    def __init__(self, parent, icons) -> None:
        self.parent = parent
        self.icons = icons
        self.create_buttons()

    def create_buttons(self):
        btn_calendar = ctk.CTkButton(self.parent, text="Calendar", font=("Roboto", 18), image=self.icons.calendar_icon)
        btn_calendar.grid(row=6, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_notifications = ctk.CTkButton(self.parent, text="Notifications", font=("Roboto", 18),
                                          image=self.icons.notification_icon)
        btn_notifications.grid(row=9, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_notes = ctk.CTkButton(self.parent, text="Notes", font=("Roboto", 18), image=self.icons.notes_icon)
        btn_notes.grid(row=12, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_grades = ctk.CTkButton(self.parent, text="Grades", font=("Roboto", 18), image=self.icons.grades_icon)
        btn_grades.grid(row=15, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_average = ctk.CTkButton(self.parent, text="Average", font=("Roboto", 18), image=self.icons.average_icon)
        btn_average.grid(row=18, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_settings = ctk.CTkButton(self.parent, text="Settings", font=("Roboto", 18), image=self.icons.settings_icon)
        btn_settings.grid(row=29, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)


class LabelsCreator:
    def __init__(self, parent):
        self.parent = parent
        self.create_labels()

    def create_labels(self):
        lab1 = ctk.CTkLabel(self.parent, text="Student Planner", font=("Roboto", 24))
        lab1.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class FramesCreator:
    def __init__(self, parent):
        self.parent = parent
        self.left_frame = None
        self.right_frame = None
        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        self.left_frame = ctk.CTkFrame(self.parent, fg_color="#444444", corner_radius=10)
        self.left_frame.grid(row=0, rowspan=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        [self.left_frame.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.left_frame.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(1)]

    def create_right_frame(self):
        self.right_frame = ctk.CTkFrame(self.parent, fg_color="#444444", corner_radius=10)
        self.right_frame.grid(row=0, rowspan=9, column=2, columnspan=22, sticky="nsew", padx=5, pady=5)


class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SOSA")
        self.geometry("960x540")
        self.minsize(960, 540)

        self.grid_maker = GridMaker(self, rows=9, columns=24)
        self.icons = IconsHolder()
        self.frames = FramesCreator(self)
        self.buttons = ButtonsCreator(self.frames.left_frame, self.icons)
        self.labels = LabelsCreator(self.frames.left_frame)
