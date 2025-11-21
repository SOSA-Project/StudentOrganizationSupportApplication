import json
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
        print("Sent")


class Client:
    """
    Chat client class. Manages all client process
    """

    chat_display = None
    msg_queue: asyncio.queues.Queue = asyncio.Queue()

    @staticmethod
    async def listen(ws) -> dict | None:
        """
        Function to listen for messages
        :param ws: websocket object
        :return: dict | None
        """
        async for msg in ws:
            print(type(json.loads(msg)))
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
            while True:
                await ws.send(make_payload("-1", "check"))
                result = await asyncio.wait_for(Client.listen(ws), timeout=1.0)
                if result and result["msg"] != "none":
                    await Client.msg_queue.put(result)
                if Client.chat_display is not None and result["msg"] != "none":
                    Client.chat_display.configure(state="normal")
                    Client.chat_display.insert("end", f"{result["name"]}: {result["msg"]}\n")
                    Client.chat_display.configure(state="disabled")
                else:
                    pass
                print(result)
                if result and result["msg"] == "none":
                    break

    @staticmethod
    def run() -> None:
        """
        Function to run client listener
        :return: None
        """
        while True:
            print("Waiting...")
            time.sleep(5)
            asyncio.run(Client.receive())


class Server:
    """
    Class to manage server for test purpose
    """

    clients: set = set()
    messages: list = []

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
                print(msg)
                data = json.loads(msg)
                # print(Server.messages)
                if data["msg"] != "check":
                    result = [row for row in Server.messages if row[1] == data["recipient"]] or None
                    if result:
                        result[0][2].append(data)
                    else:
                        Server.messages.append([None, data["recipient"], [data]])
                elif data["msg"] == "check":
                    result = [row for row in Server.messages if row[1] == data["sender"]] or None
                    if result and len(result[0][2]):
                        print(result[0][2])
                        message = result[0][2].pop(0)
                        print(message)
                        await ws.send(json.dumps(message).encode("utf-8"))
                    else:
                        new_msg = {
                            "name": "srwr",
                            "sender": -1,
                            "recipient": -1,
                            "msg": "none",
                        }
                        await ws.send(json.dumps(new_msg).encode("utf-8"))
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
            await asyncio.Future()

    @staticmethod
    def run():
        """
        Wrapper function to run the server
        """
        asyncio.run(Server.main())
