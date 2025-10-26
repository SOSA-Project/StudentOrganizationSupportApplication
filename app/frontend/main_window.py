"""
This file contains main window script.
"""

import customtkinter as ctk

from app.frontend.buttons import ButtonsCreator as ButtonsCreator
from app.frontend.icons import IconsHolder as IconsHolder
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


class FramesCreator:
    """
    Class is responsible for storing created frames for GUI.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        self.parent: ctk.CTk = parent
        self.left_frame: ctk.CTkFrame | None = None
        self.right_frame: ctk.CTkFrame | None = None
        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self) -> None:
        """
        Method creates left frame for GUI.
        :return: Nothing, only create left frame.
        """
        self.left_frame = ctk.CTkFrame(self.parent, fg_color="#444444", corner_radius=10)
        self.left_frame.grid(row=0, rowspan=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        [self.left_frame.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.left_frame.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(1)]

    def create_right_frame(self) -> None:
        """
        Method creates right frame for GUI.
        :return: Nothing, only create right frame.
        """
        self.right_frame = ctk.CTkFrame(self.parent, fg_color="#444444", corner_radius=10)
        self.right_frame.grid(row=0, rowspan=9, column=2, columnspan=22, sticky="nsew", padx=5, pady=5)


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
        self.frames: FramesCreator = FramesCreator(self)

        self.views = {
            "calendar": CalendarView(self.frames.right_frame),
            "notifications": NotificationsView(self.frames.right_frame),
            "notes": NotesView(self.frames.right_frame),
            "grades": GradesView(self.frames.right_frame),
            "average": AverageView(self.frames.right_frame),
            "settings": SettingsView(self.frames.right_frame),
        }

        self.buttons: ButtonsCreator = ButtonsCreator(self.frames.left_frame, self.icons, self.views, self)
        self.labels: LabelsCreator = LabelsCreator(self.frames.left_frame)

        self.current_view = None
        self.show_view(self.views["calendar"])

    def show_view(self, view):
        if self.current_view:
            self.current_view.pack_forget()

        self.current_view = view
        self.current_view.pack(expand=True, fill="both")
