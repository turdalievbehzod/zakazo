import logging
from psycopg2.extras import DictRow
from core.db_settings import execute_query
from typing import Any
logger = logging.getLogger(__name__)


def show_all_products() -> list[DictRow] | None:
    logger.info("Fetching all products")
    query = "SELECT * FROM products ORDER BY id"
    products = execute_query(query=query, fetch="all")

    if not products:
        logger.warning("No products found")

    return products


def add_product():
    title = input("Title: ")
    price = int(input("Price: "))
    description = input("Description: ")
    query = """
    INSERT INTO products(title, price, description) VALUES (%s,%s,%s)
    """
    params = (title, price, description,)
    execute_query(query=query,params=params)


def delete_product() -> DictRow | None | list[tuple[Any, ...]] | bool:
    prod_id = int(input("Product ID: "))
    query = "DELETE FROM products WHERE id=%s"
    params = (prod_id,)
    execute_query(query=query,params=params)