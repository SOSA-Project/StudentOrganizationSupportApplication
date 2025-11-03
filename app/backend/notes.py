"""
File contains definition of Note class
"""

from datetime import datetime


class Note:
    """
    Class stores information about a Note
    """

    def __init__(self, id: int, user_id: int, title: str, content: str) -> None:
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

    def update_title(self, new_title: str) -> None:
        """
        Updates the title of the note
        :param new_title: new title of the note
        :return: Nothing
        """
        self.title = new_title

    def update_content(self, new_content: str) -> None:
        """
        Updates the content of the note
        :param new_content: new content of the note
        :return: Nothing
        """
        self.content = new_content

    def update_user_id(self, new_user_id: int) -> None:
        """
        Updates the user_id of the note
        :param new_user_id: new user_id of the note
        :return: Nothing
        """
        self.user_id = new_user_id
