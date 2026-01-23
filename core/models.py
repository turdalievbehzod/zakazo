"""
    Tables:
    users: id, username, password, is_login, created_at
    products: id, title, price, description, created_at
    menu_products: id, date_of_menu, product_id, amount, created_at
    durations: id, from_time, to_time, seats, created_at
    orders: id, user_id, menu_product_id, amount, duration_id, status, order_type, created_at

"""
users = """
    CREATE TABLE IF NOT EXISTS users
    (
        id BIGSERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        is_login BOOLEAN DEFAULT SET NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
products = """
    CREATE TABLE IF NOT EXISTS products
    (
        id BIGSERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        price BIGINT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

menu_products = """
    CREATE TABLE IF NOT EXISTS menu_products
    (
        id BIGSERIAL PRIMARY KEY,
        date_of_menu 
        product_id BIGINT REFERENCES products(id) ON DELETE CASCADE
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""