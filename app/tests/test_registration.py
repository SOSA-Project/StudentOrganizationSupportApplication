"""
File contains tests for registration file.
"""

import pytest
import hashlib
from unittest.mock import patch
from app.backend.registration import Auth, get_all_users


def test_get_all_users_success() -> None:
    """
    Tests correct fetching of all users.
    :return: Nothing, only provides test.
    """
    mock_users = [(1, "User1", "uuid1"), (2, "User2", "uuid2")]

    with patch("app.backend.registration.Db.fetch_users", return_value=mock_users):
        result = get_all_users()
        assert result == mock_users


def test_get_all_users_exception() -> None:
    """
    Tests behavior when fetch_users raises an exception.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Db.fetch_users", side_effect=Exception("DB error")):
        result = get_all_users()
        assert result == []


@pytest.mark.parametrize("password", ["abc", "123", "", "A" * 200])
def test_hash_password(password) -> None:
    """
    Tests that hash_password returns correct SHA-256 hash for various inputs.
    :param password: password to hash
    :return: Nothing, only provides test.
    """
    expected = hashlib.sha256(password.encode("utf-8")).hexdigest()
    assert Auth.hash_password(password) == expected


@pytest.mark.parametrize(
    "username,password",
    [
        ("", "pass"),
        ("user", ""),
        ("  ", "abc"),
        (None, "pass"),
        ("user", None),
    ],
)
def test_register_user_invalid_fields(username, password) -> None:
    """
    Tests that register_user rejects empty, None, or whitespace-only username/password.
    :param username: input username
    :param password: input password
    :return: Nothing, only provides test.
    """
    assert Auth.register_user(username, password) is False


def test_register_user_already_exists() -> None:
    """
    Tests that register_user returns False if username already exists in database.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Db.fetch_user_by_name", return_value=(1, "User", "uuid", "hash")):
        assert Auth.register_user("User", "pass") is False


def test_register_user_insert_fails() -> None:
    """
    Tests that register_user returns False if Db.insert_users fails.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Db.fetch_user_by_name", return_value=None), patch(
        "app.backend.registration.Db.insert_users", return_value=False
    ):
        assert Auth.register_user("User", "pass") is False


def test_register_user_success() -> None:
    """
    Tests that register_user returns True when user registration succeeds.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Db.fetch_user_by_name", return_value=None), patch(
        "app.backend.registration.Db.insert_users", return_value=True
    ):
        assert Auth.register_user("User", "password123") is True


def test_register_user_hash_called() -> None:
    """
    Tests that hash_password is called before inserting user into database.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Db.fetch_user_by_name", return_value=None), patch(
        "app.backend.registration.Db.insert_users", return_value=True
    ) as mock_insert, patch("app.backend.registration.Auth.hash_password", return_value="HASHED") as mock_hash:

        Auth.register_user("User", "pass123")

        mock_hash.assert_called_once_with("pass123")
        mock_insert.assert_called_once()


def test_login_user_not_found() -> None:
    """
    Tests that login_user returns False if user is not found in database.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Db.fetch_user_by_name", return_value=None):
        assert Auth.login_user("User", "pass") is False


def test_login_user_wrong_password() -> None:
    """
    Tests that login_user returns False if provided password does not match stored hash.
    :return: Nothing, only provides test.
    """
    stored = (1, "User", "uuid", Auth.hash_password("correct_pass"))

    with patch("app.backend.registration.Db.fetch_user_by_name", return_value=stored):
        assert Auth.login_user("User", "wrong_pass") is False


def test_login_user_success() -> None:
    """
    Tests that login_user returns True when username and password are correct.
    Also checks that Session.set_user_details is called.
    :return: Nothing, only provides test.
    """
    stored = (1, "User", "uuid", Auth.hash_password("password"))

    with patch("app.backend.registration.Db.fetch_user_by_name", return_value=stored), patch(
        "app.backend.registration.Session.set_user_details"
    ) as mock_session:

        assert Auth.login_user("User", "password") is True
        mock_session.assert_called_once_with((1, "User", "uuid"))


def test_login_user_db_exception() -> None:
    """
    Tests that login_user returns False if database access raises an exception.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Db.fetch_user_by_name", side_effect=Exception("DB error")):
        assert Auth.login_user("User", "pass") is False


def test_logout_calls_session_reset() -> None:
    """
    Tests that logout calls Session.reset_session.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Session.reset_session") as mock_reset:
        Auth.logout()
        mock_reset.assert_called_once()


@pytest.mark.parametrize(
    "session_id,expected",
    [
        (10, True),
        (0, True),
        (None, False),
    ],
)
def test_is_authenticated(session_id, expected) -> None:
    """
    Tests is_authenticated returns True if a user session exists, False otherwise.
    :param session_id: mocked Session.id
    :param expected: expected return value
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.Session.id", session_id):
        assert Auth.is_authenticated() is expected
