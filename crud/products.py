import logging
from core.db_settings import execute_query
from typing import Optional, Union, Any
from psycopg2.extras import DictCursor, DictRow

def show_all_prods():
    query = """
    SELECT * FROM products
    """
    execute_query(query=query)
    
def add_new_product():
    title: str = input("")
    price: int = input("")
    description: str = input("")
    query = """
    INSERT INTO products(title, price, description) VALUES(%s, %s, %s)
    """
    params = (title, price, description,)
    
    execute_query(query=query, params=params)
    
def delete_product():
    query = """
    DELETE FROM products
    WHERE id=%s 
    """