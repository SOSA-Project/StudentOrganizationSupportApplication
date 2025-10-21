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
            self.parent.grid_rowconfigure(i, weight=1)
        for j in range(self.columns):
            self.parent.grid_columnconfigure(j, weight=1)


class ButtonsCreator:
    def __init__(self, parent):
        self.parent = parent
        self.create_buttons()

    def create_buttons(self):
        btn1 = ctk.CTkButton(self.parent, text="Przycisk 1")
        btn1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        btn2 = ctk.CTkButton(self.parent, text="Przycisk 2")
        btn2.grid(row=3, column=5, columnspan=2, rowspan=2, sticky="nsew", padx=5, pady=5)

        btn3 = ctk.CTkButton(self.parent, text="Przycisk 3")
        btn3.grid(row=9, column=9, sticky="nsew", padx=5, pady=5)


class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SOSA")
        self.geometry("800x600")

        self.grid_maker = GridMaker(self, rows=10, columns=15)
        self.buttons = ButtonsCreator(self)
