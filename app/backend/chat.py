import json
import threading
import time
import asyncio
import websockets

from app.backend.session import Session


def make_payload(recipient: str, msg: str) -> bytes:
    return json.dumps(
        {
            "name": Session.username,
            "sender": Session.uuid,
            "recipient": recipient,
            "msg": msg,
        }
    ).encode("utf-8")


async def send(recipient: str, msg: str):
    """
    Function to send a message
    :param recipient: recipient of the message
    :param msg: message to be sent
    :return: None
    """
    async with websockets.connect("ws://localhost:6789") as ws:
        await ws.send(make_payload(recipient, msg))


class Client:
    """
    Chat client class. Manages all client process
    """

    @staticmethod
    def run() -> None:
        """
        Function to run client listener
        :return: None
        """
        while not Client.stop_event.is_set():
            time.sleep(1)
            asyncio.run(Client.receive())

    chat_display = None
    msg_queue: asyncio.queues.Queue = asyncio.Queue()
    thread = threading.Thread(target=run, daemon=True)
    stop_event = threading.Event()

    @staticmethod
    def stop() -> None:
        """
        Function to stop the client
        :return: None
        """
        Client.stop_event.set()
        if Client.thread.is_alive():
            Client.thread.join()

    @staticmethod
    async def listen(ws) -> dict | None:
        """
        Function to listen for messages
        :param ws: websocket object
        :return: dict | None
        """
        async for msg in ws:
            return json.loads(msg)
        return None

    @staticmethod
    def send(recipient: str, msg: str) -> None:
        """
        Wrapper for send function
        :param recipient: recipient of the message
        :param msg:  to be sent
        :return: None
        """
        asyncio.run(send(recipient, msg))

    @staticmethod
    async def receive() -> None:
        """
        Function to receive a message
        :return: None
        """
        async with websockets.connect("ws://localhost:6789") as ws:
            while not Client.stop_event.is_set():
                await ws.send(make_payload("-1", "check"))
                result = await asyncio.wait_for(Client.listen(ws), timeout=1.0)
                if result and result["msg"] != "none":
                    await Client.msg_queue.put(result)
                if Client.chat_display is not None and result["msg"] != "none":
                    Client.chat_display.configure(state="normal")
                    Client.chat_display.insert("end", f"{result["name"]}: {result["msg"]}\n")
                    Client.chat_display.configure(state="disabled")
                if result and result["msg"] == "none":
                    break


class Server:
    """
    Class to manage server for test purpose
    """

    @staticmethod
    def run():
        """
        Wrapper function to run the server
        """
        try:
            Server.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(Server.loop)
            Server.stop_event = asyncio.Event()
            Server.loop.run_until_complete(Server.main())
        except OSError as e:
            if e.errno != 98:
                raise

    clients: set = set()
    messages: list = []
    thread = threading.Thread(target=run, daemon=True)
    stop_event = asyncio.Event()

    @staticmethod
    def stop() -> None:
        """
        Function to stop the server
        :return: None
        """
        Server.stop_event.set()
        if Server.thread.is_alive():
            Server.thread.join()

    @staticmethod
    async def handle(ws) -> None:
        """
        Function to process incoming messages and replies
        :param ws: websocket object
        :return: None
        """
        Server.clients.add(ws)
        try:
            async for msg in ws:
                data = json.loads(msg)
                if data["msg"] != "check":
                    result = [row for row in Server.messages if row[0] == data["recipient"]] or None
                    if result:
                        result[0][1].append(data)
                    else:
                        Server.messages.append([data["recipient"], [data]])
                elif data["msg"] == "check":
                    result = [row for row in Server.messages if row[0] == data["sender"]] or None
                    if result and len(result[0][1]):
                        message = result[0][1].pop(0)
                        await asyncio.wait_for(ws.send(json.dumps(message).encode("utf-8")), timeout=1.0)
                    else:
                        new_msg = {
                            "name": "srwr",
                            "sender": -1,
                            "recipient": -1,
                            "msg": "none",
                        }
                        await asyncio.wait_for(ws.send(json.dumps(new_msg).encode("utf-8")), timeout=1.0)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            Server.clients.remove(ws)

    @staticmethod
    async def main() -> None:
        """
        Function to run the server
        :return: None
        """
        async with websockets.serve(Server.handle, "localhost", 6789):
            print("Server running at ws://localhost:6789")
            await Server.stop_event.wait()
