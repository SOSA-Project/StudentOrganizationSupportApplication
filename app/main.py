"""
File contains a function call that runs the entire project
"""

from app.backend.chat import Client, Server
from app.frontend.main_window import AppGUI
from app.backend.database import Db


def on_close(app: AppGUI) -> None:
    """
    Function which runs on close and manages the closing order
    :app: AppGUI
    :return: Nothing, only runs application
    """
    Db.close()
    Client.stop()
    Server.stop()
    app.destroy()


def run_app() -> None:
    """
    Main function which run application.
    :return: Nothing, only runs application
    """
    app = AppGUI()
    app.protocol("WM_DELETE_WINDOW", lambda: on_close(app))
    app.mainloop()
