import logging
from psycopg2.extras import DictRow
from core.db_settings import execute_query

logger = logging.getLogger(__name__)


def show_today_menu() -> list[DictRow] | None:
    logger.info("Fetching today's menu")
    query = """
        SELECT mp.id, p.title, p.price, mp.amount
        FROM menu_products mp
        JOIN products p ON p.id = mp.product_id
        WHERE mp.date_of_menu = CURRENT_DATE
        """
    return execute_query(query=query, fetch="all")


def add_product_to_menu() -> None:
    product_id: int = int(input("Product ID: "))
    amount: int = int(input("Amount: "))
    query = """
        INSERT INTO menu_products (product_id, amount)
        VALUES (%s, %s)
        """
    execute_query(query=query, params=(product_id, amount))

    logger.info("Product %s added to today's menu", product_id)


def remove_product_from_menu() -> None:
    menu_id: int = int(input("Menu product ID: "))
    query = "DELETE FROM menu_products WHERE id=%s"
    params = (menu_id,)
    execute_query(query=query, params=params)

    logger.info("Menu product removed: %s", menu_id)
