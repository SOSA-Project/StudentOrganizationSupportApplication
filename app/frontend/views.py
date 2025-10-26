import customtkinter as ctk


class CalendarView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Calendar", font=("Roboto", 18)).pack(pady=20)


class NotificationsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Notifications", font=("Roboto", 18)).pack(pady=20)


class NotesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Notes", font=("Roboto", 18)).pack(pady=20)


class GradesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Grades", font=("Roboto", 18)).pack(pady=20)


class AverageView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Average", font=("Roboto", 18)).pack(pady=20)


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Settings", font=("Roboto", 18)).pack(pady=20)
