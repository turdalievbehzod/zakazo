from core.db_settings import execute_query
from psycopg2.extras import DictRow
from typing import Any




def show_all_products() -> DictRow | None | list[tuple[Any, ...]] | bool:
    execute_query("SELECT * FROM products ORDER BY id", fetch="all")

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
    execute_query("DELETE FROM products WHERE id=%s", (prod_id,))