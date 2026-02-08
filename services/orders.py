import logging
from typing import Optional
from datetime import datetime, timedelta
from core.db_settings import execute_query
from auth.login import get_active_user
from psycopg2.extras import DictRow

logger = logging.getLogger(__name__)


def make_order() -> None:
    user = get_active_user()
    if not user:
        logger.warning("Order attempt without login")
        return

    menu_id: int = int(input("Menu product ID: "))
    amount: int = int(input("Amount: "))

    menu = execute_query(
        "SELECT amount FROM menu_products WHERE id=%s",
        (menu_id,),
        fetch="one"
    )

    if not menu or menu["amount"] < amount:
        logger.warning("Not enough product in menu")
        print("Not enough product available")
        return

    print("1. Take away")
    print("2. Dine in")
    choice: str = input("Choose option: ")

    if choice == "1":
        take_away(user["id"], menu_id, amount)
        return

    if choice == "2":
        dine_in(user["id"], menu_id, amount)
        return

    logger.warning("Invalid order type selected")

def take_away(user_id: int, menu_id: int, amount: int) -> None:
    logger.info("Processing take away order")

    execute_query(
        "UPDATE menu_products SET amount = amount - %s WHERE id = %s",
        (amount, menu_id)
    )

    execute_query(
        """
        INSERT INTO orders (user_id, menu_product_id, amount, order_type)
        VALUES (%s, %s, %s, FALSE)
        """,
        (user_id, menu_id, amount)
    )

    logger.info("Take away order created successfully")

def dine_in(user_id: int, menu_id: int, amount: int) -> None:
    logger.info("Processing dine in order")

    active_duration = execute_query(
        """
        SELECT * FROM durations
        WHERE status = TRUE AND to_time > NOW()
        ORDER BY from_time
        LIMIT 1
        """,
        fetch="one"
    )

    if active_duration and active_duration["seats"] <= 0:
        logger.warning("No seats available")
        print("No seats available. Please choose take away.")
        return

    if not active_duration:
        from_time = datetime.now()
        to_time = from_time + timedelta(hours=1)

        active_duration = execute_query(
            """
            INSERT INTO durations (from_time, to_time)
            VALUES (%s, %s)
            RETURNING id
            """,
            (from_time, to_time),
            fetch="one"
        )

        duration_id = active_duration["id"]
        logger.info("New duration created")
    else:
        duration_id = active_duration["id"]

    execute_query(
        "UPDATE durations SET seats = seats - 1 WHERE id = %s",
        (duration_id,)
    )

    execute_query(
        """
        INSERT INTO orders (user_id, menu_product_id, amount, duration_id, order_type)
        VALUES (%s, %s, %s, %s, TRUE)
        """,
        (user_id, menu_id, amount, duration_id)
    )

    logger.info("Dine in order created successfully")

def close_expired_durations() -> None:
    logger.info("Closing expired durations")

    execute_query(
        """
        UPDATE durations
        SET status = FALSE
        WHERE to_time <= NOW()
        """
    )

def make_order() -> None:
    user = get_active_user()
    if not user:
        logger.warning("User is not logged in")
        return

    menu_id: int = int(input("Menu product ID: "))
    amount: int = int(input("Amount: "))

    menu = execute_query(
        "SELECT amount FROM menu_products WHERE id=%s",
        (menu_id,),
        fetch="one"
    )

    if not menu or menu["amount"] < amount:
        logger.warning("Not enough product in menu")
        print("Not enough product available")
        return

    print("1. Take away")
    print("2. Dine in")
    choice: str = input("Choose option: ")

    if choice == "1":
        return take_away(user["id"], menu_id, amount)

    if choice == "2":
        return dine_in(user["id"], menu_id, amount)

    logger.warning("Invalid order type selected")


def show_my_orders() -> list[DictRow] | None:
    user = get_active_user()
    if not user:
        return None

    return execute_query(
        """
        SELECT 
            o.id,
            p.title,
            o.amount,
            o.status,
            o.order_type,
            o.created_at,
            d.from_time,
            d.to_time
        FROM orders o
        JOIN menu_products mp ON mp.id = o.menu_product_id
        JOIN products p ON p.id = mp.product_id
        LEFT JOIN durations d ON d.id = o.duration_id
        WHERE o.user_id = %s
        ORDER BY o.created_at DESC
        """,
        (user["id"],),
        fetch="all"
    )

def show_all_orders() -> None:
    orders = execute_query(
        """ 
        SELECT o.id,
               u.username,
               o.amount,
               o.status,
               o.order_type,
               o.created_at,
               d.from_time,
               d.to_time
        FROM orders o
        JOIN users u ON u.id = o.user_id
        LEFT JOIN durations d ON d.id = o.duration_id
        ORDER BY o.created_at DESC
        """,
        fetch="all"
    )

    logger.info("Fetched all orders")
    print(orders)

def change_order_status() -> None:
    order_id: int = int(input("Order ID: "))

    order = execute_query(
        "SELECT status FROM orders WHERE id=%s",
        (order_id,),
        fetch="one"
    )

    if not order:
        logger.warning("Order not found")
        return

    new_status: bool = not order["status"]

    execute_query(
        "UPDATE orders SET status=%s WHERE id=%s",
        (new_status, order_id)
    )

    logger.info("Order status changed")

def cancel_order() -> None:
    user = get_active_user()
    if not user:
        logger.warning("Cancel order attempt without login")
        return

    order_id: int = int(input("Order ID: "))

    order = execute_query(
        "SELECT * FROM orders WHERE id=%s AND user_id=%s",
        (order_id, user["id"]),
        fetch="one"
    )

    if not order or not order["status"]:
        logger.warning("Invalid cancel attempt")
        return

    execute_query(
        "UPDATE orders SET status=FALSE WHERE id=%s",
        (order_id,)
    )

    logger.info("Order cancelled successfully")
