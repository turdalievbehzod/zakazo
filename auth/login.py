import logging
from typing import Any
from psycopg2.extras import DictRow
from core.db_settings import execute_query

logger = logging.getLogger(__name__)


def register() -> bool:
    """
    Register new users
    :return: True if success else False
    """
    username: str = input("Username: ")
    password: str = input("Password: ")
    
    query: str = "INSERT INTO users (username, password) VALUES (%s, %s)"
    params: tuple[str, str] = (username, password,)

    if execute_query(query=query, params=params):
        # print("Successfully registered ✅")
        logger.debug('user successfully registered')
        return True
    else:
        # print("Something went wrong, try again later ❌")
        logger.warning('incorrect type, must be a string')
        return False


def login() -> bool:
    username: str = input("Username: ")
    password: str = input("Password: ")

    user = execute_query(
        """
        SELECT id, username, is_admin
        FROM users
        WHERE username=%s AND password=%s
        """,
        (username, password),
        fetch="one"
    )

    if not user:
        logger.warning("Login failed")
        return False

    execute_query(
        "UPDATE users SET active=TRUE WHERE id=%s",
        (user["id"],)
    )

    logger.info(
        "User logged in | admin=%s",
        user["is_admin"]
    )

    return True



def get_active_user() -> dict | None:
    return execute_query(
        """
        SELECT id, username, is_admin
        FROM users
        WHERE active=TRUE
        """,
        fetch="one"
    )



def logout_all() -> None:
    """
    Update all user is_login to False
    :return:
    """
    query1 = "UPDATE users SET is_login=False WHERE id > 0"
    execute_query(query=query1)
    