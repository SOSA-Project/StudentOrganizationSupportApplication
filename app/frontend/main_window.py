"""
This file contains main window script.
"""

import customtkinter as ctk
from PIL import Image

from app.backend.notifications import initiate_notification_manager, NotificationManager
from app.frontend.buttons import ButtonsCreator as ButtonsCreator
from app.frontend.icons import IconsHolder as IconsHolder
from app.frontend.frames import LeftFrame, RightFrame
from app.frontend.views import (
    CalendarView,
    NotificationsView,
    NotesView,
    GradesView,
    AverageView,
    SettingsView,
    ChatView,
    LoginRegisterView,
)


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
        self.parent = parent
        self.original_img = Image.open("./app/assets/logo.png")
        self.current_ctk_img = None
        self.create_labels()

    def create_labels(self) -> None:
        """
        This method creates image on GUI.
        :return: nothing.
        """
        self.current_ctk_img = ctk.CTkImage(
            light_image=self.original_img, dark_image=self.original_img, size=(100, 100)
        )

        self.logo_label = ctk.CTkLabel(self.parent, text="", image=self.current_ctk_img)
        self.logo_label.grid(row=2, rowspan=2, column=0, padx=5, pady=5)

    def resize_logo(self, size: int) -> None:
        """
        This method resize application logo.
        :param size: new logo size.
        :return: nothing, only change image size.
        """

        if size < 30:
            size = 30

        self.current_ctk_img = ctk.CTkImage(
            light_image=self.original_img, dark_image=self.original_img, size=(size, size)
        )

        self.logo_label.configure(image=self.current_ctk_img)
        self.logo_label.image = self.current_ctk_img


class AppGUI(ctk.CTk):
    """
    Main GUI class.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("SOSA")
        self.geometry("961x541")
        self.minsize(961, 541)
        self.notifications_manager: NotificationManager | None = None

        # Basic main app window setup
        self.grid_maker: GridMaker = GridMaker(self, rows=9, columns=24)
        self.login_view = LoginRegisterView(self, on_success=self.show_main_app)
        self.login_view.pack(expand=True, fill="both")

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def show_main_app(self) -> None:
        """
        Method displays the main part of the application after successful login.
        Creates main layout and initializes necessary frames, buttons and views.
        :return: Nothing, only builds main interface.
        """
        self.login_view.pack_forget()
        self.notifications_manager = initiate_notification_manager(self)
        self.btn_icons: IconsHolder = IconsHolder()
        self.left_frame: LeftFrame = LeftFrame(self, color="#444444")
        self.right_frame: RightFrame = RightFrame(self, color="#242424")

        # Container for all available views
        self.view_classes: dict[str, type[ctk.CTkFrame]] = {
            "calendar": CalendarView,
            "notifications": NotificationsView,
            "notes": NotesView,
            "grades": GradesView,
            "average": AverageView,
            "settings": SettingsView,
            "chat": ChatView,
        }

        self.views: dict[str, ctk.CTkFrame] = {}

        # Buttons for left gui frame
        self.buttons: ButtonsCreator = ButtonsCreator(self.left_frame.frame, self.btn_icons.icons, self.views, self)
        self.labels: LabelsCreator = LabelsCreator(self.left_frame.frame)

        # Current right frame view
        self.current_view: None | ctk.CTkFrame = None
        self.show_view_by_name("calendar")

        # Resizable text and images in buttons
        self.counter = 0
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

    def show_view_by_name(self, name: str) -> None:
        """
        Displays a view by its name, creating it only once (lazy loading).
        :param name: View key from self.view_classes.
        """

        if name not in self.views:
            if name in self.view_classes:
                if name == "notifications":
                    self.views[name] = NotificationsView(
                        parent=self.right_frame.frame, notification_manager=self.notifications_manager
                    )
                else:
                    self.views[name] = self.view_classes[name](self.right_frame.frame)
            else:
                print(f"Unknown view name: {name}")
                return

        if name == "average":
            self.views[name].refresh()

        self.show_view(self.views[name])

    def on_resize(self, event) -> None:
        """
        Method is responsible for scaling the sizes of texts and icons in buttons depending on the width of the window
        :param event: built in variable
        :return: Nothing, only resize text in buttons and images.
        """
        self.counter += 1
        if not self.counter % 7 == 0:
            return None
        self.counter = 0

        width: int = self.winfo_width()
        new_sizes: dict[str, tuple[int, int, int]] = {
            "1": (940, 1100, 18),
            "2": (1101, 1200, 19),
            "3": (1201, 1250, 20),
            "4": (1251, 1300, 21),
            "5": (1301, 1400, 22),
            "6": (1401, 1450, 23),
            "7": (1451, 1550, 24),
            "8": (1551, 1600, 25),
            "9": (1601, 1700, 26),
            "10": (1701, 1750, 27),
            "11": (1751, 1850, 28),
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
                self.labels.resize_logo(new_font_img_size * 6)

    def close_app(self) -> None:
        """
        Method that manages closing all processes before terminating application
        :return:
        """
        if self.notifications_manager is not None:
            self.notifications_manager.stop_checking()
        self.quit()
