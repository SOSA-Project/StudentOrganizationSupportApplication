"""
File contains definition of Note and NoteManager class
"""

from datetime import datetime

from app.backend.data_base import fetch_notes


class Note:
    """
    Class stores information about a Note
    """

    def __init__(
        self, id: int, user_id: int, title: str, content: str, color: str = "", associated_date: datetime | None = None
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.associated_date = associated_date
        if color == "":
            colors: list[str] = ["#ada132", "#2d7523", "#1e6a6e"]
            self.color = colors[id % len(colors)]
        else:
            self.color = color

    def update_title(self, new_title: str) -> None:
        """
        Updates the title of the note
        :param new_title: new title of the note
        :return: Nothing
        """
        self.title = new_title

    def update_content(self, new_content: str) -> None:
        """
        Updates the content of the note
        :param new_content: new content of the note
        :return: Nothing
        """
        self.content = new_content

    def update_user_id(self, new_user_id: int) -> None:
        """
        Updates the user_id of the note
        :param new_user_id: new user_id of the note
        :return: Nothing
        """
        self.user_id = new_user_id


class NoteManager:
    """
    Class responsible for managing notes fetched from the database.
    """

    def __init__(self, notes_list: list[tuple[int, str, str, str, int]]) -> None:
        self.notes: list[Note] = []
        self.fill_notes_table(notes_list)

    def fill_notes_table(self, notes_list: list[tuple[int, str, str, str, int]]) -> None:
        """
        Method that fills notes table with data fetched from the database.
        :param notes_list: List of tuples representing notes
        :return: Nothing
        """
        for row in notes_list:
            note_id, title, content, created_at, user_id = row
            note = Note(note_id, user_id, title, content)
            note.created_at = created_at
            self.notes.append(note)

    def get_all_notes(self) -> list[Note]:
        """
        Method that returns all notes.
        :return: List of Note objects
        """
        return self.notes


def initiate_note_manager() -> NoteManager | None:
    """
    Function that fetches data from the database, validates it, and returns a NoteManager instance.
    :return: An instance of NoteManager class or None
    """
    try:
        notes = fetch_notes()
        if not notes or not isinstance(notes, list):
            return None

        def valid_item(item: tuple) -> bool:
            expected_types = (int, str, str, str, int)
            if not isinstance(item, tuple) or len(item) != len(expected_types):
                return False
            return all(isinstance(x, t) for x, t in zip(item, expected_types))

        if all(valid_item(item) for item in notes):
            return NoteManager(notes)

        return None

    except TypeError:
        print("Notes could not be fetched from database")
        return None
