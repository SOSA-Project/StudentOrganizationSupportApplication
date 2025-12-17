"""
This file contains views for all widgets.
"""

import random
import calendar
import json
import pyperclip
from gc import collect
from typing import Callable
from datetime import datetime
from abc import ABC, abstractmethod
from CTkListbox import CTkListbox

import customtkinter as ctk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from app.backend.grade_monitor import initiate_grade_monitor, GradeMonitor
from app.backend.charts import (
    StatisticsManager,
    subjects_averages_histogram_plot,
    all_grades_histogram_plot,
    all_grades_pie_plot,
)
from app.backend.database import Db
from app.backend.notifications import initiate_notification_manager, NotificationType, Notification
from app.backend.registration import Auth, get_all_users
from app.backend.notes import initiate_note_manager
from app.backend.notes import Note
from app.backend.tooltip import Tooltip
from app.backend.chat import Client, Server
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
        :return: Nothing
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

        footer_frame = ctk.CTkFrame(self)
        footer_frame.pack(pady=5, padx=20)

        share_btn = ctk.CTkButton(
            footer_frame, text="Share", width=40, command=lambda: pyperclip.copy(self.calendar_to_json())
        )
        share_btn.pack(side="right", padx=(5, 10), pady=10)

        paste_btn = ctk.CTkButton(
            footer_frame,
            text="Paste",
            width=40,
            command=lambda: self.update_calendar(self.json_to_notes(pyperclip.paste())),
        )
        paste_btn.pack(side="left", padx=(10, 5), pady=10)

        self.update_calendar()

    def update_calendar(self, notes: list[Note] | None = None) -> None:
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

        current_notes: list[Note]
        if notes is None or len(notes) <= 0:
            current_notes = self.get_notes_for_current_month()
        else:
            current_notes = notes

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

    def calendar_to_json(self) -> str:
        """
        Converts current calendar month information to json format for sharing
        :return: String containing data converter to json format
        """
        notes = self.get_notes_for_current_month()
        calendar_data = {
            "identifier": "SOSA",
            "year": self.current_date.year,
            "month": self.current_date.month,
            "notes": [
                {
                    "associated_date": (
                        note.associated_date.strftime("%Y-%m-%d %H:%M:%S") if note.associated_date is not None else None
                    ),
                    "content": note.content,
                    "color": note.color,
                    "title": note.title,
                }
                for note in notes
            ],
        }
        return json.dumps(calendar_data)

    def json_to_notes(self, json_data: str) -> list[Note] | None:
        """
        Converts json formatted data of a calendar month back to usable format
        :param json_data: json data string containing calendar information
        :return: List of notes retrieved from json data string or None if a wrong format is read
        """
        try:
            data = json.loads(json_data)
            year = data["year"]
            month = data["month"]
            notes = [
                Note(
                    0,
                    0,
                    note["title"],
                    note["content"],
                    note["color"],
                    (
                        datetime.strptime(note["associated_date"], "%Y-%m-%d %H:%M:%S")
                        if note["associated_date"] != "None"
                        else None
                    ),
                )
                for note in data["notes"]
            ]
            self.current_date = self.current_date.replace(year=year + 1, month=month)
            return notes
        except Exception:
            return None


class NotificationsView(BaseView):
    """
    View for notifications widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.notification_manager = initiate_notification_manager()
        self.create_frame_content()

    def create_frame_content(self) -> None:
        """
        This method creates elements visible on the frame.
        :return: Nothing
        """

        label_one: ctk.CTkLabel = ctk.CTkLabel(self, text="Notifications", font=("Roboto", 18))
        label_one.grid(row=2, column=3, columnspan=2, rowspan=4, pady=10)

        notification_types = [nt.name for nt in NotificationType]
        notification_types.insert(0, "-")
        self.notifications_types_filter = ctk.CTkOptionMenu(self, values=notification_types, height=50, width=150)
        self.notifications_types_filter.grid(row=6, column=3, rowspan=4, columnspan=2)

        self.notifications_listbox = CTkListbox(self, height=350, width=750, fg_color="#242424")
        self.notifications_listbox.grid(row=13, column=1, columnspan=6, rowspan=12)

        mark_as_read_button = ctk.CTkButton(self, text="Mark as Read", command=self.mark_as_read, height=50, width=150)
        mark_as_read_button.grid(row=26, column=2, pady=10, rowspan=4)

        filter_button = ctk.CTkButton(self, text="Filter", command=self.filter_notifications, height=50, width=150)
        filter_button.grid(row=26, column=5, pady=10, rowspan=4)

        self.populate_notifications()

    def populate_notifications(self, type_filter: str | None = None) -> None:
        """
        Populates notifications list box with fetched notifications
        :return: Nothing
        """
        self.notifications_listbox.delete(0, ctk.END)

        if self.notification_manager is not None:
            notifications: list[Notification]
            notifications = self.notification_manager.get_all_notifications()
            if type_filter is not None and type_filter != "-":
                notifications = [n for n in notifications if n.notification_type.name == type_filter]

            for notification in notifications:
                notification_type = notification.notification_type.name
                is_read = "Read" if notification.is_read else "Unread"
                time = (
                    notification.associated_time.strftime("%Y-%m-%d %H:%M:%S")
                    if notification.associated_time
                    else "N/A"
                )
                item_text = f"[{notification_type}] {notification.message} - {time} - {is_read}"
                self.notifications_listbox.insert(ctk.END, item_text)

    def mark_as_read(self) -> None:
        """
        Marks a notification as read
        :return: Nothing
        """
        if self.notification_manager is not None:
            selected_index = self.notifications_listbox.curselection()
            if selected_index is not None:
                selected_notification = self.notification_manager.get_all_notifications()[selected_index]
                selected_notification.mark_as_read()
                self.populate_notifications()

    def filter_notifications(self) -> None:
        """
        Filters notifications by type
        :return: Nothing
        """
        self.populate_notifications(self.notifications_types_filter.get())


class NotesView(BaseView):
    """
    View for notes widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)

        self.menu_values = (
            "Show notes",
            "Add note",
            "Delete note",
            "Edit note",
        )

        self.note_id_data = self._update_options_data()

        self.labels_container: dict[str, ctk.CTkLabel] = {}
        self.options_container: dict[str, ctk.CTkOptionMenu] = {}

        self.create_frame_content()

        self.note_views = {
            "show_notes": self.show_notes_gui(),
            "add_note": self.add_note_gui(),
            "delete_note": self.delete_note_gui(),
            "edit_note": self.edit_note_gui(),
        }

        self.show_view(self.note_views["edit_note"])
        self.show_view(self.note_views["show_notes"])

    def _get_separator_line(self) -> str:
        """
        Method generates separator line for separate line
        :return: Nothing
        """
        self.update_idletasks()

        try:
            real_widget = self.notes_textbox._textbox
        except AttributeError:
            real_widget = self.notes_textbox

        width_px = real_widget.winfo_width()

        if width_px <= 1:
            width_px = real_widget.winfo_reqwidth()

        try:
            font_spec = real_widget.cget("font")
            font = tkFont.Font(font=font_spec)
        except Exception:
            font = tkFont.Font(family="Consolas", size=16)

        dash_width = font.measure("-") or 10

        width_px = max(1, width_px - 12)

        count = max(1, int(width_px // dash_width))

        return "-" * count

    @classmethod
    def _update_options_data(cls) -> tuple[str, ...]:
        """
        Support method updates data after change.
        :return: updated data.
        """
        notes = Db.fetch_notes()
        return tuple(str(n[0]) for n in notes) if notes else ("None",)

    def _prepare_data_for_db(self) -> dict[str, str | int]:
        """
        Method prepares data for db view.
        :return:
        """
        data: dict[str, str | int] = {}

        if hasattr(self, "add_note_title_input"):
            data["title_add"] = str(self.add_note_title_input.get())
            data["content_add"] = self.add_note_content_input.get("1.0", "end").rstrip("\n")
        if hasattr(self, "edit_note_id_optionmenu"):
            data["id_edit"] = str(self.edit_note_id_optionmenu.get())
            data["title_edit"] = str(self.edit_note_title_input.get())
            data["content_edit"] = self.edit_note_content_input.get("1.0", "end").rstrip("\n")
        if hasattr(self, "note_id_optionmenu"):
            data["id_del"] = str(self.note_id_optionmenu.get())
        return data

    def change_gui(self, _=None) -> None:
        """
        Method that is responsible for changing GUIs.
        :param _: temp param for get().
        :return: Nothing
        """
        button_value = self.menu_button.get()

        match button_value:
            case "Show notes":
                self.refresh_notes_table()
                self.show_view(self.note_views["show_notes"])
                self.menu_label.configure(text="Notes")
            case "Add note":
                self.show_view(self.note_views["add_note"])
                self.menu_label.configure(text="")
            case "Delete note":
                self.note_id_data = self._update_options_data()
                if hasattr(self, "note_id_optionmenu"):
                    self.note_id_optionmenu.configure(values=self.note_id_data)
                self.show_view(self.note_views["delete_note"])
                self.menu_label.configure(text="")
            case "Edit note":
                self.note_id_data = self._update_options_data()
                if hasattr(self, "edit_note_id_optionmenu"):
                    self.edit_note_id_optionmenu.configure(values=self.note_id_data)
                self.show_view(self.note_views["edit_note"])
                self.menu_label.configure(text="")

    def add_note(self) -> None:
        """
        Method adds new note.
        :return: Nothing
        """
        data = self._prepare_data_for_db()
        title = str(data.get("title_add", "")).strip()
        content = str(data.get("content_add", "")).strip()
        if not title and not content:
            self.menu_label.configure(text="Title or content required")
            return
        created_at = datetime.now().isoformat()
        temp_user_id: int = 1

        succes = Db.insert_note(title=title, content=content, created_at=created_at, user_id=temp_user_id)
        if succes:
            self.note_id_data = self._update_options_data()
            if hasattr(self, "note_id_optionmenu"):
                self.note_id_optionmenu.configure(values=self.note_id_data)
            if hasattr(self, "edit_note_id_optionmenu"):
                self.edit_note_id_optionmenu.configure(values=self.note_id_data)
            self.refresh_notes_table()
            self.menu_label.configure(text="Note has been added")
            self.add_note_title_input.delete(0, "end")
            self.add_note_content_input.delete(1.0, "end")
        else:
            self.menu_label.configure(text="Failed to add note")

    def edit_note(self) -> None:
        """
        Method edits note.
        :return: Nothing
        """
        data = self._prepare_data_for_db()
        try:
            nid = int(data.get("id_edit", "0"))
        except Exception:
            self.menu_label.configure(text="Invalid ID")
            return
        title = str(data.get("title_edit", "")).strip()
        content = str(data.get("content_edit", "")).strip()
        if nid == 0:
            self.menu_label.configure(text="Select valid ID")
            return

        created_at = datetime.now().isoformat()
        temp_user_id = 1

        success = Db.update_note(note_id=nid, title=title, content=content, created_at=created_at, user_id=temp_user_id)
        if success:
            self.note_id_data = self._update_options_data()
            if hasattr(self, "note_id_optionmenu"):
                self.note_id_optionmenu.configure(values=self.note_id_data)
            if hasattr(self, "edit_note_id_optionmenu"):
                self.edit_note_id_optionmenu.configure(values=self.note_id_data)
            self.refresh_notes_table()
            self.menu_label.configure(text="Note has been edited")
        else:
            self.menu_label.configure(text="Failed to edit note")

    def delete_note(self) -> None:
        """
        Method deletes note.
        :return: Nothing
        """
        data = self._prepare_data_for_db()
        try:
            nid = int(data.get("id_del", "0"))
        except Exception:
            self.menu_label.configure(text="Invalid ID")
            return
        if nid == 0:
            self.menu_label.configure(text="Select valid ID")
            return

        success = Db.delete_note(note_id=nid)
        if success:
            self.note_id_data = self._update_options_data()
            if hasattr(self, "note_id_optionmenu"):
                self.note_id_optionmenu.configure(values=self.note_id_data)
            if hasattr(self, "edit_note_id_optionmenu"):
                self.edit_note_id_optionmenu.configure(values=self.note_id_data)
            self.refresh_notes_table()
            self.menu_label.configure(text="Note has been deleted")
        else:
            self.menu_label.configure(text="Failed to delete note")

    def add_note_gui(self) -> ctk.CTkFrame:
        """
        Method that creates GUI for adding new notes into database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        labels_data = {
            ("title_label", "Note title:", 10),
            ("content_label", "Note content:", 12),
        }

        for key, text, row in labels_data:
            label = ctk.CTkLabel(frame, text=text, font=("Roboto", 18))
            label.grid(row=row, rowspan=2, column=2, columnspan=2, padx=5, pady=5)
            setattr(self, key, label)

        self.add_note_title_input = ctk.CTkEntry(frame, width=250)
        self.add_note_title_input.grid(row=10, rowspan=2, column=4, columnspan=2, padx=5, pady=5, sticky="ew")

        self.add_note_content_input = ctk.CTkTextbox(frame, width=250, height=250)
        self.add_note_content_input.grid(row=12, rowspan=6, column=4, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.add_note_btn = ctk.CTkButton(
            frame,
            text="Add new note",
            font=("Roboto", 18),
            command=self.add_note,
        )
        self.add_note_btn.grid(row=26, rowspan=3, column=3, columnspan=2, padx=5, pady=5, sticky="nsew")

        return frame

    def get_note_ids(self) -> tuple[str, ...]:
        """
        This method gets note ids from database.
        :return: Tuple of note ids.
        """
        notes = Db.fetch_notes()
        if not notes:
            return ("None",)
        return tuple(str(note[0]) for note in notes)

    def edit_note_gui(self) -> ctk.CTkFrame:
        """
        This method creates GUI for editing existing notes into database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        labels_data = {
            ("note_id_label", "Select note ID:", 10),
            ("title_label", "Note title:", 12),
            ("content_label", "Note content:", 14),
        }

        for key, text, row in labels_data:
            label = ctk.CTkLabel(frame, text=text, font=("Roboto", 18))
            label.grid(row=row, rowspan=2, column=2, columnspan=2, padx=5, pady=5)
            setattr(self, key, label)

        self.edit_note_id_optionmenu = ctk.CTkOptionMenu(
            frame, values=self._update_options_data(), width=200, font=("Roboto", 18)
        )
        self.edit_note_id_optionmenu.grid(row=10, rowspan=2, column=4, columnspan=2, padx=5, pady=5)

        self.edit_note_title_input = ctk.CTkEntry(frame, width=250)
        self.edit_note_title_input.grid(row=12, rowspan=2, column=4, columnspan=2, padx=5, pady=5, sticky="ew")

        self.edit_note_content_input = ctk.CTkTextbox(frame, width=250, height=250)
        self.edit_note_content_input.grid(row=14, rowspan=6, column=4, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.save_note_btn = ctk.CTkButton(
            frame,
            text="Edit Note",
            font=("Roboto", 18),
            command=self.edit_note,
        )
        self.save_note_btn.grid(row=26, rowspan=3, column=3, columnspan=2, padx=5, pady=5, sticky="nsew")

        return frame

    def delete_note_gui(self) -> ctk.CTkFrame:
        """
        This method creates GUI for deleting notes from database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        label = ctk.CTkLabel(frame, text="Select note ID:", font=("Roboto", 18))
        label.grid(row=10, rowspan=2, column=2, columnspan=2, padx=5, pady=5)

        self.note_id_optionmenu = ctk.CTkOptionMenu(
            frame, values=self._update_options_data(), width=200, font=("Roboto", 18)
        )
        self.note_id_optionmenu.grid(row=10, rowspan=2, column=4, columnspan=2, padx=5, pady=5)

        self.delete_note_btn = ctk.CTkButton(
            frame,
            text="Delete Note",
            font=("Roboto", 18),
            command=self.delete_note,
        )
        self.delete_note_btn.grid(row=26, rowspan=3, column=3, columnspan=2, padx=5, pady=5, sticky="nsew")

        return frame

    def _on_textbox_resize(self, event=None) -> None:
        """
        This method is called when the text box is resized.
        :param event: Object automatically passed by the bind
        :return: Nothing
        """
        self.refresh_notes_table()

    def show_notes_gui(self) -> ctk.CTkFrame:
        """
        Method that creates GUI for showing grades in database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.notes_textbox = ctk.CTkTextbox(frame, font=("Consolas", 16), fg_color="#242424")
        self.notes_textbox.bind("<Configure>", self._on_textbox_resize)
        try:
            self.notes_textbox._textbox.bind("<Configure>", self._on_textbox_resize)
        except AttributeError:
            pass
        self.notes_textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.notes_textbox.configure(state="disabled")

        self.refresh_notes_table()
        return frame

    def refresh_notes_table(self) -> None:
        """
        This method creates table for showing grades in database.
        :return: Nothing.
        """
        notes = Db.fetch_notes()

        if not hasattr(self, "notes_textbox"):
            return

        try:
            self.update_idletasks()
        except Exception:
            pass

        separator = self._get_separator_line()

        self.notes_textbox.configure(state="normal")
        self.notes_textbox.delete("1.0", "end")

        if not notes:
            self.notes_textbox.insert("end", "No notes available\n")
        else:
            for note in notes:
                note_id, title, content = note[:3]
                self.notes_textbox.insert("end", f"ID: {note_id}\n")
                self.notes_textbox.insert("end", f"Title: {title}\n")
                self.notes_textbox.insert("end", f"Content:\n{content}\n")
                self.notes_textbox.insert("end", separator + "\n")

        self.notes_textbox.configure(state="disabled")

    def create_frame_content(self) -> None:
        """
        This method creates constant GUI content.
        :return: Nothing.
        """
        self.menu_button = ctk.CTkSegmentedButton(
            self,
            values=self.menu_values,
            font=("Roboto", 14.5),
            command=self.change_gui,
            height=50,
            corner_radius=10,
            fg_color="#242424",
            border_width=5,
        )

        self.menu_button.grid(row=2, rowspan=2, column=2, columnspan=4, padx=0, pady=0)
        self.menu_button.set(self.menu_values[0])

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
        self.menu_values: tuple[str, ...] = ("Average", "Histogram", "Pie Chart")
        subjects = Db.fetch_subjects()
        self.subject_data = tuple(subject[1] for subject in subjects) if subjects else ("None",)
        self.create_frame_content()

    def update_subject_data(self, new_subjects: tuple[str, ...]) -> None:
        """
        This method is responsible for updating option menu values.
        :param new_subjects: updated subjects data.
        :return: Nothing, only update data.
        """
        self.subject_data = new_subjects

        if hasattr(self, "menu_label") and hasattr(self, "subject_name_option"):
            self.subject_name_option: ctk.CTkOptionMenu
            self.subject_name_option.grid_forget()
            self.subject_name_option.destroy()

            self.subject_name_option = ctk.CTkOptionMenu(
                self.menu_label, values=self.subject_data, width=150, font=("Roboto", 18), command=self.change_gui
            )
            self.subject_name_option.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

            if self.subject_data:
                self.subject_name_option.set(self.subject_data[0])

    @classmethod
    def _create_avg_chart(cls, monitor: GradeMonitor) -> Figure:
        """
        This method creates new chart based on provided data.
        :param monitor: data about grades.
        :return: New chart.
        """
        charts_manager = StatisticsManager(monitor)
        grades_avg = charts_manager.subjects_averages()
        return subjects_averages_histogram_plot(grades_avg, "dark")

    @classmethod
    def _create_grades_pie_plot(cls, grades_data: GradeMonitor, subject: list[str]) -> Figure:
        """
        This method creates new chart based on provided data.
        :param grades_data: data about grades.
        :param subject: subject name.
        :return: New chart.
        """
        charts_manager = StatisticsManager(grades_data)
        grades_number: dict[float, int] = charts_manager.grades_number(subject)
        return all_grades_pie_plot(grades_number, "dark")

    @classmethod
    def _create_grades_histogram(cls, grades_data: GradeMonitor, subject: list[str]) -> Figure:
        """
        This method creates new chart based on provided data.
        :param grades_data: data about grades.
        :param subject: subject name.
        :return: New chart.
        """
        charts_manager = StatisticsManager(grades_data)
        grades_number: dict[float, int] = charts_manager.grades_number(subject)
        return all_grades_histogram_plot(grades_number, "dark")

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

    def _create_chart_content(self, chart: Figure) -> None:
        """
        This method creates GUI content.
        :param chart: chart to display.
        :return: Nothing, only creates GUI content.
        """
        self.canvas = FigureCanvasTkAgg(chart, master=self)
        self.canvas.draw()

        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(bg=self.cget("fg_color"), highlightthickness=0, bd=0)
        canvas_widget.grid(row=5, rowspan=27, column=0, columnspan=8, padx=5, pady=5, sticky="nsew")

    def avg_chart_gui(self) -> None:
        """
        This method creates avg histogram chart.
        :return: Nothing, only creates GUI content
        """
        if (grades_data := initiate_grade_monitor()) is None:
            return

        chart: Figure = self._create_avg_chart(grades_data)
        self._create_chart_content(chart)

    def histogram_grades_gui(self, subject: list[str]) -> None:
        """
        This method creates histogram chart.
        :param subject: subject name.
        :return: Nothing, only creates GUI content
        """
        if (grades_data := initiate_grade_monitor()) is None:
            return

        chart: Figure = self._create_grades_histogram(grades_data, subject)
        self._create_chart_content(chart)

    def pie_grades_gui(self, subject: list[str]) -> None:
        """
        This method creates pie chart.
        :param subject: subject name.
        :return: Nothing, only creates GUI content
        """
        if (grades_data := initiate_grade_monitor()) is None:
            return

        chart: Figure = self._create_grades_pie_plot(grades_data, subject)
        self._create_chart_content(chart)

    def change_gui(self, _=None) -> None:
        """
        This method is responsible for changing GUIs.
        :param _: temp param for get().
        :return: Nothing, only changes windows.
        """
        button_value = self.menu_button.get()
        self._destroy_old_canvas()

        match button_value:
            case "Average":
                self.avg_chart_gui()
            case "Histogram":
                option_value = self.subject_name_option.get()
                self.subject_name_option.configure(values=self.subject_data)
                print(self.subject_data)
                self.histogram_grades_gui(option_value)
            case "Pie Chart":
                option_value = self.subject_name_option.get()
                self.subject_name_option.configure(values=self.subject_data)
                print(self.subject_data)
                self.pie_grades_gui(option_value)

    def create_frame_content(self) -> ctk.CTkFrame:
        """
        This method creates elements visible on the frame.
        :return: new ctk frame.
        """
        self.menu_button = ctk.CTkSegmentedButton(
            self,
            values=self.menu_values,
            font=("Roboto", 24),
            command=self.change_gui,
            height=60,
            corner_radius=10,
            fg_color="#242424",
            border_width=5,
        )
        self.menu_button.grid(row=2, rowspan=2, column=1, columnspan=4, padx=1, pady=20, sticky="ew")
        self.menu_button.set(self.menu_values[0])

        self.menu_label = ctk.CTkLabel(
            self,
            text="",
            font=("Roboto", 24),
            height=60,
            corner_radius=10,
            fg_color="#242424",
        )
        self.menu_label.grid(row=2, rowspan=2, column=5, columnspan=2, padx=1, pady=20, sticky="ew")

        self.subject_name_option = ctk.CTkOptionMenu(
            self.menu_label, values=self.subject_data, width=150, font=("Roboto", 18), command=self.change_gui
        )
        self.subject_name_option.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        self.change_gui()

    def refresh(self) -> None:
        """
        Method refresh chart.
        :return: Nothing, only refresh chart
        """
        self.create_frame_content()


class GradesView(BaseView):
    """
    View for grades.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.average_view = AverageView(parent=self)

        self.menu_values = (
            "Show grades",
            "Add grade",
            "Edit grade",
            "Delete grade",
            "Add subject",
            "Edit subject",
            "Delete subject",
        )
        self.grades = ("1", "2", "3", "3.5", "4", "4.5", "5", "6")
        self.grade_weight_sem = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.subject_ects_values = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.grade_types = ("Lecture", "Laboratory", "Exercise", "Seminar")

        self.subject_data, self.grades_id_data = self._update_options_data()
        self.subject_id_data = self._update_options_data_sub()
        self.labels_container: dict[str, ctk.CTkLabel] = {}
        self.options_container: dict[str, ctk.CTkOptionMenu] = {}

        self.create_frame_content()

        self.grade_views = {
            "add_view": self.add_new_grade_gui(),
            "delete_view": self.delete_grade_gui(),
            "edit_view": self.edit_grade_gui(),
            "show_grades": self.show_grades_gui(),
        }

        self.subject_views = {
            "add_view": self.add_subject_gui(),
            "delete_view": self.delete_subject_gui(),
            "edit_view": self.edit_subject_gui(),
        }

        self.show_view(self.grade_views["edit_view"])
        self.show_view(self.grade_views["show_grades"])

    def _prepare_data_for_db(self) -> dict[str, int | str]:
        """
        Support method prepare data from database for option menus.
        :return: prepared data.
        """
        type_convert = {"Lecture": 1, "Laboratory": 2, "Exercise": 3, "Seminar": 4}
        subjects_convert = {name: sub_id for sub_id, name, ect in tuple(Db.fetch_subjects() or [])}
        option_data: dict[str, int | str] = {}

        for data in self.options_container.items():
            option_data[data[0]] = str(data[1].get())

        option_data["type_add"] = type_convert[str(option_data["type_add"])]
        option_data["type_edit"] = type_convert[str(option_data["type_edit"])]
        option_data["subject_add"] = subjects_convert[str(option_data["subject_add"])]
        option_data["subject_edit"] = subjects_convert[str(option_data["subject_edit"])]
        return option_data

    @classmethod
    def _update_options_data(cls) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """
        Support method updates data after change.
        :return: updated data.
        """
        subjects = Db.fetch_subjects()
        subject_data = tuple(subject[1] for subject in subjects) if subjects else ("None",)
        grades_id = Db.fetch_grades_id()
        grades_id_data = tuple(str(g_id[0]) for g_id in grades_id) if grades_id else ("None",)
        return subject_data, grades_id_data

    @classmethod
    def _update_options_data_sub(cls) -> tuple[str, ...]:
        """
        Support method updates data after change.
        :return: updated data.
        """
        subjects = Db.fetch_subjects()
        subjects_id_data = tuple(str(subject[0]) for subject in subjects) if subjects else ("None",)
        return subjects_id_data

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

    def _display_labels_elements(self, labels_data, parent) -> None:
        """
        Support method for displaying GUI content.
        :param labels_data: data about labels.
        :param parent: main frame.
        :return: Nothing, only create GUI content.
        """
        for l_key, l_text, l_row in labels_data:
            self.labels_container[l_key] = ctk.CTkLabel(parent, text=l_text, font=("Roboto", 18))
            self.labels_container[l_key].grid(row=l_row, rowspan=2, column=2, columnspan=2, padx=5, pady=5)

    def _display_options_elements(self, options_data, parent) -> None:
        """
        Support method for displaying GUI content.
        :param options_data: data about options.
        :param parent: main frame.
        :return: Nothing, only create GUI content.
        """
        for o_key, o_value, o_row in options_data:
            self.options_container[o_key] = ctk.CTkOptionMenu(parent, values=o_value, width=200, font=("Roboto", 18))
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
            case "Add grade":
                self.refresh_options_in_frame("add_view")
                self.show_view(self.grade_views["add_view"])
                self.menu_label.configure(text="")
            case "Edit grade":
                self.refresh_options_in_frame("edit_view")
                self.show_view(self.grade_views["edit_view"])
                self.menu_label.configure(text="")
            case "Delete grade":
                self.refresh_options_in_frame("delete_view")
                self.show_view(self.grade_views["delete_view"])
                self.menu_label.configure(text="")
            case "Show grades":
                self.refresh_grades_table()
                self.show_view(self.grade_views["show_grades"])
                self.menu_label.configure(text="Student grades")
            case "Add subject":
                self.show_view(self.subject_views["add_view"])
                self.menu_label.configure(text="")
            case "Edit subject":
                self.show_view(self.subject_views["edit_view"])
                self.menu_label.configure(text="")
            case "Delete subject":
                self.show_view(self.subject_views["delete_view"])
                self.menu_label.configure(text="")

    def add_grade(self) -> None:
        """
        This method adds new grades into database.
        :return: Nothing, only adds grades into database.
        """
        option_data: dict[str, int | str] = self._prepare_data_for_db()
        temp_user_id: int = 1

        Db.insert_grade(
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

        Db.update_grade(
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
        Method removes the selected rating from the database.
        :return: Nothing.
        """
        option_data: dict[str, int | str] = self._prepare_data_for_db()
        Db.delete_grade(grade_id=int(option_data["id_del"]))

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

    def add_subject(self) -> None:
        """
        This method is responsible for adding new subject into database.
        :return: Nothing, only adds subject into database.
        """
        option_data: dict[str, int | str] = self._prepare_data_for_db()
        subject_name = self.subject_name_input_add.get()

        Db.insert_subject(name=str(subject_name), ects=int(option_data["add_sub_ects"]))

        self.subject_data, self.grades_id_data = self._update_options_data()
        self.subject_id_data = self._update_options_data_sub()
        self.delete_subject_option_menu.configure(values=self.subject_id_data)
        self.sub_id_data_option_menu.configure(values=self.subject_id_data)
        self.average_view.update_subject_data(self.subject_data)
        self.menu_label.configure(text="New subject has been added")

    def edit_subject(self) -> None:
        """
        This method is responsible for update existing subject in database.
        :return: Nothing, only update subject.
        """
        option_data: dict[str, int | str] = self._prepare_data_for_db()
        subject_name = self.subject_name_input_edit.get()

        Db.update_subject(
            subject_id=int(option_data["sub_id_option_edit"]),
            name=str(subject_name),
            ects=int(option_data["sub_ects_option_edit"]),
        )

        self.subject_data, self.grades_id_data = self._update_options_data()
        self.subject_id_data = self._update_options_data_sub()
        self.delete_subject_option_menu.configure(values=self.subject_id_data)
        self.sub_id_data_option_menu.configure(values=self.subject_id_data)
        self.average_view.update_subject_data(self.subject_data)
        self.menu_label.configure(text="Subject has been updated")

    def delete_subject(self) -> None:
        """
        This method is responsible for delete selected subject from database.
        :return: Nothing, only delete subject.
        """
        option_data: dict[str, int | str] = self._prepare_data_for_db()

        Db.delete_subject(subject_id=int(option_data["sub_id_option_delete"]))

        self.subject_data, self.grades_id_data = self._update_options_data()
        self.subject_id_data = self._update_options_data_sub()
        self.delete_subject_option_menu.configure(values=self.subject_id_data)
        self.sub_id_data_option_menu.configure(values=self.subject_id_data)
        self.average_view.update_subject_data(self.subject_data)
        self.menu_label.configure(text="Subject has been deleted")

    def add_subject_gui(self) -> ctk.CTkFrame:
        """
        This method creates GUI for adding new subjects into database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        labels_data = {("sub_name_add", "Subject name:", 13), ("sub_ects", "Subject ECTS:", 15)}

        option_data = {("add_sub_ects", self.subject_ects_values, 15)}

        self.subject_name_input_add = ctk.CTkEntry(frame, width=200, placeholder_text="subject name")
        self.subject_name_input_add.grid(row=13, rowspan=2, column=4, columnspan=2, padx=5, pady=5)

        self._display_labels_elements(labels_data, frame)
        self._display_options_elements(option_data, frame)

        self.add_subject_btn = ctk.CTkButton(
            frame, text="Add new subject", font=("Roboto", 18), command=self.add_subject
        )
        self.add_subject_btn.grid(row=26, rowspan=3, column=3, columnspan=2, padx=(30, 5), pady=5, sticky="nsew")

        return frame

    def edit_subject_gui(self) -> ctk.CTkFrame:
        """
        This method creates GUI for editing current subjects in database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        labels_data = {
            ("sub_id_edit", "Current subject ID:", 10),
            ("sub_name_edit", "Subject name:", 12),
            ("sub_ects_edit", "Subject ECTS", 14),
        }

        option_data = {
            ("sub_id_option_edit", self.subject_id_data, 10),
            ("sub_ects_option_edit", self.subject_ects_values, 15),
        }

        self.subject_name_input_edit = ctk.CTkEntry(frame, width=200, placeholder_text="subject name")
        self.subject_name_input_edit.grid(row=13, rowspan=2, column=4, columnspan=2, padx=5, pady=5)

        self._display_labels_elements(labels_data, frame)
        self._display_options_elements(option_data, frame)

        self.sub_id_data_option_menu = self.options_container["sub_id_option_edit"]
        self.edit_subject_btn = ctk.CTkButton(
            frame, text="Edit subject", font=("Roboto", 18), command=self.edit_subject
        )
        self.edit_subject_btn.grid(row=26, rowspan=3, column=3, columnspan=2, padx=(30, 5), pady=5, sticky="nsew")

        return frame

    def delete_subject_gui(self) -> ctk.CTkFrame:
        """
        This method creates GUI for deleting existing subjects from database.
        :return: New CTK frame.
        """
        frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=10)
        frame.grid_rowconfigure(tuple(range(32)), weight=1, uniform="rowcol")
        frame.grid_columnconfigure(tuple(range(8)), weight=1, uniform="rowcol")

        labels_data = {("sub_id_delete", "Current subject ID:", 14)}

        option_data = {("sub_id_option_delete", self.subject_id_data, 14)}

        self._display_labels_elements(labels_data, frame)
        self._display_options_elements(option_data, frame)
        self.delete_subject_option_menu = self.options_container["sub_id_option_delete"]

        self.delete_subject_btn = ctk.CTkButton(
            frame, text="Delete subject", font=("Roboto", 18), command=self.delete_subject
        )
        self.delete_subject_btn.grid(row=26, rowspan=3, column=3, columnspan=2, padx=(30, 5), pady=5, sticky="nsew")

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
        self.grades_textbox._textbox.tag_configure("center", justify="center")
        self.grades_textbox._textbox.tag_configure("right", justify="right")

        self.refresh_grades_table()
        self.menu_label.configure(text="Student grades")

        return frame

    def refresh_grades_table(self) -> None:
        """
        Method that fills the grades table.
        :return: Nothing
        """
        decode_grade_type = {1: "Lecture", 2: "Laboratory", 3: "Exercise", 4: "Seminar"}

        if not hasattr(self, "grades_textbox"):
            return

        grades_data = Db.fetch_grades()

        self.grades_textbox.configure(state="normal")
        self.grades_textbox.delete("1.0", "end")

        if not grades_data:
            self.grades_textbox.insert("end", "No grades available")
        else:
            headers: tuple[str, ...] = ("ID", "Value", "Subject", "ECTS", "Weight", "Type")
            self.grades_textbox.insert(
                "end",
                f"  {headers[0]:<6} {headers[1]:<8} "
                f"{headers[2]:<20} {headers[3]:<6} {headers[4]:<8} {headers[5]:<10}\n",
                ("center"),
            )
            self.grades_textbox.insert("end", "-" * 63 + "\n", ("center"))

            for g_value, s_name, s_ects, g_weight, g_type, g_id in grades_data:
                self.grades_textbox.insert(
                    "end",
                    f"  {g_id:<6} {g_value:<8} {s_name:<20} {s_ects:<6} "
                    f"{g_weight:<8} {decode_grade_type[int(g_type)]:<12}\n",
                    ("center"),
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
            font=("Roboto", 14.5),
            command=self.change_gui,
            height=50,
            corner_radius=10,
            fg_color="#242424",
            border_width=5,
        )
        self.menu_button.grid(row=2, rowspan=2, column=2, columnspan=4, padx=0, pady=0)
        self.menu_button.set(self.menu_values[0])

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
        self.users_listbox.grid_columnconfigure(0, weight=1)

        users = get_all_users()
        for i, user in enumerate(users or []):
            if user[0] == Session.id:
                continue
            user_button = ctk.CTkButton(
                self.users_listbox, text=user[1], font=("Roboto", 16), command=lambda u=user[2]: self.on_user_click(u)
            )
            user_button.grid(row=i, column=0, sticky="ew", padx=10, pady=2)

        self.chat_display = ctk.CTkTextbox(self, font=("Roboto", 14), wrap="word")
        self.chat_display.grid(row=0, rowspan=28, column=2, columnspan=6, sticky="nsew", padx=5, pady=5)
        self.chat_display.configure(state="disabled")

        Client.chat_display = self.chat_display

        self.message_entry = ctk.CTkEntry(self, placeholder_text="Type your message...", font=("Roboto", 14))
        self.message_entry.grid(row=28, rowspan=2, column=2, columnspan=5, sticky="ew", padx=5, pady=5)

        self.send_button = ctk.CTkButton(self, text="Send", font=("Roboto", 14), command=self.send_message)
        self.send_button.grid(row=28, rowspan=2, column=7, sticky="ew", padx=5, pady=5)

    def on_user_click(self, uuid: str) -> None:
        """
        Handles user button click.
        :param uuid: The uuid of the clicked user.
        :return: None
        """
        Db.dequeue_messages()
        self.selected_user = uuid
        if self.chat_display is not None:
            users = Db.fetch_users()
            if users is None:
                raise RuntimeError("No users found!")

            user = next((row for row in users if row[2] == str(uuid)), None)

            if user is not None:
                self.chat_display.configure(state="normal")
                self.chat_display.delete("1.0", "end")
                msgs = Db.fetch_messages() or []
                for msg in msgs:
                    if msg[2] == str(uuid):
                        if msg[3]:
                            self.chat_display.insert("end", f"{user[1]}: {msg[1]}\n")
                        else:
                            self.chat_display.insert("end", f"You: {msg[1]}\n")
                    pass
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
                Client.send(self.selected_user, message)
                Db.insert_message(message, self.selected_user, 0)


class SettingsView(BaseView):
    """
    View for settings widget.
    """

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(x=20, y=20, relwidth=0.95, relheight=0.95, anchor="nw")
        self.container.grid_rowconfigure(tuple(range(30)), weight=1)
        self.container.grid_columnconfigure(tuple(range(8)), weight=1)
        self.create_frame_content()

    def create_frame_content(self) -> None:
        """
        This method creates frame content.
        :return: Nothing, only creates frame content.
        """
        self.create_settings_content()
        self.create_theme_toggle()
        self.create_footer()

    def change_password(self) -> None:
        """
        Work in progress
        #TODO
        :return:
        """
        print("zmiana hasla")

    def create_settings_content(self) -> None:
        """
        This method is responsible for creating main settings frame and its content.
        :return: Nothing, only creates main frame.
        """
        self.settings_frame = ctk.CTkFrame(
            self.container,
            fg_color="#242424",
            corner_radius=10,
        )
        self.settings_frame.grid(
            row=7,
            rowspan=15,
            column=1,
            columnspan=6,
            pady=(5, 5),
            sticky="nsew",
        )
        self.settings_frame.grid_rowconfigure(tuple(range(20)), weight=1)
        self.settings_frame.grid_columnconfigure(tuple(range(6)), weight=1)

        self.old_password_entry = ctk.CTkEntry(
            master=self.settings_frame, placeholder_text="Old password", font=("Roboto", 18), corner_radius=8, show="*"
        )
        self.old_password_entry.grid(row=5, rowspan=1, column=1, columnspan=4, padx=10, pady=10, sticky="ew")

        self.new_password_entry = ctk.CTkEntry(
            master=self.settings_frame, placeholder_text="New password", font=("Roboto", 18), corner_radius=8, show="*"
        )
        self.new_password_entry.grid(row=7, rowspan=1, column=1, columnspan=4, padx=10, pady=10, sticky="ew")

        self.confirm_password_entry = ctk.CTkEntry(
            master=self.settings_frame,
            placeholder_text="Confirm password",
            font=("Roboto", 18),
            corner_radius=8,
            show="*",
        )
        self.confirm_password_entry.grid(row=9, rowspan=1, column=1, columnspan=4, padx=10, pady=10, sticky="ew")

        self.submit_button = ctk.CTkButton(
            master=self.settings_frame,
            text="Change password",
            corner_radius=8,
            height=60,
            font=("Roboto", 18),
            command=self.change_password,
        )
        self.submit_button.grid(row=11, rowspan=6, column=1, columnspan=4, padx=10, pady=10, sticky="ew")

    def create_theme_toggle(self) -> None:
        """
        This frame is responsible for creating frame for dark mode switch.
        :return: Nothing, only creates new frame.
        """
        self.theme_frame = ctk.CTkFrame(
            self.container,
            fg_color="#242424",
            corner_radius=10,
            height=100,
        )
        self.theme_frame.grid(
            row=1,
            rowspan=4,
            column=1,
            columnspan=6,
            pady=(5, 5),
            sticky="ew",
        )

        self.theme_frame.grid_columnconfigure(0, weight=1)
        self.theme_frame.grid_columnconfigure(1, weight=0)

        self.dark_mode_label = ctk.CTkLabel(
            self.theme_frame,
            text="Dark mode",
            font=("Roboto", 18),
            anchor="w",
        )
        self.dark_mode_label.grid(row=0, column=0, padx=20, sticky="w")

        self.dark_mode_var = ctk.BooleanVar(value=True)  # switch włączony na starcie

        self.dark_mode_switch = ctk.CTkSwitch(
            self.theme_frame,
            text="",
            command=self.toggle_dark_mode,
            variable=self.dark_mode_var,
            onvalue=True,
            offvalue=False,
        )
        self.dark_mode_switch.grid(row=0, column=1, padx=20, sticky="e")

        ctk.set_appearance_mode("dark")

    def toggle_dark_mode(self) -> None:
        """
        This method is responsible for change application theme.
        (Work in progress)
        #TODO
        :return:
        """
        if self.dark_mode_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def create_footer(self) -> None:
        """
        This method is responsible for creating bottom frame.
        :return: Nothing, only creates frame.
        """
        self.footer_label = ctk.CTkLabel(
            self.container,
            text="Settings",
            font=("Roboto", 24),
            height=50,
            corner_radius=10,
            fg_color="#242424",
        )
        self.footer_label.grid(
            row=25,
            rowspan=2,
            column=1,
            columnspan=6,
            pady=(5, 10),
            sticky="ew",
        )


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

        self.password_entry = ctk.CTkEntry(self.bg_frame, placeholder_text="Password", font=("Roboto", 18), show="*")
        self.password_entry.grid(row=5, column=2, columnspan=2, sticky="ew", padx=20)

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
        password = self.password_entry.get().strip()
        if not username:
            self.feedback_label.configure(text="Username cannot be empty!")
            return
        if not password:
            self.feedback_label.configure(text="Password cannot be empty!")
            return

        if Auth.login_user(username, password):
            self.feedback_label.configure(text="Login successful!", text_color="green")
            self.after(500, self.on_success)
            Client.thread.start()
            Server.thread.start()
        else:
            self.feedback_label.configure(text="Wrong login or password!")

    def register_user(self) -> None:
        """
        This method handles the registration process and displays messages.
        :return: None
        """

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username:
            self.feedback_label.configure(text="Username cannot be empty!")
            return
        if not password:
            self.feedback_label.configure(text="Password cannot be empty!")
            return

        if Auth.register_user(username, password):
            self.feedback_label.configure(text="Registration successful!", text_color="green")
            self.after(500, self.on_success)
        else:
            self.feedback_label.configure(text="User already exists or error!")
