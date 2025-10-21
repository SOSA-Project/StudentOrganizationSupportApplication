"""
This file contains main window script
"""

import customtkinter as ctk


class GridMaker:
    def __init__(self, parent, rows, columns):
        self.parent = parent
        self.create_grid(rows, columns)

    def create_grid(self, rows, columns):
        [self.parent.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(rows)]
        [self.parent.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(columns)]


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
        self.btn_frame = None
        self.create_frames()

    def create_frames(self):
        self.btn_frame = ctk.CTkFrame(self.parent, fg_color="#444444", corner_radius=10)
        self.btn_frame.grid(row=0, rowspan=15, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        for i in range(15):
            self.btn_frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.btn_frame.grid_columnconfigure(j, weight=1)


class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SOSA")
        self.geometry("960x540")
        self.minsize(960, 540)

        self.grid_maker = GridMaker(self, rows=36, columns=64)
        self.frames = FramesCreator(self)
        self.buttons = ButtonsCreator(self.frames.btn_frame)
        self.labels = LabelsCreator(self.frames.btn_frame)
