import customtkinter as ctk

from app.frontend.frames import LeftFrame, RightFrame


class CalendarView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#444444", corner_radius=10)  # własny styl widoku

        [self.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(1)]

        self.grid_propagate(False)  # wewnątrz widoku
        self.update_idletasks()

        label_one = ctk.CTkLabel(self, text="Calendar", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class NotificationsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#444444", corner_radius=10)  # własny styl widoku

        # Konfiguracja siatki w obrębie widoku
        for i in range(32):
            self.grid_rowconfigure(i, weight=1, uniform="rowcol")
        for i in range(1):
            self.grid_columnconfigure(i, weight=1, uniform="rowcol")

        self.grid_propagate(False)  # wewnątrz widoku
        self.update_idletasks()

        label_one = ctk.CTkLabel(self, text="Notification", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)
#
#
# class NotesView(ctk.CTkFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         ctk.CTkLabel(self.parent, text="Notes", font=("Roboto", 18))
#
#
# class GradesView(ctk.CTkFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         ctk.CTkLabel(self.parent, text="Grades", font=("Roboto", 18))
#
#
# class AverageView(ctk.CTkFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         ctk.CTkLabel(self.parent, text="Average", font=("Roboto", 18))
#
#
# class SettingsView(ctk.CTkFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         ctk.CTkLabel(self.parent, text="Settings", font=("Roboto", 18))
