class Session:
    """
    This class handles the session variables.
    """

    id = None
    username = None
    uuid = None

    @staticmethod
    def set_user_details(user: tuple) -> None:
        """
        This method sets the session variables.
        :param user: user tuple
        :return: None
        """
        Session.id = user[0]
        Session.username = user[1]
        Session.uuid = user[2]
        print(f"session data: {user}")

    @staticmethod
    def reset_session() -> None:
        """
        This method resets all session variables.
        :return: None
        """
        Session.id = None
        Session.username = None
        Session.uuid = None
