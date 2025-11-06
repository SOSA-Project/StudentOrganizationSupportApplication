"""
This file contains views for all widgets.
"""

import random
from abc import ABC, abstractmethod


import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import calendar

from app.backend.grade_monitor import initiate_grade_monitor
from app.backend.charts import StatisticsManager, subjects_averages_histogram_plot


class BaseView(ctk.CTkFrame, ABC):
    """
    This class is a template for the remaining views.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent, fg_color="#444444", corner_radius=10)
        [self.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(1)]

        self.grid_propagate(False)
        self.update_idletasks()

    @abstractmethod
    def create_frame_content(self) -> None:
        """
        Abstract method for BaseView class.
        :return: Nothing, this is abstract method.
        """
        pass


class CalendarView(BaseView):
    """
    View for calendar widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.current_date = datetime.now()
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(pady=10, padx=20, fill="both")

        prev_btn = ctk.CTkButton(header_frame, text="<", width=40, command=self.prev_month)
        prev_btn.pack(side="left", padx=10)

        self.header = ctk.CTkLabel(header_frame, text="", font=("Roboto", 18))
        self.header.pack(side="left", expand=True)

        next_btn = ctk.CTkButton(header_frame, text=">", width=40, command=self.next_month)
        next_btn.pack(side="right", padx=10)

        self.calendar_frame = ctk.CTkFrame(self)
        self.calendar_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.update_calendar()

    def update_calendar(self) -> None:
        """
        This method updates the calendar view with the according month and a year destroying previous widgets
        and creating new ones in their place
        :return: Nothing
        """
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        year, month = self.current_date.year, self.current_date.month
        self.header.configure(text=f"{calendar.month_name[month]} {year}")

        week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for idx, day in enumerate(week_days):
            (
                ctk.CTkLabel(self.calendar_frame, text=day, font=("Roboto", 20, "bold")).grid(
                    row=0, column=idx, padx=5, pady=5
                )
            )

        cal = calendar.monthcalendar(year, month)
        for r, w in enumerate(cal, start=1):
            for c, d in enumerate(w):
                if d == 0:
                    continue
                btn = ctk.CTkButton(self.calendar_frame, text=str(d), width=40, height=30, font=("Roboto", 18, "bold"))
                btn.configure(command=lambda b=btn: self.placeholder_action(b))
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

        for col in range(7):
            self.calendar_frame.grid_columnconfigure(col, weight=1)
        for row in range(len(cal) + 1):
            self.calendar_frame.grid_rowconfigure(row, weight=1)

    def placeholder_action(self, btn: ctk.CTkButton) -> None:
        """
        This method is just a placeholder and will be removed in the future
        :param btn: Day button placeholder
        :return: Nothing
        """
        btn.configure(fg_color="#" + str(random.randint(100000, 999999)))

    def prev_month(self) -> None:
        """
        Changes currently viewed month to a previous month and updates the calendar view
        :return: Nothing
        """
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()

    def next_month(self) -> None:
        """
        Changes currently viewed month to a following month and updates the calendar view
        :return: Nothing
        """
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()


class NotificationsView(BaseView):
    """
    View for notifications widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        label_one: ctk.CTkLabel = ctk.CTkLabel(self, text="Notifications", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class NotesView(BaseView):
    """
    View for notes widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        label_one: ctk.CTkLabel = ctk.CTkLabel(self, text="Notes", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)

        scrollable_frame: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(self)
        scrollable_frame.grid(row=2, column=0, padx=5, pady=5, columnspan=1, sticky="nsew", rowspan=50)

        colors: list[str] = ["#ada132", "#2d7523", "#1e6a6e"]

        for x in range(10):
            note_frame: ctk.CTkFrame = ctk.CTkFrame(scrollable_frame, fg_color=colors[x % len(colors)])
            note_frame.pack(fill="x", pady=10, padx=10)

            title_label = ctk.CTkLabel(note_frame, text=f"Title {x}", font=("Roboto", 18, "bold"))
            title_label.pack(anchor="w")

            date_label = ctk.CTkLabel(note_frame, text="Created at Date", font=("Roboto", 10))
            date_label.pack(anchor="w")

            content_label = ctk.CTkLabel(note_frame, text="Content", wraplength=1000, font=("Roboto", 12))
            content_label.pack(anchor="w", pady=(0, 5))


class GradesView(BaseView):
    """
    View for grades widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        label_one: ctk.CTkLabel = ctk.CTkLabel(self, text="Grades", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class AverageView(BaseView):
    """
    View for average widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        if (grades_data := initiate_grade_monitor()) is None:
            return

        charts_manager: StatisticsManager = StatisticsManager(grades_data)
        grades_avg: dict[str, float] = charts_manager.subjects_averages()
        histogram: Figure = subjects_averages_histogram_plot(grades_avg, "dark")
        canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(histogram, master=self)
        canvas.draw()
        plt.close(histogram)

        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(bg=self.cget("fg_color"), highlightthickness=0, bd=0)
        canvas_widget.grid(row=0, rowspan=32, column=0, columnspan=1, padx=3, pady=3, sticky="nsew")


class ChatView(BaseView):
    """
    View for chat widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        label_one: ctk.CTkLabel = ctk.CTkLabel(self, text="Chat", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)


class SettingsView(BaseView):
    """
    View for settings widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        label_one: ctk.CTkLabel = ctk.CTkLabel(self, text="Settings", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=1, padx=5, pady=5)
