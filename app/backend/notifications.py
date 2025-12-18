from datetime import datetime
from enum import Enum
import customtkinter as ctk
from typing import Callable

from app.backend.tooltip import NotificationPopUp


class NotificationType(Enum):
    """
    Enumerator class for types of notifications
    """

    INFO = 1
    REMINDER = 2
    ALERT = 3
    WARNING = 4
    ERROR = 5


class Notification:
    """
    Class representing a notification, possessing data relevant to a notification.
    """

    def __init__(
        self,
        id: int,
        user_id: int,
        message: str,
        notification_type: int = 1,
        is_read: bool = False,
        associated_time: datetime | None = None,
    ) -> None:
        self.id: int = id
        self.user_id: int = user_id
        self.message: str = message
        self.notification_type: NotificationType = NotificationType(notification_type)
        self.is_read: bool = is_read
        self.associated_time: datetime | None = associated_time

    def mark_as_read(self) -> None:
        """
        Marks notification as read.
        :return: Nothing
        """
        self.is_read = True

    def update_message(self, new_message: str) -> None:
        """
        Updates notification's message.
        :param new_message:  to update notification
        :return: Nothing
        """
        self.message = new_message


class NotificationManager:
    """
    Class responsible for managing notifications.
    """

    def __init__(self, notifications_list: list[tuple[int, int, str, int, str, bool]], app: ctk.CTk) -> None:
        self.notifications: list[Notification] = []
        self.fill_notifications_table(notifications_list)
        self.app = app
        self.check_interval_ms = 500
        self.popup_window: NotificationPopUp | None = None
        self.check_id = None
        self.notifications_updated: None | Callable = None

        self.check_notifications()

    def fill_notifications_table(self, notifications_list: list[tuple[int, int, str, int, str, bool]]) -> None:
        """
        Method that fills notifications list with fetched notifications.
        :param notifications_list: List of tuples representing notifications data
        :return: Nothing
        """
        for row in notifications_list:
            notification_id, user_id, message, notification_type, associated_time, is_read = row
            notification = Notification(
                notification_id,
                user_id=user_id,
                message=message,
                notification_type=notification_type,
                is_read=is_read,
                associated_time=datetime.strptime(associated_time, "%Y-%m-%d %H:%M:%S"),
            )
            self.notifications.append(notification)

    def get_all_notifications(self) -> list[Notification]:
        """
        Method returns list of all user's notifications.
        :return: List of notifications
        """
        return self.notifications

    def get_unread_notifications(self) -> list[Notification]:
        """
        Method returns unread notifications.
        :return: List of unread notifications
        """
        return [n for n in self.notifications if not n.is_read]

    def check_notifications(self) -> None:
        """
        Method which cyclically checks whether a notification should be displayed
        :return: Nothing
        """

        now = datetime.now()

        for notification in self.get_unread_notifications():
            if notification.associated_time is not None and now >= notification.associated_time:
                if self.show_notification(notification):
                    notification.is_read = True
                    if self.notifications_updated is not None:
                        self.notifications_updated()

        self.check_id = self.app.after(self.check_interval_ms, self.check_notifications)

    def stop_checking(self) -> None:
        """
        Method that stops notification checking process
        :return: Nothing
        """
        if self.check_id:
            self.app.after_cancel(self.check_id)
            self.check_id = None

    def show_notification(self, notification: Notification) -> bool:
        """
        Method responsible for displaying a notification
        :param notification: Notification to be displayed
        :return: Whether the notification is still active
        """
        if self.popup_window:
            if not self.popup_window.active:
                del self.popup_window
                self.popup_window = None
            return False
        self.popup_window = NotificationPopUp(self.app, notification.message)
        return True


def initiate_notification_manager(app: ctk.CTk) -> NotificationManager | None:
    """
    Function fetches notifications data from database, verifies it
    and initiates an instance of notification manager with it.
    :return: Initialised instance of NotificationManager or None when data is verified as incorrect
    """
    try:
        # notifications = Db.fetch_notifications() uncomment when implemented in database
        notifications = [
            (1, 1, "Test Notification TEST MESSAGE TEST MESSAGE TEST MESSAGE  ", 1, "2025-12-17 17:58:30", False),
            (2, 1, "Second Test Notification", 1, "2025-12-04 17:25:13", False),
            (3, 1, "Test Alert", 3, "2025-12-04 16:30:23", True),
            (4, 1, "Test Warning", 4, "2025-12-04 16:42:11", True),
            (5, 1, "Test Error", 5, "2025-12-04 16:21:37", True),
        ]
        if not notifications or not isinstance(notifications, list):
            return None

        def valid_item(item: tuple) -> bool:
            expected_types = (int, int, str, int, str, bool)
            if not isinstance(item, tuple) or len(item) != len(expected_types):
                return False
            return all(isinstance(x, t) for x, t in zip(item, expected_types))

        if all(valid_item(item) for item in notifications):
            return NotificationManager(notifications, app)

        return None

    except TypeError:
        print("Notifications could not be fetched from database")
        return None
