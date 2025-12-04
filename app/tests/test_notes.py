"""
File contains tests for notes file.
"""

import pytest
from unittest.mock import patch
from datetime import datetime

from app.backend.database import Db
from app.backend.notes import Note, NoteManager, initiate_note_manager


def test_note_creation_defaults() -> None:
    """
    Tests creating a Note object with default color and no associated_date.
    :return: Nothing, only provides test.
    """
    note = Note(id=1, user_id=10, title="Test", content="Content")
    assert note.id == 1
    assert note.user_id == 10
    assert note.title == "Test"
    assert note.content == "Content"
    assert note.associated_date is None
    assert note.color in ["#ada132", "#2d7523", "#1e6a6e"]
    datetime.strptime(note.created_at, "%Y-%m-%d %H:%M")


def test_note_creation_custom_color_and_date() -> None:
    """
    Tests creating a Note object with custom color and associated_date.
    :return: Nothing, only provides test.
    """
    now = datetime(2025, 1, 1, 12, 0)
    note = Note(id=2, user_id=5, title="Title", content="Content", color="#ffffff", associated_date=now)
    assert note.color == "#ffffff"
    assert note.associated_date == now


def test_note_update_methods() -> None:
    """
    Tests update_title, update_content and update_user_id methods of Note.
    :return: Nothing, only provides test.
    """
    note = Note(id=0, user_id=1, title="Old", content="Old content")
    note.update_title("New Title")
    note.update_content("New Content")
    note.update_user_id(42)
    assert note.title == "New Title"
    assert note.content == "New Content"
    assert note.user_id == 42


def test_note_manager_fill_and_get_all_notes() -> None:
    """
    Tests NoteManager initialization and get_all_notes method.
    :return: Nothing, only provides test.
    """
    notes_data = [
        (1, "Title1", "Content1", "2025-01-01 10:00", 10),
        (2, "Title2", "Content2", "2025-01-02 11:00", 20),
    ]
    manager = NoteManager(notes_data)
    all_notes = manager.get_all_notes()
    assert len(all_notes) == 2
    assert all_notes[0].title == "Title1"
    assert all_notes[1].user_id == 20


@pytest.fixture
def mock_fetch_notes():
    """
    Fixture that mocks fetch_notes function to provide controlled database output.
    :return: yields the patch object
    """
    with patch.object(Db, "fetch_notes") as mock:
        yield mock


def test_initiate_note_manager_success(mock_fetch_notes) -> None:
    """
    Tests initiate_note_manager returns NoteManager when fetch_notes returns valid data.
    :param mock_fetch_notes: mocked fetch_notes function.
    :return: Nothing, only provides test.
    """
    mock_fetch_notes.return_value = [(1, "Title", "Content", "2025-01-01 10:00", 10)]
    manager = initiate_note_manager()
    assert manager is not None
    assert isinstance(manager, NoteManager)
    assert manager.get_all_notes()[0].title == "Title"


def test_initiate_note_manager_empty_list(mock_fetch_notes) -> None:
    """
    Tests initiate_note_manager returns None when fetch_notes returns empty list.
    :param mock_fetch_notes: mocked fetch_notes function.
    :return: Nothing, only provides test.
    """
    mock_fetch_notes.return_value = []
    manager = initiate_note_manager()
    assert manager is None


def test_initiate_note_manager_invalid_structure(mock_fetch_notes) -> None:
    """
    Tests initiate_note_manager returns None for invalid tuple structure.
    :param mock_fetch_notes: mocked fetch_notes function.
    :return: Nothing, only provides test.
    """
    mock_fetch_notes.return_value = [(1, "Title", "Content")]
    manager = initiate_note_manager()
    assert manager is None


def test_initiate_note_manager_type_error(mock_fetch_notes) -> None:
    """
    Tests initiate_note_manager handles TypeError and returns None.
    :param mock_fetch_notes: mocked fetch_notes function.
    :return: Nothing, only provides test.
    """
    mock_fetch_notes.side_effect = TypeError("Database error")
    manager = initiate_note_manager()
    assert manager is None


@pytest.mark.parametrize("note_id", range(6))
def test_note_colors_cycling(note_id) -> None:
    """
    Tests that Note colors are cycled properly based on id.
    :param note_id: ID of the note to test color cycling.
    :return: Nothing, only provides test.
    """
    colors = ["#ada132", "#2d7523", "#1e6a6e"]
    note = Note(id=note_id, user_id=0, title="T", content="C")
    assert note.color == colors[note_id % len(colors)]
