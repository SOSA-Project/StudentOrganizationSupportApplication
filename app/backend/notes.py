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
