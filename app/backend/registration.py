import uuid
import hashlib
from app.backend.database import Db
from app.backend.session import Session


def get_all_users() -> list[tuple[int, str, str]] | None:
    """
    Returns all users from the data source.
    :param: None
    :return list of tuple: list of tuple representing users or None
    """
    try:
        return Db.fetch_users()
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []


class Auth:
    """
    Class responsible for user registration, login, logout, and session management.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Creates SHA-256 hash of the provided password.
        :param password: password to hash
        :return: hashed password as a string
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def register_user(username: str, password: str) -> bool:
        """
        Registers a new user.
        :param username: username to register
        :param password: password to register
        :return: True if registration was successful, False otherwise
        """
        if not username or not password:
            print("Fields cannot be empty.")
            return False

        if Db.fetch_user_by_name(username):
            print("User already exists.")
            return False

        user_uuid = str(uuid.uuid4())
        password_hash = Auth.hash_password(password)

        if Db.insert_users(username, user_uuid, password_hash):
            print("Registration successful!")
            return True

        print("Registration failed.")
        return False

    @staticmethod
    def login_user(username: str, password: str) -> bool:
        """
        Login a user.
        :param username: username to login
        :param password: password to login
        :return: True if login was successful, False otherwise
        """
        try:
            user = Db.fetch_user_by_name(username)
            if not user:
                print("User not found.")
                return False

            user_id, stored_name, stored_uuid, stored_hash = user
            if Auth.hash_password(password) != stored_hash:
                print("Wrong password.")
                return False

            Session.set_user_details((user_id, stored_name, stored_uuid))
            print("Login successful!")
            return True
        except Exception as e:
            print(f"Login failed due to DB error: {e}")
            return False

    @staticmethod
    def logout():
        """
        Logs out the current user by resetting the session.
        """
        Session.reset_session()

    @staticmethod
    def is_authenticated() -> bool:
        """
        Checks if there is an active user session.
        :return: True if a user is logged in, False otherwise
        """
        return Session.id is not None
