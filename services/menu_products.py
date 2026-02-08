from core.db_settings import execute_query




def show_today_menu():
    query = """
    SELECT mp.id, p.title, p.price, mp.amount
    FROM menu_products mp
    JOIN products p ON p.id = mp.product_id
    WHERE mp.date_of_menu = CURRENT_DATE
    ORDER BY mp.id
    """
    return execute_query(query, fetch="all")




def add_product_to_menu():
    product_id = int(input("Product ID: "))
    amount = int(input("Amount: "))
    execute_query(
    "INSERT INTO menu_products(product_id, amount) VALUES (%s,%s)",
    (product_id, amount)
    )




def remove_product_from_menu():
    menu_id = int(input("Menu product ID: "))
    execute_query("DELETE FROM menu_products WHERE id=%s", (menu_id,))