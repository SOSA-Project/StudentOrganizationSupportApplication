import socket
import threading
import uuid


def handle_incoming(conn) -> None:
    """
    This function listens for incoming messages.
    :param conn: current socket connection
    """
    while True:  # handle auth
        try:
            msg = conn.recv(1024).decode("utf-8")
            if msg:
                print(msg)
                break
        except Exception as e:
            print(f"Error in handle_incoming: {e}")
            break

    while True:  # text
        try:
            msg = conn.recv(1024).decode("utf-8")
            if msg:
                print(f"\nPeer: {msg}")  # place for integration with gui/db
        except Exception as e:
            print(f"Error in handle_incoming: {e}")
            break


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
