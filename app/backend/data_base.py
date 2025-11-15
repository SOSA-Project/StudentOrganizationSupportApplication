"""
The file creates a database and operates on it.
"""

import sqlite3
import os

db_path = "./app/data_base/db.sqlite3"


def connect_to_database() -> sqlite3.Connection:
    """
    The function checks whether the database exists, and if not, it creates it.
    :return sqlite3.Connection:
    """
    if os.path.exists(db_path):
        return sqlite3.connect(db_path)
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
               CREATE TABLE "grades" (
                    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                    "value"	REAL NOT NULL,
                    "weight"	REAL,
                    "type"	INTEGER NOT NULL,
                    "semester"	TEXT NOT NULL,
                    "subject_id"	INTEGER NOT NULL,
                    "user_id"	INTEGER NOT NULL
                )
               """
        )
        cursor.execute(
            """
            CREATE TABLE "notes" (
                "id"	INTEGER,
                "title"	TEXT,
                "content"	TEXT,
                "created_at"	TEXT,
                "user_id"	INTEGER,
                PRIMARY KEY("id")
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE "events" (
                "id"	INTEGER NOT NULL,
                "title"	TEXT NOT NULL,
                "description"	TEXT NOT NULL,
                "date"	TEXT NOT NULL,
                "user_id"	INTEGER NOT NULL,
                PRIMARY KEY("id")
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE "messages" (
                "id"	INTEGER NOT NULL,
                "content"	TEXT NOT NULL,
                "user_id"	INTEGER NOT NULL,
                PRIMARY KEY("id")
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE "users" (
                "id"	INTEGER NOT NULL,
                "name"	TEXT NOT NULL,
                "uuid"	TEXT NOT NULL,
                PRIMARY KEY("id")
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE "subjects" (
                "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                "name"	TEXT,
                "ects"	INTEGER
            )
            """
        )
        conn.commit()
        return conn


# region grades
def fetch_grades() -> list[tuple[float, str, int, float, int, int]] | None:
    """
    This function fetches the grades from the database.
    :return list of tuple: list of tuple representing grades
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                    SELECT g.value, s.name, s.ects, g.weight, g.type, g.id
                    FROM grades AS g JOIN subjects AS s ON g.subject_id = s.id
                       """
        )
        grades = cursor.fetchall()
        conn.commit()
        conn.close()
        return grades
    except Exception as e:
        print(e)
        return None


def fetch_grades_id() -> list[tuple[str]]:
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                    SELECT id FROM grades
                       """
        )
        grades = cursor.fetchall()
        conn.commit()
        conn.close()
        return grades
    except Exception as e:
        print(e)
        return None


def insert_grade(value: float, weight: float, sub_type: int, semester: int, subject_id: int, user_id: int) -> bool:
    """
    This function inserts grades into the database.
    :param value: grade value
    :param weight: grade weight
    :param sub_type: subject type
    :param semester: corresponding semester id
    :param subject_id: subject id
    :param user_id: user id
    :return success status: whether insert was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   INSERT INTO grades (value, weight, type, semester, subject_id, user_id)
                   VALUES (?, ?, ?, ?, ?, ?)
               """,
            (value, weight, sub_type, semester, subject_id, user_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error in insert_grade: {e}")
        return False


def update_grade(grade_id: int, value: float, weight: float, ects: int, semester_id: int) -> bool:
    """
    This function updates the grade in the database.
    :param grade_id: id of a grade to update
    :param value: new grade value
    :param weight: new grade weight
    :param ects: new ects points
    :param semester_id: new corresponding semester id
    :return success status: whether update was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   UPDATE grades
                   SET value       = ?,
                       weight      = ?,
                       ects        = ?,
                       semester_id = ?
                   WHERE id = ?
                   """,
            (value, weight, ects, semester_id, grade_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def delete_grade(grade_id: int) -> bool:
    """
    This function deletes the grade in the database.
    :param grade_id: id of a grade to delete
    :return success status: whether delete was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# endregion


# region notes
def fetch_notes() -> list[tuple[int, str, str, str, int]] | None:
    """
    This function fetches notes from the database.
    :return list of tuple: list of tuple representing notes
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes")
        notes = cursor.fetchall()
        conn.commit()
        conn.close()
        return notes
    except Exception as e:
        print(e)
        return None


def insert_note(title: str, content: str, created_at: str, user_id: int) -> bool:
    """
    This function inserts note into the database.
    :param title: note title
    :param content: note content
    :param created_at: note creation date
    :param user_id: user id
    :return success status: whether insert was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   INSERT INTO notes (title, content, created_at, user_id)
                   VALUES (?, ?, ?, ?)
                   """,
            (title, content, created_at, user_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def update_note(note_id: int, title: str, content: str, created_at: str, user_id: int) -> bool:
    """
    This function updates note in the database.
    :param note_id: id of a note to update
    :param title: note title
    :param content: note content
    :param created_at: note creation date
    :param user_id: user id
    :return success status: whether update was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   UPDATE notes
                   SET title      = ?,
                       content    = ?,
                       created_at = ?,
                       user_id    = ?
                   WHERE id       = ?
               """,
            (title, content, created_at, user_id, note_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def delete_note(note_id: int) -> bool:
    """
    This function deletes the note in the database.
    :param note_id: id of a note to delete
    :return success status: whether delete was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# endregion


# region subjects
def fetch_subjects() -> list[tuple[int, str, int]] | None:
    """
    This function fetches subjects from the database.
    :return list of tuple: list of tuple representing subjects
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects")
        subjects = cursor.fetchall()
        conn.commit()
        conn.close()
        return subjects
    except Exception as e:
        print(e)
        return None


def insert_subject(name: str, ects: int) -> bool:
    """
    This function inserts subject into the database.
    :param name: subject name
    :param ects: subject ects
    :return success status: whether insert was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   INSERT INTO subjects (name, ects)
                   VALUES (?, ?)
               """,
            (name, ects),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error in insert_subject: {e}")
        return False


def update_subject(subject_id: int, name: str, ects: int) -> bool:
    """
    This function updates subject in the database.
    :param name: subject name
    :param ects: subject ects
    :return success status: whether update was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   UPDATE subjects
                   SET name   = ?,
                       ects   = ?
                   WHERE id   = ?
               """,
            (name, ects, subject_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def delete_subject(subject_id: int) -> bool:
    """
    This function deletes the subject in the database.
    :param note_id: id of a subject to delete
    :return success status: whether delete was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# endregions


# region events
def fetch_events() -> list[tuple[int, str, str, str, int]] | None:
    """
    This function fetches events from the database.
    :return list of tuple: list of tuple representing events
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        conn.commit()
        conn.close()
        return events
    except Exception as e:
        print(e)
        return None


def insert_event(title: str, description: str, date: str, user_id: int) -> bool:
    """
    This function inserts event into the database.
    :param title: event title
    :param description: event description
    :param date: event date
    :param event_id: user id
    :return success status: whether insert was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   INSERT INTO events (title, description, date, user_id)
                   VALUES (?, ?, ?, ?)
               """,
            (title, description, date, user_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def update_event(title: str, description: str, date: str, event_id: int) -> bool:
    """
    This function updates event in the database.
    :param title: event title
    :param description: event description
    :param date: event date
    :param event_id: user id
    :return success status: whether update was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   UPDATE events
                   SET title       = ?,
                       description = ?,
                       date        = ?,
                       user_id     = ?
                   WHERE id        = ?
               """,
            (title, description, date, event_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def delete_event(event_id: int) -> bool:
    """
    This function deletes the event in the database.
    :param event_id: id of a subject to delete
    :return success status: whether delete was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# endregion


# region messages


def fetch_messages() -> list[tuple[int, str, int]] | None:
    """
    This function fetches messages from the database.
    :return list of tuple: list of tuple representing messages
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        messages = cursor.fetchall()
        conn.commit()
        conn.close()
        return messages
    except Exception as e:
        print(e)
        return None


def insert_message(content: str, user_id: int) -> bool:
    """
    This function inserts event into the database.
    :param content: message content
    :param user_id: user id
    :return success status: whether insert was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   INSERT INTO messages (content, user_id)
                   VALUES (?, ?, ?, ?)
               """,
            (content, user_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def update_message(message_id: int, content: str, user_id: int) -> bool:
    """
    This function updates event in the database.
    :param content: message content
    :param user_id: user id
    :param message_id: message id
    :return success status: whether update was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   UPDATE messages
                   SET content = ?,
                       user_id = ?
                   WHERE id    = ?
               """,
            (content, user_id, message_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def delete_message(message_id: int) -> bool:
    """
    This function deletes the message in the database.
    :param message_id: id of a message to delete
    :return success status: whether delete was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# endregion


# region users
def fetch_users() -> list[tuple[int, str, str]] | None:
    """
    This function fetches users from the database.
    :return list of tuple: list of tuple representing users
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        events = cursor.fetchall()
        conn.commit()
        conn.close()
        return events
    except Exception as e:
        print(e)
        return None


def insert_users(name: str, uuid: str) -> bool:
    """
    This function inserts user into the database.
    :param name: user name
    :param uuid: user uuid
    :return success status: whether insert was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   INSERT INTO users (name, uuid)
                   VALUES (?, ?)
               """,
            (name, uuid),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def update_user(user_id: int, name: str, uuid: str) -> bool:
    """
    This function updates user in the database.
    :param user_id: user id
    :param name: user name
    :param uuid: user uuid
    :return success status: whether update was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                   UPDATE users
                   SET name = ?,
                       uuid = ?
                   WHERE id = ?
               """,
            (name, uuid, user_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def delete_user(user_id: int) -> bool:
    """
    This function deletes the user in the database.
    :param user_id: user id
    :return success status: whether delete was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# endregion
