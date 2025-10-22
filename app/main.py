"""
File contains a function call that runs the entire project
"""

from app.frontend.main_window import AppGUI


def run_app() -> None:
    """
    Main function which run application.
    :return: Nothing, only runs application
    """
    app = AppGUI()
    app.mainloop()
