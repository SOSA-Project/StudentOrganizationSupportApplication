"""
This file contains buttons implementation for left frame in gui.
"""

import customtkinter as ctk


class ButtonsCreator:
    """
    Class is responsible for storing created buttons for GUI.
    """

    def __init__(
        self, parent: ctk.CTk, icons: dict[str, ctk.CTkImage], views: dict[str, ctk.CTkFrame], app: ctk.CTkFrame
    ) -> None:
        self.parent: ctk.CTk = parent
        self.icons: dict[str, ctk.CTkImage] = icons
        self.views: dict[str, ctk.CTkFrame] = views
        self.app: ctk.CTkFrame = app
        self.font_size: int = 18
        self.buttons: dict[str, ctk.CTkButton] = {}
        self.create_buttons()

    def create_buttons(self) -> None:
        """
        Method creates all buttons for left application frame.
        :return: Nothing, only creates buttons.
        """
        self.buttons["calendar"] = ctk.CTkButton(
            self.parent,
            text="Calendar",
            font=("Roboto", self.font_size),
            image=self.icons["calendar_icon"],
            command=lambda: self.app.show_view(self.views["calendar"]),
        )
        self.buttons["calendar"].grid(row=6, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        self.buttons["notifications"] = ctk.CTkButton(
            self.parent,
            text="Notifications",
            font=("Roboto", self.font_size),
            image=self.icons["notification_icon"],
            command=lambda: self.app.show_view(self.views["notifications"]),
        )
        self.buttons["notifications"].grid(row=9, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        self.buttons["notes"] = ctk.CTkButton(
            self.parent,
            text="Notes",
            font=("Roboto", self.font_size),
            image=self.icons["notes_icon"],
            command=lambda: self.app.show_view(self.views["notes"]),
        )
        self.buttons["notes"].grid(row=12, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        self.buttons["grades"] = ctk.CTkButton(
            self.parent,
            text="Grades",
            font=("Roboto", self.font_size),
            image=self.icons["grades_icon"],
            command=lambda: self.app.show_view(self.views["grades"]),
        )
        self.buttons["grades"].grid(row=15, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        self.buttons["average"] = ctk.CTkButton(
            self.parent,
            text="Average",
            font=("Roboto", self.font_size),
            image=self.icons["average_icon"],
            command=lambda: self.app.show_view(self.views["average"]),
        )
        self.buttons["average"].grid(row=18, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        self.buttons["settings"] = ctk.CTkButton(
            self.parent,
            text="Settings",
            font=("Roboto", self.font_size),
            image=self.icons["settings_icon"],
            command=lambda: self.app.show_view(self.views["settings"]),
        )
        self.buttons["settings"].grid(row=29, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

    def destroy_buttons(self) -> None:
        """
        Method delete buttons from class.
        :return: Nothing, only delete buttons.
        """
        for button in self.buttons.values():
            button.configure(image=None)
            button.destroy()
        self.buttons.clear()
