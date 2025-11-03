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
        self.font_family: str = "Roboto"
        self.buttons: dict[str, ctk.CTkButton] = {}
        self.create_buttons()

    def create_buttons(self) -> None:
        """
        Method creates all buttons for left application frame.
        :return: Nothing, only creates buttons.
        """
        button_config = {
            ("calendar", "Calendar", 6),
            ("notifications", "Notifications", 9),
            ("notes", "Notes", 12),
            ("grades", "Grades", 15),
            ("average", "Average", 18),
            ("chat", "Chat", 21),
            ("settings", "Settings", 29),
        }

        for key, text, row in button_config:
            self.buttons[key] = ctk.CTkButton(
                self.parent,
                text=text,
                font=(self.font_family, self.font_size),
                image=self.icons[f"{key}_icon"],
                command=lambda k=key: self.app.show_view(self.views[k]),
            )
            self.buttons[key].grid(row=row, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=5)

    def destroy_buttons(self) -> None:
        """
        Method delete buttons from class.
        :return: Nothing, only delete buttons.
        """
        for button in self.buttons.values():
            button.configure(image=None)
            button.destroy()
        self.buttons.clear()
