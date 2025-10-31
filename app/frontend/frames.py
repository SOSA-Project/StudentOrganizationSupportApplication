"""
This file contains classes responsible for creating right and left frames for main gui app.
"""

import customtkinter as ctk


class LeftFrame:
    """
    Class is responsible for creating left frame for GUI.
    """

    def __init__(self, parent: ctk.CTk, color: str) -> None:
        self.parent: ctk.CTk = parent
        self.color: str = color
        self.left_frame: ctk.CTkFrame | None = None
        self._create_left_frame(self.color)

    def _create_left_frame(self, color: str) -> None:
        """
        Method creates left frame for GUI.
        :return: Nothing, only create left frame.
        """
        self.left_frame = ctk.CTkFrame(self.parent, fg_color=color, corner_radius=10)
        self.left_frame.grid(row=0, rowspan=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        [self.left_frame.grid_rowconfigure(index=i, weight=1, uniform="rowcol") for i in range(32)]
        [self.left_frame.grid_columnconfigure(index=i, weight=1, uniform="rowcol") for i in range(1)]

    @property
    def frame(self) -> ctk.CTkFrame:
        """
        Method is responsible for returning created frame.
        :return: ctk frame.
        """
        return self.left_frame


class RightFrame:
    """
    Class is responsible for creating right frame for GUI.
    """

    def __init__(self, parent: ctk.CTk, color: str) -> None:
        self.parent: ctk.CTk = parent
        self.color: str = color
        self.right_frame: ctk.CTkFrame | None = None
        self._create_right_frame(self.color)

    def _create_right_frame(self, color: str) -> None:
        """
        Method creates right frame for GUI.
        :return: Nothing, only create right frame.
        """
        self.right_frame = ctk.CTkFrame(self.parent, fg_color=color, corner_radius=10)
        self.right_frame.grid(row=0, rowspan=9, column=2, columnspan=22, sticky="nsew", padx=(0, 5), pady=5)
        self.right_frame.grid_rowconfigure(index=0, weight=1, uniform="rowcol")
        self.right_frame.grid_columnconfigure(index=0, weight=1, uniform="rowcol")
        self.right_frame.grid_propagate(False)
        self.right_frame.update_idletasks()

    @property
    def frame(self) -> ctk.CTkFrame:
        """
        Method is responsible for returning created frame.
        :return: ctk frame.
        """
        return self.right_frame
