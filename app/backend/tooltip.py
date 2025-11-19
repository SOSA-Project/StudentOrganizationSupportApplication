import customtkinter as ctk


class Tooltip:
    """
    Class manages creating, displaying and hiding a tooltip for a chosen widget
    """
    def __init__(self, widget: ctk, text: str, color: str = "#3B8ED0", delay: float = 400, wrap_length:int = 250, x_offset: float = 10, y_offset: float = 0) -> None:
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wrap_length = wrap_length
        self.color = color
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.tooltip_window = None
        self.after_id = None

        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event = None) -> None:
        """
        Method defines an on enter event for widget
        :param event: Empty event required for compilation
        :return: Nothing
        """
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def on_leave(self, event = None):
        """
        Method defines an on leave event for widget
        :param event: Empty event required for compilation
        :return: Nothing
        """
        if self.after_id:
            self.widget.after_cancel(self.after_id)
        self.after_id = None
        self.hide_tooltip()

    def show_tooltip(self) -> None:
        """
        Method creates tooltip for the widget
        :return: Nothing
        """
        if self.tooltip_window:
            return

        x = self.widget.winfo_rootx() + self.x_offset
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + self.y_offset

        self.tooltip_window = tw = ctk.CTkToplevel(self.widget)
        tw.overrideredirect(True)
        tw.geometry(f"+{x}+{y}")

        transparent_color = "#010203"
        tw.configure(fg_color=transparent_color)
        tw.wm_attributes("-transparentcolor", transparent_color)

        label = ctk.CTkLabel(
            tw,
            text=self.text,
            fg_color=("black", self.color),
            corner_radius=8,
            text_color=("black", "white"),
            padx=10,
            pady=6,
            wraplength = self.wrap_length
        )
        label.pack()

    def hide_tooltip(self) -> None:
        """
        Method hides and destroys tooltip of the widget
        :return: Nothing
        """
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None