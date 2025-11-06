import uuid
import hashlib
from app.backend.data_base import fetch_users, insert_users


def get_all_users() -> list[tuple[int, str, str]] | None:
    """
    Returns all users from the data source.
    :param: None
    :return list of tuple: list of tuple representing users or None
    """
    try:
        return fetch_users()
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []


def encrypt_uuid(plain_uuid: str) -> str:
    """
    Encrypts the UUID using SHA-256 hash.
    :param plain_uuid: UUID string
    :return: Encrypted (hashed) UUID
    """
    return hashlib.sha256(plain_uuid.encode("utf-8")).hexdigest()


def register_user(name: str) -> dict[str, str] | None:
    """
    Registers a new user if not existing already.
    Encrypts UUID before storing it.
    :param name: Username
    :return: User details or None
    """
    if not name or not name.strip():
        print("Invalid username — cannot be empty.")
        return None

    users = get_all_users()
    if users and any(u[1].lower() == name.lower() for u in users):
        print(f"User '{name}' already exists.")
        return None

    new_uuid = str(uuid.uuid4())
    encrypted_uuid = encrypt_uuid(new_uuid)

    success = insert_users(name, encrypted_uuid)
    if not success:
        print("Error inserting user into database.")
        return None
    print("Successfully registered.")
    return {"name": name, "uuid": encrypted_uuid}
