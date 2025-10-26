from __future__ import annotations

import customtkinter as ctk

from app.frontend.icons import IconsHolder as IconsHolder


class ButtonsCreator:
    """
    Class is responsible for storing created buttons for GUI.
    """

    def __init__(self, parent: ctk.CTk, icons: IconsHolder, views: dict, app) -> None:
        self.parent: ctk.CTk = parent
        self.icons: IconsHolder = icons
        self.views = views
        self.app = app
        self.create_buttons()

    def create_buttons(self) -> None:
        """
        Method creates all buttons for left application frame.
        :return: Nothing, only creates buttons.
        """
        btn_calendar: ctk.CTkButton = ctk.CTkButton(
            self.parent,
            text="Calendar",
            font=("Roboto", 18),
            image=self.icons.calendar_icon,
            command=lambda: self.app.show_view(self.views["calendar"]),
        )
        btn_calendar.grid(row=6, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_notifications: ctk.CTkButton = ctk.CTkButton(
            self.parent,
            text="Notifications",
            font=("Roboto", 18),
            image=self.icons.notification_icon,
            command=lambda: self.app.show_view(self.views["notifications"]),
        )
        btn_notifications.grid(row=9, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_notes: ctk.CTkButton = ctk.CTkButton(
            self.parent,
            text="Notes",
            font=("Roboto", 18),
            image=self.icons.notes_icon,
            command=lambda: self.app.show_view(self.views["notes"]),
        )
        btn_notes.grid(row=12, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_grades: ctk.CTkButton = ctk.CTkButton(
            self.parent,
            text="Grades",
            font=("Roboto", 18),
            image=self.icons.grades_icon,
            command=lambda: self.app.show_view(self.views["grades"]),
        )
        btn_grades.grid(row=15, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_average: ctk.CTkButton = ctk.CTkButton(
            self.parent,
            text="Average",
            font=("Roboto", 18),
            image=self.icons.average_icon,
            command=lambda: self.app.show_view(self.views["average"]),
        )
        btn_average.grid(row=18, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)

        btn_settings: ctk.CTkButton = ctk.CTkButton(
            self.parent,
            text="Settings",
            font=("Roboto", 18),
            image=self.icons.settings_icon,
            command=lambda: self.app.show_view(self.views["settings"]),
        )
        btn_settings.grid(row=29, rowspan=3, column=0, columnspan=1, sticky="nsew", padx=8, pady=6)
