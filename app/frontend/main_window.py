"""
This file contains main window script
"""

import customtkinter as ctk


class GridMaker:
    def __init__(self, parent, rows, columns):
        self.parent = parent
        self.rows = rows
        self.columns = columns
        self.create_grid()

    def create_grid(self):
        for i in range(self.rows):
            self.parent.grid_rowconfigure(i, weight=1, uniform="rowcol")
        for j in range(self.columns):
            self.parent.grid_columnconfigure(j, weight=1, uniform="rowcol")


class ButtonsCreator:
    def __init__(self, parent):
        self.parent = parent
        self.create_buttons()

    def create_buttons(self):
        btn_calendar = ctk.CTkButton(self.parent, text="Calendar")
        btn_calendar.grid(row=2, rowspan=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        btn_notifications = ctk.CTkButton(self.parent, text="Notifications")
        btn_notifications.grid(row=5, rowspan=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        btn_notes = ctk.CTkButton(self.parent, text="Notes")
        btn_notes.grid(row=8, rowspan=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        btn_grades = ctk.CTkButton(self.parent, text="Grades")
        btn_grades.grid(row=11, rowspan=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)


class LabelsCreator:
    def __init__(self, parent):
        self.parent = parent
        self.create_labels()

    def create_labels(self):
        lab1 = ctk.CTkLabel(self.parent, text="Student Planner", font=("Arial", 16))
        lab1.grid(row=0, rowspan=2, column=0, columnspan=2, padx=5, pady=5)


class FramesCreator:
    def __init__(self, parent):
        self.parent = parent
        self.create_frames()

    def create_frames(self):
        pass


class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SOSA")
        self.geometry("960x540")
        self.minsize(960, 540)

        self.grid_maker = GridMaker(self, rows=36, columns=64)
        self.buttons = ButtonsCreator(self)
        self.labels = LabelsCreator(self)
        self.frames = FramesCreator(self)
