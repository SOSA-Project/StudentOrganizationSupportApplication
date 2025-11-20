"""
This file contains views for all widgets.
"""

import random
from gc import collect
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
from app.backend.data_base import (
    fetch_subjects,
    insert_grade,
    fetch_grades_id,
    update_grade,
    delete_grade,
    fetch_grades,
    fetch_users,
    Persistant,
)
from app.backend.registration import get_all_users
from app.backend.registration import register_user
from app.backend.notes import initiate_note_manager
from app.backend.notes import Note
from app.backend.tooltip import Tooltip

from app.backend.chat import Chat, send
from app.backend.session import Session


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
        self.note_manager = initiate_note_manager()
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

        current_notes: list[Note] = self.get_notes_for_current_month()

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
                date_notes: list[Note] = [
                    n for n in current_notes if n.associated_date is not None and n.associated_date.day == d
                ]
                for i, note in enumerate(date_notes):
                    Tooltip(btn, note.content, note.color, x_offset=i * 265 + 10)
                    btn.configure(fg_color=note.color, hover_color=self.darken_color(note.color))

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

    def get_notes_for_current_month(self) -> list[Note]:
        """
        Method gathers currently relevant notes pointing to dates in currently displayed month and year
        :return: List containing all relevant notes
        """
        current_notes: list[Note] = []
        if self.note_manager is not None:
            current_notes = self.note_manager.get_all_notes()
            current_notes[0].associated_date = datetime(year=2025, month=11, day=1)
            current_notes[1].associated_date = datetime(year=2025, month=11, day=19)
            current_notes[2].associated_date = datetime(year=2025, month=11, day=19)
            current_notes[3].associated_date = datetime(year=2025, month=11, day=30)
            if current_notes is not None:
                current_notes = list(
                    filter(
                        lambda n: n.associated_date is not None
                        and n.associated_date.year == self.current_date.year
                        and n.associated_date.month == self.current_date.month,
                        current_notes,
                    )
                )
            else:
                return []
        return current_notes

    def darken_color(self, hex_color: str, factor: float = 0.8) -> str:
        """
        Method generates a new color code based on factor variable, used for button hover color
        :param hex_color: Original color
        :param factor: Factor based on which the color is modified <1 - color is darker >1 color is lighter
        :return: Modified color code
        """
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        return f"#{r:02x}{g:02x}{b:02x}"


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

        for i, note in enumerate(notes):
            note_frame: ctk.CTkFrame = ctk.CTkFrame(scrollable_frame, fg_color=note.color)
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
    View for grades.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.menu_values = ("Add new grade", "Edit grade", "Delete grade", "Show grades")
        self.grades = ("1", "2", "3", "3.5", "4", "4.5", "5", "6")
        self.grade_weight_sem = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.grade_types = ("Lecture", "Laboratory", "Exercise", "Seminar")

        self.subject_data, self.grades_id_data = self._update_options_data()
        self.labels_container: dict[str, ctk.CTkLabel] = {}
        self.options_container: dict[str, ctk.CTkOptionMenu] = {}

        self.create_frame_content()

        self.grade_views = {
            "add_view": self.add_new_grade_gui(),
            "delete_view": self.delete_grade_gui(),
            "edit_view": self.edit_grade_gui(),
            "show_grades": self.show_grades_gui(),
        }

        self.show_view(self.grade_views["edit_view"])
        self.show_view(self.grade_views["add_view"])

    def _prepare_data_for_db(self) -> dict[str, int | str]:
        """
        Support method prepare data from database for option menus.
        :return: prepared data.
        """
        type_convert = {"Lecture": 1, "Laboratory": 2, "Exercise": 3, "Seminar": 4}
        subjects_convert = {name: sub_id for sub_id, name, ect in tuple(fetch_subjects() or [])}
        option_data: dict[str, int | str] = {}

        for data in self.options_container.items():
            option_data[data[0]] = str(data[1].get())

        option_data["type_add"] = type_convert[str(option_data["type_add"])]
        option_data["type_edit"] = type_convert[str(option_data["type_edit"])]
        option_data["subject_add"] = subjects_convert[str(option_data["subject_add"])]
        option_data["subject_edit"] = subjects_convert[str(option_data["subject_edit"])]
        return option_data

    def _update_options_data(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """
        Support method updates data after change.
        :return: updated data.
        """
        subjects = fetch_subjects()
        subject_data = tuple(subject[1] for subject in subjects) if subjects else ("None",)
        grades_id = fetch_grades_id()
        grades_id_data = tuple(str(g_id[0]) for g_id in grades_id) if grades_id else ("None",)
        return subject_data, grades_id_data

    def _display_frame_elements(self, labels_data, options_data, parent) -> None:
        """
        Support method for displaying GUI content.
        :param labels_data: data about labels.
        :param options_data: data about options.
        :param parent: main frame.
        :return: Nothing, only create GUI content.
        """
        for (l_key, l_text, l_row), (o_key, o_value, o_row) in zip(labels_data, options_data):
            self.labels_container[l_key] = ctk.CTkLabel(parent, text=l_text, font=("Roboto", 18))
            self.labels_container[l_key].grid(row=l_row, rowspan=2, column=2, columnspan=2, padx=5, pady=5)

            self.options_container[o_key] = ctk.CTkOptionMenu(parent, values=o_value, width=150, font=("Roboto", 18))
            self.options_container[o_key].grid(row=o_row, rowspan=2, column=4, columnspan=2, padx=5, pady=5)

    def refresh_options_in_frame(self, view_name: str) -> None:
        """
        Method updates data in options menus.
        :param view_name: view name.
        :return: Nothing.
        """
        self.subject_data, self.grades_id_data = self._update_options_data()

        if view_name == "add_view":
            self.options_container["value_add"].configure(values=self.grades)
            self.options_container["weight_add"].configure(values=self.grade_weight_sem)
            self.options_container["type_add"].configure(values=self.grade_types)
            self.options_container["semester_add"].configure(values=self.grade_weight_sem)
            self.options_container["subject_add"].configure(values=self.subject_data)
        elif view_name == "edit_view":
            self.options_container["id_edit"].configure(values=self.grades_id_data)
            self.options_container["value_edit"].configure(values=self.grades)
            self.options_container["weight_edit"].configure(values=self.grade_weight_sem)
            self.options_container["type_edit"].configure(values=self.grade_types)
            self.options_container["semester_edit"].configure(values=self.grade_weight_sem)
            self.options_container["subject_edit"].configure(values=self.subject_data)
        elif view_name == "delete_view":
            self.options_container["id_del"].configure(values=self.grades_id_data)

    def change_gui(self, _=None) -> None:
        """
        This method is responsible for changing GUIs.
        :param _: temp param for get().
        :return: Nothing, only changes windows.
        """
        button_value = self.menu_button.get()

        match button_value:
            case "Add new grade":
                self.refresh_options_in_frame("add_view")
                self.show_view(self.grade_views["add_view"])
            case "Edit grade":
                self.refresh_options_in_frame("edit_view")
                self.show_view(self.grade_views["edit_view"])
            case "Delete grade":
                self.refresh_options_in_frame("delete_view")
                self.show_view(self.grade_views["delete_view"])
            case "Show grades":
                self.refresh_grades_table()
                self.show_view(self.grade_views["show_grades"])

        self.menu_label.configure(text="")

    def add_grade(self) -> None:
        """
        This method adds new grades into database.
        :return: Nothing, only adds grades into database.
        """
        option_data: dict[str, int | str] = self._prepare_data_for_db()
        temp_user_id: int = 1

        insert_grade(
            value=float(option_data["value_add"]),
            weight=float(option_data["weight_add"]),
            subject_id=int(option_data["subject_add"]),
            semester=int(option_data["semester_add"]),
            sub_type=int(option_data["type_add"]),
            user_id=temp_user_id,
        )

        self.subject_data, self.grades_id_data = self._update_options_data()
        self.delete_id_optionmenu.configure(values=self.grades_id_data)
        self.menu_label.configure(text="New grade has been added")

    def edit_grade(self) -> None:
        """
        Work in progress
        :return:
        """
        option_data: dict[str, int | str] = self._prepare_data_for_db()
        temp_user_id: int = 1

        update_grade(
            grade_id=int(option_data["id_edit"]),
            value=float(option_data["value_edit"]),
            weight=float(option_data["weight_edit"]),
            sub_type=int(option_data["type_edit"]),
            semester=int(option_data["semester_edit"]),
            subject_id=int(option_data["subject_edit"]),
            user_id=temp_user_id,
        )

        self.subject_data, self.grades_id_data = self._update_options_data()
        self.delete_id_optionmenu.configure(values=self.grades_id_data)
        self.menu_label.configure(text="Grade has been updated")

    def delete_grade(self) -> None:
        """
        Method deletes choosed grade from database.
        :return: Nothing.
        """
        option_data: dict[str, int | str] = self._prepare_data_for_db()
        delete_grade(grade_id=int(option_data["id_del"]))

        self.subject_data, self.grades_id_data = self._update_options_data()
        self.delete_id_optionmenu.configure(values=self.grades_id_data)
        self.menu_label.configure(text="Grade has been deleted")

    def add_new_grade_gui(self) -> ctk.CTkFrame:
        """
        This method creates GUI for adding new grades into database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        labels_data = {
            ("value", "New grade value:", 10),
            ("weight", "New grade weight:", 12),
            ("type", "New grade type:", 14),
            ("semester", "Semester number:", 16),
            ("subject", "Subject type:", 18),
        }

        options_data = {
            ("value_add", self.grades, 10),
            ("weight_add", self.grade_weight_sem, 12),
            ("type_add", self.grade_types, 14),
            ("semester_add", self.grade_weight_sem, 16),
            ("subject_add", self.subject_data, 18),
        }

        self._display_frame_elements(labels_data, options_data, frame)
        self.add_grade_bnt = ctk.CTkButton(frame, text="Add new grade", font=("Roboto", 18), command=self.add_grade)
        self.add_grade_bnt.grid(row=26, rowspan=3, column=3, columnspan=2, padx=5, pady=5, sticky="nsew")

        return frame

    def delete_grade_gui(self) -> ctk.CTkFrame:
        """
        This method creates GUI for deleting grades into database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        labels_data = {("id_del", "Current grade ID:", 14)}
        options_data = {("id_del", self.grades_id_data, 14)}

        self._display_frame_elements(labels_data, options_data, frame)
        self.delete_id_optionmenu = self.options_container["id_del"]

        self.delete_grade_bnt = ctk.CTkButton(
            frame, text="Delete grade", font=("Roboto", 18), command=self.delete_grade
        )
        self.delete_grade_bnt.grid(row=26, rowspan=3, column=3, columnspan=2, padx=5, pady=5, sticky="nsew")

        return frame

    def edit_grade_gui(self) -> ctk.CTkFrame:
        """
        This method creates GUI for update new grades in database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        labels_data = {
            ("id", "Current grade ID:", 8),
            ("value", "New grade value:", 10),
            ("weight", "New grade weight:", 12),
            ("type", "New grade type:", 14),
            ("semester", "Semester number:", 16),
            ("subject", "Subject type:", 18),
        }

        options_data = {
            ("id_edit", self.grades_id_data, 8),
            ("value_edit", self.grades, 10),
            ("weight_edit", self.grade_weight_sem, 12),
            ("type_edit", self.grade_types, 14),
            ("semester_edit", self.grade_weight_sem, 16),
            ("subject_edit", self.subject_data, 18),
        }

        self._display_frame_elements(labels_data, options_data, frame)
        self.edit_grade_bnt = ctk.CTkButton(frame, text="Edit grade", font=("Roboto", 18), command=self.edit_grade)
        self.edit_grade_bnt.grid(row=26, rowspan=3, column=3, columnspan=2, padx=5, pady=5, sticky="nsew")

        return frame

    def show_grades_gui(self) -> ctk.CTkFrame:
        """
        Method that creates GUI for showing grades in database.
        :return: New CTK frame.
        """
        frame: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.grades_textbox: ctk.CTkTextbox = ctk.CTkTextbox(frame, font=("Consolas", 18), fg_color="#242424")
        self.grades_textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.grades_textbox.configure(state="disabled")

        self.refresh_grades_table()

        return frame

    def refresh_grades_table(self) -> None:
        """
        Method that fills the grades table.
        :return: Nothing
        """
        decode_grade_type = {1: "Lecture", 2: "Laboratory", 3: "Exercise", 4: "Seminar"}

        if not hasattr(self, "grades_textbox"):
            return

        grades_data = fetch_grades()

        self.grades_textbox.configure(state="normal")
        self.grades_textbox.delete("1.0", "end")

        if not grades_data:
            self.grades_textbox.insert("end", "No grades available")
        else:
            headers: tuple[str, ...] = ("ID", "Value", "Subject", "ECTS", "Weight", "Type")
            self.grades_textbox.insert(
                "end",
                f"{headers[0]:<6} {headers[1]:<8} {headers[2]:<20} {headers[3]:<6} {headers[4]:<8} {headers[5]:<10}\n",
            )
            self.grades_textbox.insert("end", "-" * 63 + "\n")

            for g_value, s_name, s_ects, g_weight, g_type, g_id in grades_data:
                self.grades_textbox.insert(
                    "end",
                    f"{g_id:<6} {g_value:<8} {s_name:<20} {s_ects:<6} "
                    f"{g_weight:<8} {decode_grade_type[int(g_type)]:<12}\n",
                )

        self.grades_textbox.configure(state="disabled")

    def create_frame_content(self) -> None:
        """
        This method creates constant GUI content.
        :return: Nothing, only create elements.
        """
        self.menu_button = ctk.CTkSegmentedButton(
            self,
            values=self.menu_values,
            font=("Roboto", 24),
            command=self.change_gui,
            height=50,
            corner_radius=10,
            fg_color="#242424",
            border_width=5,
        )
        self.menu_button.grid(row=2, rowspan=2, column=2, columnspan=4, padx=0, pady=0)
        self.menu_button.set("Add new grade")

        self.menu_label = ctk.CTkLabel(
            self,
            text="",
            font=("Roboto", 24),
            height=50,
            corner_radius=10,
            fg_color="#242424",
        )
        self.menu_label.grid(row=27, rowspan=2, column=2, columnspan=4, padx=5, pady=5, sticky="ew")

    def show_view(self, view: ctk.CTkFrame) -> None:
        """
        This method is responsible for changing GUI frames.
        :param view: new view to display.
        :return: Nothing, only change GUI windows.
        """
        view.tkraise()
        self.current_view = view
        self.current_view.grid(row=6, rowspan=19, column=2, columnspan=4, padx=5, pady=5, sticky="nsew")


class AverageView(BaseView):
    """
    View for average widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.canvas: FigureCanvasTkAgg | None = None
        self.create_frame_content()

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """

        self._destroy_old_canvas()

        if (grades_data := initiate_grade_monitor()) is None:
            return

        charts_manager: StatisticsManager = StatisticsManager(grades_data)
        grades_avg: dict[str, float] = charts_manager.subjects_averages()
        histogram: Figure = subjects_averages_histogram_plot(grades_avg, "dark")
        self.canvas = FigureCanvasTkAgg(histogram, master=self)
        self.canvas.draw()
        plt.close(histogram)

        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(bg=self.cget("fg_color"), highlightthickness=0, bd=0)
        canvas_widget.grid(row=0, rowspan=32, column=0, columnspan=8, padx=3, pady=3, sticky="nsew")

    def refresh(self) -> None:
        """
        Method refresh chart.
        :return: Nothing, only refresh chart
        """
        self.create_frame_content()

    def _destroy_old_canvas(self) -> None:
        """
        Method delete old chart from app.
        :return: Nothing, only delete old chart.
        """
        if self.canvas is not None:
            widget = self.canvas.get_tk_widget()
            widget.destroy()
            fig = self.canvas.figure
            fig.clear()
            plt.close(fig)
            self.canvas = None
            collect()


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
            if user[0] == Persistant.get_id():  # remove own user
                continue
            user_button = ctk.CTkButton(
                self.users_listbox, text=user[1], font=("Roboto", 16), command=lambda u=user[2]: self.on_user_click(u)
            )
            user_button.grid(row=i, column=0, sticky="ew", padx=10, pady=2)

        self.chat_display = ctk.CTkTextbox(self, font=("Roboto", 14), wrap="word")
        self.chat_display.grid(row=0, rowspan=28, column=2, columnspan=6, sticky="nsew", padx=5, pady=5)
        self.chat_display.configure(state="disabled")

        Chat.chat_display = self.chat_display

        self.message_entry = ctk.CTkEntry(self, placeholder_text="Type your message...", font=("Roboto", 14))
        self.message_entry.grid(row=28, rowspan=2, column=2, columnspan=5, sticky="ew", padx=5, pady=5)

        self.send_button = ctk.CTkButton(self, text="Send", font=("Roboto", 14), command=self.send_message)
        self.send_button.grid(row=28, rowspan=2, column=7, sticky="ew", padx=5, pady=5)

        Chat.connect()

    def on_user_click(self, uuid: str) -> None:
        """
        Handles user button click.
        :param uuid: The uuid of the clicked user.
        :return: None
        """
        self.selected_user = uuid
        if self.chat_display is not None:
            users = fetch_users()
            if users is None:
                raise RuntimeError("No users found!")

            user = next((row for row in users if row[2] == str(uuid)), None)

            if user is not None:
                self.chat_display.configure(state="normal")
                self.chat_display.insert("end", f"Selected user: {user[1]}\n")
                self.chat_display.configure(state="disabled")
            else:
                self.chat_display.configure(state="normal")
                self.chat_display.insert("end", "No such user\n")
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
                self.chat_display.insert("end", f"You: {message}\n")
                self.chat_display.configure(state="disabled")
                self.message_entry.delete(0, "end")
                send(self.selected_user, message)


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

        users = get_all_users() or []
        user = next((u for u in users if u[1].lower() == username.lower()), None)
        if user:
            self.feedback_label.configure(text="Login successful!", text_color="green")
            self.after(500, self.on_success)
            Session.set_user_details(user)
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
