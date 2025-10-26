"""
This file contains main window script.
"""

import customtkinter as ctk

from app.frontend.buttons import ButtonsCreator as ButtonsCreator
from app.frontend.icons import IconsHolder as IconsHolder
from app.frontend.frames import LeftFrame, RightFrame
from app.frontend.views import CalendarView, NotificationsView, NotesView, GradesView, AverageView, SettingsView


class GridMaker:
    """
    Class is responsible for creating grid for main window.
    """

    def __init__(self, parent: ctk.CTk, rows: int, columns: int) -> None:
        self.parent: ctk.CTk = parent
        self.create_grid(rows, columns)

    def create_grid(self, rows: int, columns: int) -> None:
        """
        Method creates mesh for main application window.
        :param rows: number of grid rows.
        :param columns: numer of column rows.
        :return: Nothing, only creates mesh.
        """
        [self.parent.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(rows)]
        [self.parent.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(columns)]


class LabelsCreator:
    """
    Class is responsible for storing created labels for GUI.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        self.parent: ctk.CTk = parent
        self.create_labels()

    def create_labels(self) -> None:
        """
        Method creates labels for GUI.
        :return: Nothing, only creates labels.
        """
        label_one: ctk.CTkLabel = ctk.CTkLabel(self.parent, text="Student Planner", font=("Roboto", 24))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class AppGUI(ctk.CTk):
    """
    Main GUI class.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("SOSA")
        self.geometry("960x540")
        self.minsize(960, 540)

        self.grid_maker: GridMaker = GridMaker(self, rows=9, columns=24)
        self.icons: IconsHolder = IconsHolder()
        self.left_frame: LeftFrame = LeftFrame(self, color="#444444")
        self.right_frame: RightFrame = RightFrame(self, color="#242424")

        self.views: dict[str, ctk.CTkFrame] = {
            "calendar": CalendarView(self.right_frame.frame),
            "notifications": NotificationsView(self.right_frame.frame),
            "notes": NotesView(self.right_frame.frame),
            "grades": GradesView(self.right_frame.frame),
            "average": AverageView(self.right_frame.frame),
            "settings": SettingsView(self.right_frame.frame),
        }

        self.buttons: ButtonsCreator = ButtonsCreator(self.left_frame.frame, self.icons, self.views, self)
        self.labels: LabelsCreator = LabelsCreator(self.left_frame.frame)

        self.current_view: None | ctk.CTkFrame = None
        self.show_view(self.views["calendar"])

    def show_view(self, view: ctk.CTkFrame):
        if self.current_view:
            self.current_view.pack_forget()

        self.current_view = view
        self.current_view.pack(expand=True, fill="both")
