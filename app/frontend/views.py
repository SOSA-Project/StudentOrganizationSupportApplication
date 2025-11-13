"""
This file contains views for all widgets.
"""

import random
from typing import Callable
from datetime import datetime
import calendar
from abc import ABC, abstractmethod

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from app.backend.grade_monitor import initiate_grade_monitor
from app.backend.charts import StatisticsManager, subjects_averages_histogram_plot
from app.backend.data_base import fetch_subjects, insert_grade
from app.backend.registration import get_all_users
from app.backend.registration import register_user
from app.backend.notes import initiate_note_manager
from app.backend.notes import Note


class BaseView(ctk.CTkFrame, ABC):
    """
    This class is a template for the remaining views.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent, fg_color="#444444", corner_radius=10)
        [self.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(8)]

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
        self.pack_propagate(False)

    def create_frame_content(self) -> None:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(pady=10, padx=20, fill="x")

        prev_btn = ctk.CTkButton(header_frame, text="<", width=40, command=self.prev_month)
        prev_btn.pack(side="left", padx=10, pady=10)

        self.header = ctk.CTkLabel(header_frame, text="", font=("Roboto", 18))
        self.header.pack(side="left", expand=True)

        next_btn = ctk.CTkButton(header_frame, text=">", width=40, command=self.next_month)
        next_btn.pack(side="right", padx=10, pady=10)

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
            lab = ctk.CTkLabel(self.calendar_frame, text=day, font=("Roboto", 20, "bold"))
            lab.grid(row=0, column=idx, padx=3, pady=(6, 3))
            if idx == 0:
                lab.grid_configure(padx=(6, 3))
            if idx == len(week_days) - 1:
                lab.grid_configure(padx=(3, 6))

        cal = calendar.monthcalendar(year, month)
        for r, w in enumerate(cal, start=1):
            for c, d in enumerate(w):
                if d == 0:
                    continue
                btn = ctk.CTkButton(self.calendar_frame, text=str(d), width=40, height=30, font=("Roboto", 18, "bold"))
                btn.configure(command=lambda b=btn: self.placeholder_action(b))
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                if c == 0:
                    btn.grid_configure(padx=(6, 3))
                if c == len(w) - 1:
                    btn.grid_configure(padx=(3, 6))
                if r == len(cal):
                    btn.grid_configure(pady=(3, 6))

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
        label_one.grid(row=0, rowspan=2, column=0, columnspan=8, padx=5, pady=5)


class NotesView(BaseView):
    """
    View for notes widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.note_manager = initiate_note_manager()
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        label_one: ctk.CTkLabel = ctk.CTkLabel(self, text="Notes", font=("Roboto", 18))
        label_one.grid(row=0, rowspan=2, column=0, columnspan=8, padx=5, pady=5)

        scrollable_frame: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(self)
        scrollable_frame.grid(row=2, column=0, padx=5, pady=5, columnspan=8, sticky="nsew", rowspan=50)

        if not self.note_manager or not self.note_manager.get_all_notes():
            empty_label: ctk.CTkLabel = ctk.CTkLabel(scrollable_frame, text="Notes are empty", font=("Roboto", 14))
            empty_label.pack(pady=20)
            return scrollable_frame

        notes: list[Note] = self.note_manager.get_all_notes()

        colors: list[str] = ["#ada132", "#2d7523", "#1e6a6e"]

        for i, note in enumerate(notes):
            note_frame: ctk.CTkFrame = ctk.CTkFrame(scrollable_frame, fg_color=colors[i % len(colors)])
            note_frame.pack(fill="x", pady=8, padx=8)

            title_label: ctk.CTkLabel = ctk.CTkLabel(note_frame, text=note.title, font=("Roboto", 20))
            title_label.pack(anchor="w", padx=8, pady=(8, 0))

            date_label: ctk.CTkLabel = ctk.CTkLabel(
                note_frame, text=f"Created at: {note.created_at}", font=("Roboto", 12)
            )
            date_label.pack(anchor="w", padx=8, pady=(2, 4))

            content_label: ctk.CTkLabel = ctk.CTkLabel(
                note_frame, text=note.content, wraplength=500, font=("Roboto", 18), justify="left"
            )
            content_label.pack(anchor="w", padx=8, pady=(0, 12))


class GradesView(BaseView):
    """
    View for grades widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.bg_frame: ctk.CTkFrame | None = None
        self.add_grade_bnt: ctk.CTkButton | None = None
        self.menu_values: tuple[str, ...] = ("Add new grade", "Show grades")
        self.grades: tuple[str, ...] = ("1", "2", "3", "3.5", "4", "4.5", "5", "6")
        self.grade_weight_sem: tuple[str, ...] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.grade_types: tuple[str, ...] = ("Lecture", "Laboratory", "Exercise", "Seminar")
        self.subjects = fetch_subjects()
        self.subject_data: tuple[str, ...] = (
            tuple(subject[1] for subject in self.subjects) if self.subjects is not None else ("None",)
        )
        self.labels_container: dict[str, ctk.CTkLabel] = {}
        self.options_container: dict[str, ctk.CTkOptionMenu] = {}
        self.create_frame_content()
        self.add_new_grade_gui()

    def show_grades_gui(self) -> None:
        """
        Method will be completed in next PR
        """
        pass

    def change_gui(self, _=None) -> None:
        """
        Method will be completed in next PR
        """
        print(self.menu_button.get())

    def add_grade(self) -> None:
        """
        Method add new grade into database.
        :return: Nothing, only add grade into database.
        """
        type_convert: dict[str, int] = {"Lecture": 1, "Laboratory": 2, "Exercise": 3, "Seminar": 4}
        subjects_convert: dict[str, int] = {name: sub_id for sub_id, name, ect in tuple(fetch_subjects() or [])}
        temp_user_id: int = 1
        option_data: dict[str, int | str] = dict()

        for data in self.options_container.items():
            option_data[data[0]] = str(data[1].get())

        option_data["type"] = type_convert[str(option_data["type"])]
        option_data["subject"] = subjects_convert[str(option_data["subject"])]

        insert_grade(
            value=float(option_data["value"]),
            weight=float(option_data["weight"]),
            subject_id=int(option_data["subject"]),
            semester=int(option_data["semester"]),
            sub_type=int(option_data["type"]),
            user_id=temp_user_id,
        )

    def add_new_grade_gui(self) -> None:
        """
        Method creates labels and options widget for GUI.
        :return: Nothing, only creates GUI elements.
        """
        self.bg_frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        self.bg_frame.grid(row=7, rowspan=19, column=2, columnspan=4, padx=5, pady=5, sticky="nsew")
        [self.bg_frame.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.bg_frame.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(8)]

        labels_data: set[tuple[str, str, int]] = {
            ("value", "New grade value:", 10),
            ("weight", "New grade weight:", 12),
            ("type", "New grade type:", 14),
            ("semester", "Semester number:", 16),
            ("subject", "Subject type:", 18),
        }

        options_data: set[tuple[str, tuple[str, ...], int]] = {
            ("value", self.grades, 10),
            ("weight", self.grade_weight_sem, 12),
            ("type", self.grade_types, 14),
            ("semester", self.grade_weight_sem, 16),
            ("subject", self.subject_data, 18),
        }

        for (l_key, l_text, l_row), (o_key, o_value, o_row) in zip(labels_data, options_data):
            self.labels_container[l_key] = ctk.CTkLabel(self.bg_frame, text=l_text, font=("Roboto", 18))
            self.labels_container[l_key].grid(row=l_row, rowspan=2, column=2, columnspan=2, padx=5, pady=5)
            self.options_container[o_key] = ctk.CTkOptionMenu(
                self.bg_frame, values=o_value, width=150, font=("Roboto", 18)
            )
            self.options_container[o_key].grid(row=o_row, rowspan=2, column=4, columnspan=2, padx=5, pady=5)

        self.add_grade_bnt = ctk.CTkButton(
            self.bg_frame, text="Add new grade", font=("Roboto", 18), command=self.add_grade
        )
        self.add_grade_bnt.grid(row=21, rowspan=3, column=3, columnspan=2, padx=5, pady=5)

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """

        self.menu_button = ctk.CTkSegmentedButton(
            self,
            values=self.menu_values,
            font=("Roboto", 18),
            command=self.change_gui,
            height=50,
            corner_radius=10,
            fg_color="#242424",
            border_width=5,
        )
        self.menu_button.grid(row=0, rowspan=2, column=2, columnspan=4, padx=0, pady=0)
        self.menu_button.set("Add new grade")


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
        canvas_widget.grid(row=0, rowspan=32, column=0, columnspan=8, padx=3, pady=3, sticky="nsew")

    def refresh(self) -> None:
        """
        Method refresh chart.
        :return: Nothing, only refresh chart
        """
        self.create_frame_content()


class ChatView(BaseView):
    """
    View for chat widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.users_listbox: ctk.CTkScrollableFrame | None = None
        self.chat_display: ctk.CTkTextbox | None = None
        self.message_entry: ctk.CTkEntry | None = None
        self.send_button: ctk.CTkButton | None = None
        self.selected_user: str | None = None
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        self.users_listbox = ctk.CTkScrollableFrame(self)
        self.users_listbox.grid(row=0, rowspan=32, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Configure the scrollable frame's internal grid
        self.users_listbox.grid_columnconfigure(0, weight=1)

        users = get_all_users()
        for i, user in enumerate(users or []):
            user_button = ctk.CTkButton(
                self.users_listbox, text=user[1], font=("Roboto", 16), command=lambda u=user[1]: self.on_user_click(u)
            )
            user_button.grid(row=i, column=0, sticky="ew", padx=10, pady=2)

        self.chat_display = ctk.CTkTextbox(self, font=("Roboto", 14), wrap="word")
        self.chat_display.grid(row=0, rowspan=28, column=2, columnspan=6, sticky="nsew", padx=5, pady=5)
        self.chat_display.configure(state="disabled")

        self.message_entry = ctk.CTkEntry(self, placeholder_text="Type your message...", font=("Roboto", 14))
        self.message_entry.grid(row=28, rowspan=2, column=2, columnspan=5, sticky="ew", padx=5, pady=5)

        self.send_button = ctk.CTkButton(self, text="Send", font=("Roboto", 14), command=self.send_message)
        self.send_button.grid(row=28, rowspan=2, column=7, sticky="ew", padx=5, pady=5)

    def on_user_click(self, username: str) -> None:
        """
        Handles user button click.
        :param username: The username of the clicked user.
        :return: None
        """
        self.selected_user = username
        if self.chat_display is not None:
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"Selected user: {username}\n")
            self.chat_display.configure(state="disabled")

    def send_message(self) -> None:
        """
        Appends the typed message to the chat display.
        :return: None
        """
        if self.message_entry is not None and self.chat_display is not None:
            message = self.message_entry.get().strip()
            if message and self.selected_user:
                self.chat_display.configure(state="normal")
                self.chat_display.insert("end", f"You to {self.selected_user}: {message}\n")
                self.chat_display.configure(state="disabled")
                self.message_entry.delete(0, "end")


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
        label_one.grid(row=0, rowspan=2, column=0, columnspan=8, padx=5, pady=5)


class LoginRegisterView(ctk.CTkFrame):
    """
    View for user login and registration.
    Appears on app start.
    """

    def __init__(self, parent: ctk.CTk, on_success: Callable) -> None:
        super().__init__(parent, fg_color="#444444", corner_radius=10)
        self.on_success = on_success
        self.create_frame_content()

    def create_frame_content(self) -> None:
        """
        This method creates elements visible on the frame.
        :return: None
        """

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.bg_frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        self.bg_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        for i in range(10):
            self.bg_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.bg_frame.grid_columnconfigure(i, weight=1)

        title_label = ctk.CTkLabel(self.bg_frame, text="Student Planner Login/Register", font=("Roboto", 24))
        title_label.grid(row=1, column=1, columnspan=4, sticky="nsew")

        self.username_entry = ctk.CTkEntry(self.bg_frame, placeholder_text="Username", font=("Roboto", 18))
        self.username_entry.grid(row=4, column=2, columnspan=2, sticky="ew", padx=20)

        login_btn = ctk.CTkButton(self.bg_frame, text="Login", font=("Roboto", 18), command=self.login_user)
        login_btn.grid(row=6, column=2, sticky="nsew", padx=10, pady=10)

        register_btn = ctk.CTkButton(self.bg_frame, text="Register", font=("Roboto", 18), command=self.register_user)
        register_btn.grid(row=6, column=3, sticky="nsew", padx=10, pady=10)

        self.feedback_label = ctk.CTkLabel(self.bg_frame, text="", font=("Roboto", 14), text_color="red")
        self.feedback_label.grid(row=7, column=1, columnspan=4, sticky="nsew", pady=10)

    def login_user(self) -> None:
        """
        This method handles the login process and displays messages.
        :return: None
        """

        username = self.username_entry.get().strip()
        if not username:
            self.feedback_label.configure(text="Username cannot be empty!")
            return

        users = get_all_users()
        if users and any(u[1].lower() == username.lower() for u in users):
            self.feedback_label.configure(text="Login successful!", text_color="green")
            self.after(500, self.on_success)
        else:
            self.feedback_label.configure(text="User not found!")

    def register_user(self) -> None:
        """
        This method handles the registration process and displays messages.
        :return: None
        """

        username = self.username_entry.get().strip()
        if not username:
            self.feedback_label.configure(text="Username cannot be empty!")
            return

        result = register_user(username)
        if result:
            self.feedback_label.configure(text="Registration successful!", text_color="green")
            self.after(500, self.on_success)
        else:
            self.feedback_label.configure(text="User already exists or error!")
