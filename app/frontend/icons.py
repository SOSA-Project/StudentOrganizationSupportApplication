"""
This file contains class for icons in for buttons.
"""

from PIL import Image

import customtkinter as ctk


class IconsHolder:
    """
    Class is responsible for read icons for GUI.
    """

    def __init__(self) -> None:
        self.icon_size: int = 20
        self.icons: dict[str, ctk.CTkImage] = {}

        self.icons_paths = {
            "calendar_path": Image.open("./app/assets/calendar.png"),
            "notification_path": Image.open("./app/assets/bell.png"),
            "notes_path": Image.open("./app/assets/notes.png"),
            "grades_path": Image.open("./app/assets/grades.png"),
            "average_path": Image.open("./app/assets/chart.png"),
            "settings_path": Image.open("./app/assets/settings.png"),
        }

        self.read_icons()

    def read_icons(self):
        self.icons["calendar_icon"] = ctk.CTkImage(
            light_image=self.icons_paths["calendar_path"],
            dark_image=self.icons_paths["calendar_path"],
            size=(self.icon_size, self.icon_size),
        )
        self.icons["notification_icon"] = ctk.CTkImage(
            light_image=self.icons_paths["notification_path"],
            dark_image=self.icons_paths["notification_path"],
            size=(self.icon_size, self.icon_size),
        )
        self.icons["notes_icon"] = ctk.CTkImage(
            light_image=self.icons_paths["notes_path"],
            dark_image=self.icons_paths["notes_path"],
            size=(self.icon_size, self.icon_size),
        )
        self.icons["grades_icon"] = ctk.CTkImage(
            light_image=self.icons_paths["grades_path"],
            dark_image=self.icons_paths["grades_path"],
            size=(self.icon_size, self.icon_size),
        )
        self.icons["average_icon"] = ctk.CTkImage(
            light_image=self.icons_paths["average_path"],
            dark_image=self.icons_paths["average_path"],
            size=(self.icon_size, self.icon_size),
        )
        self.icons["settings_icon"] = ctk.CTkImage(
            light_image=self.icons_paths["settings_path"],
            dark_image=self.icons_paths["settings_path"],
            size=(self.icon_size, self.icon_size),
        )

    def destroy_icons(self):
        self.icons.clear()
