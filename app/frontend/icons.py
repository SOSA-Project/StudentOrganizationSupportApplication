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
        self.icons_paths: dict[str, ctk.CTkImage] = {
            "calendar_path": Image.open("./app/assets/calendar.png"),
            "notification_path": Image.open("./app/assets/bell.png"),
            "notes_path": Image.open("./app/assets/notes.png"),
            "grades_path": Image.open("./app/assets/grades.png"),
            "average_path": Image.open("./app/assets/chart.png"),
            "settings_path": Image.open("./app/assets/settings.png"),
        }
        self.create_icons()

    def create_icons(self) -> None:
        """
        Method is responsible for creating images based on icons
        :return: Nothing, only reads icons form disk.
        """
        icons_config = {
            ("calendar_icon", "calendar_path"),
            ("notifications_icon", "notification_path"),
            ("notes_icon", "notes_path"),
            ("grades_icon", "grades_path"),
            ("average_icon", "average_path"),
            ("settings_icon", "settings_path")
        }

        for icon, path in icons_config:
            self.icons[icon] = ctk.CTkImage(
                light_image=self.icons_paths[path],
                dark_image=self.icons_paths[path],
                size=(self.icon_size, self.icon_size)
            )


    def destroy_icons(self) -> None:
        """
        Method delete icons from class.
        :return: Nothing, only delete icons from class.
        """
        self.icons.clear()
