users = """
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    is_login BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

products = """
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price BIGINT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

menu_products = """
CREATE TABLE IF NOT EXISTS menu_products (
    id BIGSERIAL PRIMARY KEY,
    date_of_menu DATE DEFAULT CURRENT_DATE,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    amount BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

durations = """
CREATE TABLE IF NOT EXISTS durations (
    id BIGSERIAL PRIMARY KEY,
    from_time TIMESTAMP NOT NULL,
    to_time TIMESTAMP NOT NULL,
    seats INT DEFAULT 20,
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

orders = """
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    menu_product_id BIGINT REFERENCES menu_products(id),
    amount BIGINT NOT NULL,
    duration_id BIGINT REFERENCES durations(id),
    status BOOLEAN DEFAULT TRUE,
    order_type BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
