"""
File contains tests for notifications module.
"""

import pytest

from app.backend.notifications import (
    Notification,
    NotificationType,
    NotificationManager,
    initiate_notification_manager,
)


def test_mark_as_read() -> None:
    """
    Tests the mark_as_read method of Notification.
    :return: Nothing, only provides test.
    """
    notif = Notification(1, "10", "msg", 1, False)
    notif.mark_as_read()
    assert notif.is_read is True


def test_update_message() -> None:
    """
    Tests the update_message method of Notification.
    :return: Nothing, only provides test.
    """
    notif = Notification(1, "10", "old", 1, False)
    notif.update_message("new")
    assert notif.message == "new"


@pytest.mark.parametrize("ntype", [1, 2, 3, 4, 5])
def test_notification_type_enum(ntype: int) -> None:
    """
    Tests NotificationType enum assignment in Notification.
    :param ntype: Integer representing notification type.
    :return: Nothing, only provides test.
    """
    notif = Notification(1, "10", "msg", ntype)
    assert notif.notification_type == NotificationType(ntype)


def test_notification_manager_fills_notifications() -> None:
    """
    Tests fill_notifications_table method of NotificationManager.
    Ensures notifications are parsed correctly.
    :return: Nothing, only provides test.
    """
    sample = [
        (1, 1, "A", 1, "2025-12-04 12:00:00", False),
        (2, 1, "B", 2, "2025-12-04 13:00:00", True),
    ]

    mgr = NotificationManager(sample)

    assert len(mgr.notifications) == 2
    assert mgr.notifications[0].message == "A"
    assert mgr.notifications[1].notification_type == NotificationType.REMINDER


def test_get_unread_notifications() -> None:
    """
    Tests get_unread_notifications method of NotificationManager.
    :return: Nothing, only provides test.
    """
    sample = [
        (1, 1, "A", 1, "2025-12-04 12:00:00", False),
        (2, 1, "B", 2, "2025-12-04 13:00:00", True),
        (3, 1, "C", 3, "2025-12-04 14:00:00", False),
    ]

    mgr = NotificationManager(sample)

    unread = mgr.get_unread_notifications()
    assert len(unread) == 2
    assert unread[0].message == "A"
    assert unread[1].message == "C"


def test_initiate_notification_manager_returns_manager() -> None:
    """
    Tests initiate_notification_manager function.
    Ensures that it returns a NotificationManager instance with correct data.
    :return: Nothing, only provides test.
    """
    mgr = initiate_notification_manager()
    assert mgr is not None
    assert isinstance(mgr, NotificationManager)
    assert len(mgr.notifications) == 5
    assert all(isinstance(n, Notification) for n in mgr.notifications)
