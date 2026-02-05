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
        date_of_menu DATE DEFAULT CURRENT_DATE
        product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
        amount BIGINT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

durations = """
    CREATE TABLE IF NOT EXISTS durations
    (
        id BIGSERIAL PRIMARY_KEY,
        from_time 
        to_time
    )
"""

_current_user = None


def set_current_user(user: dict) -> dict | None:
    """
    Save logged in user
    """
    global _current_user
    _current_user = user


def get_current_user() -> dict | None:
    """
    Get current logged in user
    """
    return _current_user


def logout() -> None:
    """
    Logout current user
    """
    global _current_user
    _current_user = None