print("Hello, World!")

import sqlite3
import csv

conn = sqlite3.connect('/sqlite/data-engineer.db')
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        product_price FLOAT NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS shops (
        shop_id INTEGER PRIMARY KEY,
        shop_location TEXT NOT NULL,
        shop_employees INTEGER NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS sales (
        product_id TEXT,
        shop_id INTEGER,
        created_at BIGINT NOT NULL,
        quantity_sold INTEGER,
        PRIMARY KEY(product_id, shop_id),
        FOREIGN KEY(product_id) REFERENCES Products(product_id),
        FOREIGN KEY(shop_id) REFERENCES Shops(shop_id)

    )
    """
)