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
        self.calendar_icon: ctk.CTkImage = ctk.CTkImage(
            light_image=Image.open("./app/assets/calendar.png"),
            dark_image=Image.open("./app/assets/calendar.png"),
            size=(20, 20),
        )
        self.notification_icon: ctk.CTkImage = ctk.CTkImage(
            light_image=Image.open("./app/assets/bell.png"),
            dark_image=Image.open("./app/assets/bell.png"),
            size=(20, 20),
        )
        self.notes_icon: ctk.CTkImage = ctk.CTkImage(
            light_image=Image.open("./app/assets/notes.png"),
            dark_image=Image.open("./app/assets/notes.png"),
            size=(20, 20),
        )
        self.grades_icon: ctk.CTkImage = ctk.CTkImage(
            light_image=Image.open("./app/assets/grades.png"),
            dark_image=Image.open("./app/assets/grades.png"),
            size=(20, 20),
        )
        self.average_icon: ctk.CTkImage = ctk.CTkImage(
            light_image=Image.open("./app/assets/chart.png"),
            dark_image=Image.open("./app/assets/chart.png"),
            size=(20, 20),
        )
        self.settings_icon: ctk.CTkImage = ctk.CTkImage(
            light_image=Image.open("./app/assets/settings.png"),
            dark_image=Image.open("./app/assets/settings.png"),
            size=(20, 20),
        )
