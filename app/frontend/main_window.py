"""
This file contains main window script
"""

import customtkinter as ctk


class GridMaker:
    def __init__(self, parent, rows: int, columns: int) -> None:
        self.parent = parent
        self.create_grid(rows, columns)

    def create_grid(self, rows: int, columns: int) -> None:
        [self.parent.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(rows)]
        [self.parent.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(columns)]


class ButtonsCreator:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.create_buttons()

    def create_buttons(self):
        btn_calendar = ctk.CTkButton(self.parent, text="Calendar")
        btn_calendar.grid(row=6, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_notifications = ctk.CTkButton(self.parent, text="Notifications")
        btn_notifications.grid(row=9, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_notes = ctk.CTkButton(self.parent, text="Notes")
        btn_notes.grid(row=12, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_grades = ctk.CTkButton(self.parent, text="Grades")
        btn_grades.grid(row=15, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_average = ctk.CTkButton(self.parent, text="Average")
        btn_average.grid(row=18, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_settings = ctk.CTkButton(self.parent, text="Settings")
        btn_settings.grid(row=29, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)


class LabelsCreator:
    def __init__(self, parent):
        self.parent = parent
        self.create_labels()

    def create_labels(self):
        lab1 = ctk.CTkLabel(self.parent, text="Student Planner", font=("Arial", 16))
        lab1.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class FramesCreator:
    def __init__(self, parent):
        self.parent = parent
        self.btn_frame = None
        self.create_left_frame()

    def create_left_frame(self):
        self.btn_frame = ctk.CTkFrame(self.parent, fg_color="#444444", corner_radius=10)
        self.btn_frame.grid(row=0, rowspan=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        [self.btn_frame.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.btn_frame.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(1)]


class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SOSA")
        self.geometry("960x540")
        self.minsize(960, 540)

        self.grid_maker = GridMaker(self, rows=9, columns=24)
        self.frames = FramesCreator(self)
        self.buttons = ButtonsCreator(self.frames.btn_frame)
        self.labels = LabelsCreator(self.frames.btn_frame)
