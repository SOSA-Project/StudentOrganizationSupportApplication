import socket
import threading
import uuid
import json
from app.backend.database import Db
from app.backend.database import Persistent


class Chat:
    """
    Class for managing connection
    """

    conn = None
    chat_display = None

    @staticmethod
    def connect() -> socket.socket | None:
        """
        This function creates a new socket connection with the chat - server or client role
        :return: None
        """
        try:
            Chat.conn = listener()
        except Exception as e:
            print(f"Error in chat file: {e}")
            try:
                Chat.conn = initiator()
                print("Działa")
            except Exception as e:
                print(f"Error in chat file2: {e}")
        return Chat.conn


def send(uuid: str, msg: str) -> None:
    """
    Function to send message
    :param uuid: uuid of the user
    :param msg: message
    :return: None
    """
    if Chat.conn is None:
        Chat.conn = Chat.connect()

    users = Db.fetch_users()
    if users is None:
        raise RuntimeError("No users found!")

    host = users[Persistent.get_id() - 1]

    auth = {
        "name": host[1],
        "sender": host[2],
        "recipient": uuid,
        "msg": msg,
    }

    if (conn := Chat.conn) is not None:
        conn.send(json.dumps(auth).encode("utf-8"))


def handle_incoming(conn) -> None:
    """
    This function listens for incoming messages.
    :param conn: current socket connection
    """
    while True:  # text
        try:
            msg = conn.recv(1024).decode("utf-8")
            if msg:
                data = json.loads(msg)

                users = Db.fetch_users()
                if users is None:
                    raise RuntimeError("No users found!")

                if data["recipient"] == users[Persistent.get_id() - 1][2]:
                    Db.insert_message(data["msg"], data["sender"])
                    if Chat.chat_display is not None:
                        Chat.chat_display.configure(state="normal")
                        Chat.chat_display.insert("end", f"{data["name"]}: {data["msg"]}\n")
                        Chat.chat_display.configure(state="disabled")
                    else:
                        raise RuntimeError("Chat uninitiated!")

        except Exception as e:
            print(f"Error in handle_incoming: {e}")
            break
    Chat.conn = None


def initiator(host: str = "localhost", port: int = 1337) -> socket.socket:
    """
    This function creates a new socket connection with the chat - server role
    :param host: server host address
    :param port: port number
    :return: socket connection
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    conn, addr = server.accept()
    threading.Thread(target=handle_incoming, args=(conn,), daemon=True).start()
    return conn


def listener(host: str = "localhost", port: int = 1337) -> socket.socket:
    """
    This function creates a new socket connection with the chat - client role
    :param host: server host address
    :param port: port number
    :return: socket connection
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    threading.Thread(target=handle_incoming, args=(client,), daemon=True).start()
    return client


def chat_loop(conn: socket.socket) -> None:
    """
    This function handles sending messages.
    :param conn: current socket connection
    """
    # example auth
    local_uuid = uuid.uuid4()
    conn.send(('{ "name": "' + str(local_uuid) + '", "uuid": "' + str(local_uuid) + '" }').encode("utf-8"))
    print("Chat\n")
    while True:
        msg = input()
        if msg.lower() == "exit":
            conn.close()
            break
        conn.send(msg.encode("utf-8"))


if __name__ == "__main__":
    try:
        conn = listener()
    except Exception as e:
        print(f"Error in chat file: {e}")
        conn = initiator()
    print(type(conn))
    chat_loop(conn)
