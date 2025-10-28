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
                            "id"	INTEGER NOT NULL,
                            "value"	REAL NOT NULL,
                            "ects"	INTEGER NOT NULL,
                            "semester_id"	INTEGER NOT NULL,
                            PRIMARY KEY("id")
                        )
                       """
        )
        return conn


def fetch_grades() -> list[tuple[float, str, int, float, int, int]] | None:
    """
    This function fetches the grades from the database.
    :return list of tuple: list of tuple representing grades
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grades")
        grades = cursor.fetchall()
        conn.commit()
        conn.close()
        return grades
    except Exception as e:
        print(e)
        return None


def insert_grade(value: float, ects: int, semester_id: int) -> bool:
    """
    This function inserts grades into the database.
    :param value: grade value
    :param ects: ects points associated with grade
    :param semester_id: corresponding semester id
    :return success status: whether insert was successful or not
    """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                       INSERT INTO grades (value, ects, semester_id)
                       VALUES (?, ?, ?)
                       """,
            (value, ects, semester_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def update_grade(grade_id: int, value: float, ects: int, semester_id: int) -> bool:
    """
    This function updates the grade in the database.
    :param grade_id: id of a grade to update
    :param value: new grade value
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
                           ects        = ?,
                           semester_id = ?
                       WHERE id = ?
                       """,
            (value, ects, semester_id, grade_id),
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
def fetch_notes() -> list[tuple[str | int]] | None:
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


def update_note(
    note_id: int, title: str, content: str, created_at: str, user_id: int
) -> bool:
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
                       SET title     = ?,
                           content   = ?,
                           created_at = ?,
                           user_id   = ?
                       WHERE id      = ?
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
