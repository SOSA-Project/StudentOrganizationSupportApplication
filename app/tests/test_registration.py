"""
File contains tests for registration file.
"""

import pytest
import hashlib
from unittest.mock import patch

from app.backend.registration import (
    get_all_users,
    encrypt_uuid,
    register_user,
)


@pytest.fixture
def mock_empty_db():
    """
    Fixture providing mocked empty DB state.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.get_all_users", return_value=[]), patch(
        "app.backend.registration.insert_users", return_value=True
    ):
        yield


def test_get_all_users_success() -> None:
    """
    Tests correct fetching of all users.
    :return: Nothing, only provides test.
    """
    mock_users = [(1, "Name1", "hash1"), (2, "Name2", "hash2")]

    with patch("app.backend.registration.fetch_users", return_value=mock_users):
        result = get_all_users()
        assert result == mock_users


def test_get_all_users_exception() -> None:
    """
    Tests behavior when fetch_users raises an exception.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.fetch_users", side_effect=Exception("DB error")):
        result = get_all_users()
        assert result == []


@pytest.mark.parametrize(
    "input_uuid",
    [
        "1234abcd",
        "",
        "A" * 64,
        "unicode",
    ],
)
def test_encrypt_uuid_various_inputs(input_uuid: str) -> None:
    """
    Tests SHA-256 encryption for multiple input variations.
    :param input_uuid: input UUID.
    :return: Nothing, only provides test.
    """
    expected = hashlib.sha256(input_uuid.encode("utf-8")).hexdigest()
    assert encrypt_uuid(input_uuid) == expected


@pytest.mark.parametrize(
    "invalid_name",
    ["", "   ", None],
)
def test_register_user_invalid_name(invalid_name) -> None:
    """
    Tests invalid names such as empty, None, or whitespace.
    :param invalid_name: invalid name.
    :return: Nothing, only provides test.
    """
    assert register_user(invalid_name) is None


def test_register_user_already_exists() -> None:
    """
    Tests registering a user that already exists.
    :return: Nothing, only provides test.
    """
    mock_users = [(1, "Name", "hash1")]

    with patch("app.backend.registration.get_all_users", return_value=mock_users):
        assert register_user("Name") is None


def test_register_user_insert_fails(mock_empty_db) -> None:
    """
    Tests behavior when inserting a new user fails.
    :param mock_empty_db: fixture providing mocked empty DB state.
    :return: Nothing, only provides test.
    """

    with patch("app.backend.registration.insert_users", return_value=False):
        assert register_user("User") is None


def test_register_user_success(mock_empty_db) -> None:
    """
    Tests successful user registration.
    :param mock_empty_db: fixture providing mocked empty DB state.
    :return: Nothing, only provides test.
    """
    result = register_user("User")
    assert result is not None
    assert result["name"] == "User"
    assert len(result["uuid"]) == 64


def test_register_user_calls_encrypt_uuid(mock_empty_db) -> None:
    """
    Tests if encrypt_uuid() is called during user registration.
    :param mock_empty_db: fixture providing mocked empty DB state.
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.encrypt_uuid", return_value="FAKE_HASH") as mock_e:
        result = register_user("User")

        assert result is not None
        mock_e.assert_called_once()
        assert result["uuid"] == "FAKE_HASH"


def test_register_user_uuid_unique(mock_empty_db) -> None:
    """
    Tests whether each registration generates a unique encrypted UUID.
    :param mock_empty_db: fixture providing mocked empty DB state.
    :return: Nothing, only provides test.
    """
    result1 = register_user("User1")
    result2 = register_user("User2")

    assert result1 is not None and result2 is not None
    assert result1["uuid"] != result2["uuid"]


def test_register_user_get_all_users_exception() -> None:
    """
    Tests behavior when get_all_users() returns an error (becomes empty list).
    :return: Nothing, only provides test.
    """
    with patch("app.backend.registration.get_all_users", return_value=[]), patch(
        "app.backend.registration.insert_users", return_value=True
    ):

        result = register_user("User")
        assert result is not None


def test_register_user_with_spaces(mock_empty_db) -> None:
    """
    Tests registration of username containing leading/trailing spaces.
    :param mock_empty_db: fixture providing mocked empty DB state.
    :return: Nothing, only provides test.
    """
    result = register_user("   User   ")
    assert result is not None
    assert result["name"] == "   User   "
