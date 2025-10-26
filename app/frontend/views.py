from abc import ABC, abstractmethod

import customtkinter as ctk

class BaseView(ctk.CTkFrame, ABC):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#444444", corner_radius=10)
        [self.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(1)]
        self.grid_propagate(False)
        self.update_idletasks()

    @abstractmethod
    def create_frame_content(self):
        pass


class CalendarView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self):
        label_one = ctk.CTkLabel(self, text="Calendar", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class NotificationsView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self):
        label_one = ctk.CTkLabel(self, text="Notifications", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class NotesView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self):
        label_one = ctk.CTkLabel(self, text="Notes", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class GradesView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self):
        label_one = ctk.CTkLabel(self, text="Grades", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class AverageView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self):
        label_one = ctk.CTkLabel(self, text="Average", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class SettingsView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self):
        label_one = ctk.CTkLabel(self, text="Settings", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)
