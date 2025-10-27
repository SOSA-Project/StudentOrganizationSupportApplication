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

        # Basic main app window setup
        self.grid_maker: GridMaker = GridMaker(self, rows=9, columns=24)
        self.btn_icons: IconsHolder = IconsHolder()
        self.left_frame: LeftFrame = LeftFrame(self, color="#444444")
        self.right_frame: RightFrame = RightFrame(self, color="#242424")

        # Container for all available views
        self.views: dict[str, ctk.CTkFrame] = {
            "calendar": CalendarView(self.right_frame.frame),
            "notifications": NotificationsView(self.right_frame.frame),
            "notes": NotesView(self.right_frame.frame),
            "grades": GradesView(self.right_frame.frame),
            "average": AverageView(self.right_frame.frame),
            "settings": SettingsView(self.right_frame.frame),
        }

        # Buttons for left gui frame
        self.buttons: ButtonsCreator = ButtonsCreator(self.left_frame.frame, self.btn_icons.icons, self.views, self)
        self.labels: LabelsCreator = LabelsCreator(self.left_frame.frame)

        # Current right frame view
        self.current_view: None | ctk.CTkFrame = None
        self.show_view(self.views["calendar"])

        # Resizable text and images in buttons
        self.flag: str | None = None
        self.bind("<Configure>", self.on_resize)

    def show_view(self, view: ctk.CTkFrame) -> None:
        """
        Method changes visible views on right app panel.
        :param view: ctk frame contains view.
        :return: Notching, only changes widgets.
        """
        if self.current_view:
            self.current_view.pack_forget()

        self.current_view = view
        self.current_view.pack(expand=True, fill="both")

    def on_resize(self, event) -> None:
        """
        Method is responsible for scaling the sizes of texts and icons in buttons depending on the width of the window
        :param event: built in variable
        :return: Nothing, only resize text in buttons and images.
        """
        width: int = self.winfo_width()

        new_sizes: dict[str, tuple[int, int, int]] = {
            "1": (940, 1100, 18),
            "2": (1101, 1250, 20),
            "3": (1251, 1400, 22),
            "4": (1401, 1550, 24),
            "5": (1551, 1700, 26),
            "6": (1701, 1850, 28),
        }

        new_font_img_size: int | None
        new_flag: str | None

        if self.state() == "zoomed":
            new_font_img_size = 30
            new_flag = "max"
        else:
            new_font_img_size = None
            new_flag = None
            for min_w, max_w, size in new_sizes.values():
                if min_w < width <= max_w:
                    new_font_img_size = size
                    new_flag = str(size)
                    break

        if new_flag is not None and new_flag != self.flag:
            self.flag = new_flag

            if new_font_img_size is not None:
                self.btn_icons.destroy_icons()
                self.btn_icons.icon_size = new_font_img_size
                self.btn_icons.create_icons()
                self.buttons.destroy_buttons()
                self.buttons.font_size = new_font_img_size
                self.buttons.create_buttons()
