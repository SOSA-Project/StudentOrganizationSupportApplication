from datetime import datetime
from enum import Enum
import customtkinter as ctk
from typing import Callable

from app.backend.tooltip import NotificationPopUp
from app.backend.database import Db


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
        user_id: str,
        message: str,
        notification_type: int = 1,
        is_read: bool = False,
        associated_time: datetime | None = None,
    ) -> None:
        self.id: int = id
        self.user_id: str = user_id
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

    def __init__(self, notifications_list: list[tuple[int, str, str, int, int, str]], app: ctk.CTk) -> None:
        self.notifications: list[Notification] = []
        self.fill_notifications_table(notifications_list)
        self.app = app
        self.check_interval_ms = 500
        self.popup_window: NotificationPopUp | None = None
        self.check_id = None
        self.notifications_updated: None | Callable = None

        self.check_notifications()

    def fill_notifications_table(self, notifications_list: list[tuple[int, str, str, int, int, str]]) -> None:
        """
        Method that fills notifications list with fetched notifications.
        :param notifications_list: List of tuples representing notifications data
        :return: Nothing
        """
        for row in notifications_list:
            notification_id, user_id, message, notification_type, is_read, associated_time = row
            try:
                datetime.strptime(associated_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                associated_time = "2026-1-1 00:00:00"

            notification = Notification(
                notification_id,
                user_id=user_id,
                message=message,
                notification_type=notification_type,
                is_read=bool(is_read),
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

    def delete_notification(self, notification_id: int) -> None:
        """
        Deletes notification from database and manager
        :param notification_id: Id of a notification to delete
        :return: Nothing
        """
        notification_to_delete = None
        for notification in self.notifications:
            if notification.id == notification_id:
                notification_to_delete = notification
        if notification_to_delete is not None:
            self.notifications.remove(notification_to_delete)
            Db.delete_notification(notification_to_delete.id)

    def mark_as_read(self, notification_id: int):
        notification_to_update = None
        for notification in self.notifications:
            if notification.id == notification_id:
                notification_to_update = notification
        if notification_to_update is not None:
            notification_to_update.mark_as_read()
            Db.update_notification(
                notification_id=notification_to_update.id,
                is_read=True,
                user_id=notification_to_update.user_id,
                associated_time=str(notification_to_update.associated_time),
                message=notification_to_update.message,
                notification_type=notification_to_update.notification_type.value,
            )

    def add_notification(self, message: str, notification_type: int, associated_time: str) -> None:
        """
        Adds new notification to database and manager
        :param message: Notification message
        :param notification_type: Notification type
        :param associated_time: Notification date
        :return: Nothing
        """
        Db.insert_notification(
            message=message,
            notification_type=notification_type,
            associated_time=associated_time,
            is_read=False,
            user_id="1",
        )
        db_notifications = Db.fetch_notifications()
        notification_to_add = None
        if db_notifications is not None:
            for notification in db_notifications:
                if (
                    notification[2] == message
                    and notification[3] == notification_type
                    and associated_time == notification[5]
                ):
                    notification_to_add = notification
            if notification_to_add is not None:
                self.notifications.append(
                    Notification(
                        notification_to_add[0],
                        user_id=notification_to_add[1],
                        message=notification_to_add[2],
                        notification_type=notification_to_add[3],
                        is_read=bool(notification_to_add[4]),
                        associated_time=datetime.strptime(notification_to_add[5], "%Y-%m-%d %H:%M:%S"),
                    )
                )

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
                    Db.update_notification(
                        notification_id=notification.id,
                        is_read=True,
                        user_id=notification.user_id,
                        associated_time=str(notification.associated_time),
                        message=notification.message,
                        notification_type=notification.notification_type.value,
                    )
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
        notifications = Db.fetch_notifications()
        if not notifications or not isinstance(notifications, list):
            return None

        def valid_item(item: tuple) -> bool:
            expected_types = (int, str, str, int, int, str)
            if not isinstance(item, tuple) or len(item) != len(expected_types):
                return False
            return all(isinstance(x, t) for x, t in zip(item, expected_types))

        if all(valid_item(item) for item in notifications):
            return NotificationManager(notifications, app)

        return None

    except TypeError:
        print("Notifications could not be fetched from database")
        return None
