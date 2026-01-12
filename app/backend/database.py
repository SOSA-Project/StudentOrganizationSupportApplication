"""
The file creates a database and operates on it.
"""

import sqlite3
import asyncio

from datetime import datetime

from app.backend.chat import Client


class Db:
    @staticmethod
    def connect_to_database(conn: sqlite3.Connection) -> sqlite3.Cursor:
        """
        The function checks whether the database exists, and if not, it creates it.
        :param conn: connection to database
        :return sqlite3.Cursor:
        """
        cursor = conn.cursor()
        cursor.execute(
            """
               CREATE TABLE IF NOT EXISTS "grades" (
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
            CREATE TABLE IF NOT EXISTS "notes" (
                "id"	INTEGER,
                "title"	TEXT,
                "content"	TEXT,
                "created_at"	TEXT,
                "user_id"	INTEGER,
                "associated_date"   DATETIME,
                "color" TEXT,
                PRIMARY KEY("id")
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "events" (
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
            CREATE TABLE IF NOT EXISTS "messages" (
                "id"	INTEGER NOT NULL,
                "content"	TEXT NOT NULL,
                "user_id"	INTEGER NOT NULL,
                "incoming"	INTEGER NOT NULL,
                PRIMARY KEY("id")
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "users" (
                "id"	INTEGER NOT NULL,
                "name"	TEXT NOT NULL,
                "uuid"	TEXT NOT NULL,
                "password"	TEXT NOT NULL,
                PRIMARY KEY("id")
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "notifications" (
                "id"	INTEGER UNIQUE,
                "user_id"	TEXT,
                "message"	TEXT,
                "notification_type"	INTEGER,
                "is_read"	INTEGER,
                "associated_time"	TEXT,
                PRIMARY KEY("id")
            )
            """
        )
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        if "password" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN password TEXT NOT NULL DEFAULT ''")
            print("Added missing 'password' column to 'users' table.")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "subjects" (
                "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                "name"	TEXT,
                "ects"	INTEGER
            )
            """
        )
        conn.commit()
        return cursor

    conn = sqlite3.connect("./app/database/db.sqlite3")
    cursor = connect_to_database(conn)

    @staticmethod
    def dequeue_messages() -> None:
        """
        Insert all data from async queue to db
        :return None
        """
        while Client.msg_queue.qsize():
            result = asyncio.run(Client.msg_queue.get())
            Db.insert_message(result["msg"], result["sender"], result["recipient"])

    @staticmethod
    def close() -> None:
        """
        Commit all data to db and close connection
        :return None
        """
        Db.dequeue_messages()
        Db.conn.commit()
        Db.conn.close()

    # region grades
    @staticmethod
    def fetch_grades() -> list[tuple[float, str, int, float, int, int]] | None:
        """
        This function fetches the grades from the database.
        :return list of tuple: list of tuple representing grades
        """
        try:
            Db.cursor.execute(
                """
                        SELECT g.value, s.name, s.ects, g.weight, g.type, g.id
                        FROM grades AS g JOIN subjects AS s ON g.subject_id = s.id
                           """
            )
            return Db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def fetch_grades_id() -> list[tuple[str]] | None:
        """
        This function fetches grades form the database.
        :return: grades ids.
        """
        try:
            Db.cursor.execute("SELECT id FROM grades")
            return Db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
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
            Db.cursor.execute(
                """
                       INSERT INTO grades (value, weight, type, semester, subject_id, user_id)
                       VALUES (?, ?, ?, ?, ?, ?)
                   """,
                (value, weight, sub_type, semester, subject_id, user_id),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(f"Error in insert_grade: {e}")
            return False

    @staticmethod
    def update_grade(
        grade_id: int, value: float, weight: float, sub_type: int, semester: int, subject_id: int, user_id: int
    ) -> bool:
        """
        This function updates the grade in the database.
        :param grade_id: id of a grade to update
        :param value: grade value
        :param weight: grade weight
        :param sub_type: subject type
        :param semester: corresponding semester id
        :param subject_id: subject id
        :param user_id: user id
        :return success status: whether update was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       UPDATE grades
                       SET value       = ?,
                           weight      = ?,
                           type        = ?,
                           semester    = ?,
                           subject_id  = ?,
                           user_id     = ?
                       WHERE id = ?
                       """,
                (value, weight, sub_type, semester, subject_id, user_id, grade_id),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_grade(grade_id: int) -> bool:
        """
        This function deletes the grade in the database.
        :param grade_id: id of a grade to delete
        :return success status: whether delete was successful or not
        """
        try:
            Db.cursor.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # endregion

    # region notes
    @staticmethod
    def fetch_notes() -> list[tuple[int, str, str, str, int, str, str]] | None:
        """
        This function fetches notes from the database.
        :return list of tuple: list of tuple representing notes
        """
        try:
            Db.cursor.execute("SELECT * FROM notes")
            return Db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def insert_note(
        title: str, content: str, created_at: str, user_id: int, associated_date: datetime, color: str
    ) -> bool:
        """
        This function inserts note into the database.
        :param title: note title
        :param content: note content
        :param created_at: note creation date
        :param user_id: user id
        :param associated_date: note association date
        :param color: note color
        :return success status: whether insert was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       INSERT INTO notes (title, content, created_at, user_id, associated_date, color)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """,
                (title, content, created_at, user_id, associated_date, color),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_note(
        note_id: int, title: str, content: str, created_at: str, user_id: int, associated_date: datetime, color: str
    ) -> bool:
        """
        This function updates note in the database.
        :param note_id: id of a note to update
        :param title: note title
        :param content: note content
        :param created_at: note creation date
        :param user_id: user id
        :param associated_date: note association date
        :param color: note color
        :return success status: whether update was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       UPDATE notes
                       SET title      = ?,
                           content    = ?,
                           created_at = ?,
                           user_id    = ?,
                           associated_date = ?,
                           color = ?
                       WHERE id       = ?
                   """,
                (title, content, created_at, user_id, associated_date, color, note_id),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_note(note_id: int) -> bool:
        """
        This function deletes the note in the database.
        :param note_id: id of a note to delete
        :return success status: whether delete was successful or not
        """
        try:
            Db.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            return True
        except Exception as e:
            print(e)
            return False

    # endregion

    # region subjects
    @staticmethod
    def fetch_subjects() -> list[tuple[int, str, int]] | None:
        """
        This function fetches subjects from the database.
        :return list of tuple: list of tuple representing subjects
        """
        try:
            Db.cursor.execute("SELECT * FROM subjects")
            return Db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def insert_subject(name: str, ects: int) -> bool:
        """
        This function inserts subject into the database.
        :param name: subject name
        :param ects: subject ects
        :return success status: whether insert was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       INSERT INTO subjects (name, ects)
                       VALUES (?, ?)
                   """,
                (name, ects),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(f"Error in insert_subject: {e}")
            return False

    @staticmethod
    def update_subject(subject_id: int, name: str, ects: int) -> bool:
        """
        This function updates subject in the database.
        :param subject_id: id of a subject to update
        :param name: subject name
        :param ects: subject ects
        :return success status: whether update was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       UPDATE subjects
                       SET name   = ?,
                           ects   = ?
                       WHERE id   = ?
                   """,
                (name, ects, subject_id),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_subject(subject_id: int) -> bool:
        """
        This function deletes the subject in the database.
        :param subject_id: id of a subject to delete
        :return success status: whether delete was successful or not
        """
        try:
            Db.cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # endregion

    # region events
    @staticmethod
    def fetch_events() -> list[tuple[int, str, str, str, int]] | None:
        """
        This function fetches events from the database.
        :return list of tuple: list of tuple representing events
        """
        try:
            Db.cursor.execute("SELECT * FROM events")
            return Db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def insert_event(title: str, description: str, date: str, user_id: int) -> bool:
        """
        This function inserts event into the database.
        :param title: event title
        :param description: event description
        :param date: event date
        :param user_id: user id
        :return success status: whether insert was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       INSERT INTO events (title, description, date, user_id)
                       VALUES (?, ?, ?, ?)
                   """,
                (title, description, date, user_id),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
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
            Db.cursor.execute(
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
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_event(event_id: int) -> bool:
        """
        This function deletes the event in the database.
        :param event_id: id of a subject to delete
        :return success status: whether delete was successful or not
        """
        try:
            Db.cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # endregion

    # region messages

    @staticmethod
    def fetch_messages() -> list[tuple[int, str, int, int]] | None:
        """
        This function fetches messages from the database.
        :return list of tuple: list of tuple representing messages
        """
        try:
            Db.cursor.execute("SELECT * FROM messages")
            return Db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def insert_message(content: str, user_uuid: str, recipient_uuid: str) -> bool:
        """
        This function inserts event into the database.
        :param recipient_uuid: recipient uuid
        :param content: message content
        :param user_uuid: user universally unique identifier
        :return success status: whether insert was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       INSERT INTO messages (content, user_uuid, recipient_uuid)
                       VALUES (?, ?, ?)
                   """,
                (content, user_uuid, recipient_uuid),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_message(message_id: int, content: str, user_uuid: int, recipient_uuid: str) -> bool:
        """
        This function updates event in the database.
        :param recipient_uuid: recipient uuid
        :param content: message content
        :param user_uuid: user universally unique identifier
        :param message_id: message id
        :return success status: whether update was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       UPDATE messages
                       SET content        = ?,
                           user_uuid      = ?,
                           recipient_uuid = ?
                       WHERE id           = ?
                   """,
                (content, user_uuid, message_id, recipient_uuid),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_message(message_id: int) -> bool:
        """
        This function deletes the message in the database.
        :param message_id: id of a message to delete
        :return success status: whether delete was successful or not
        """
        try:
            Db.cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # endregion

    # region users
    @staticmethod
    def fetch_user_by_name(name: str) -> tuple[int, str, str, str] | None:
        """
        This function fetches a single user from the database by their username.
        :param name: username
        :return: a tuple representing the user
        """
        try:
            Db.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
            return Db.cursor.fetchone()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def fetch_users() -> list[tuple[int, str, str]] | None:
        """
        This function fetches users from the database.
        :return list of tuple: list of tuple representing users
        """
        try:
            Db.cursor.execute("SELECT * FROM users")
            return Db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def insert_users(name: str, uuid: str, password: str) -> bool:
        """
        This function inserts user into the database.
        :param name: username
        :param uuid: user uuid
        :param password: password
        :return success status: whether insert was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       INSERT INTO users (name, uuid, password)
                       VALUES (?, ?, ?)
                   """,
                (name, uuid, password),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_user(user_id: int, name: str, uuid: str) -> bool:
        """
        This function updates user in the database.
        :param user_id: user id
        :param name: username
        :param uuid: user uuid
        :return success status: whether update was successful or not
        """
        try:
            Db.cursor.execute(
                """
                       UPDATE users
                       SET name = ?,
                           uuid = ?
                       WHERE id = ?
                   """,
                (name, uuid, user_id),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        This function deletes the user in the database.
        :param user_id: user id
        :return success status: whether delete was successful or not
        """
        try:
            Db.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def fetch_user_password(user_id: int) -> str | None:
        """
        This function fetches user password from database.
        :param user_id: user id
        :return: success status
        """
        try:
            Db.cursor.execute("SELECT password FROM users where id = ?", (user_id,))
            return Db.cursor.fetchone()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_user_password(user_id: int, new_password: str) -> bool:
        """
        This function update user password.
        :param user_id: user id
        :param new_password: new user password
        :return: success status
        """
        try:
            Db.cursor.execute(
                """
                       UPDATE users
                       SET password = ?
                       WHERE id = ?
                   """,
                (new_password, user_id),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # endregion

    # region notifications

    @staticmethod
    def fetch_notifications() -> list[tuple[int, str, str, int, int, str]] | None:
        """
        This function fetches notifications from the database.
        :return list of tuple: list of tuple representing notifications
        """
        try:
            Db.cursor.execute("SELECT * FROM notifications")
            return Db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def insert_notification(
        user_id: str,
        message: str,
        notification_type: int,
        is_read: int,
        associated_time: str,
    ) -> bool:
        """
        This function inserts notification into the database.
        :param user_id: user id
        :param message: message
        :param notification_type: notification type
        :param is_read: is read
        :param associated_time: associated time
        :return success status: whether insert was successful or not
        """
        try:
            Db.cursor.execute(
                """
                INSERT INTO notifications (user_id, message, notification_type, is_read, associated_time)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, message, notification_type, is_read, associated_time),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_notification(
        notification_id: int,
        user_id: str,
        message: str,
        notification_type: int,
        is_read: int,
        associated_time: str,
    ) -> bool:
        """
        This function updates notification in the database.
        :param notification_id: notification id
        :param user_id: user id
        :param message: notification message
        :param notification_type: notification type
        :param is_read: notification read
        :param associated_time: notification associated time
        :return success status: whether update was successful or not
        """
        try:
            Db.cursor.execute(
                """
                UPDATE notifications
                SET user_id          = ?,
                    message          = ?,
                    notification_type = ?,
                    is_read          = ?,
                    associated_time  = ?
                WHERE id             = ?
                """,
                (user_id, message, notification_type, is_read, associated_time, notification_id),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_notification(notification_id: int) -> bool:
        """
        This function deletes the notification in the database.
        :param notification_id: notification id
        :return success status: whether delete was successful or not
        """
        try:
            Db.cursor.execute(
                "DELETE FROM notifications WHERE id = ?",
                (notification_id,),
            )
            Db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
