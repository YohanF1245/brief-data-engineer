print("Hello, World!")

import sqlite3
import requests
from datetime import datetime
# Database creation
conn = sqlite3.connect('/sqlite/data-engineer.db')

cursor = conn.cursor()
# Tables creation
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        product_price FLOAT NOT NULL,
        product_stock INTEGER NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS shops (
        shop_id INTEGER PRIMARY KEY,
        shop_location TEXT NOT NULL UNIQUE,
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
        PRIMARY KEY(product_id, shop_id, created_at),
        FOREIGN KEY(product_id) REFERENCES Products(product_id),
        FOREIGN KEY(shop_id) REFERENCES Shops(shop_id)

    )
    """
)

# connect to the api
url = "http://data-api:555/api"
urlProducts = "/products_data"
urlShops = "/shops_data"
urlSales = "/sales_data"

#retrieve products data
responseProducts = requests.get(url + urlProducts)
products = responseProducts.json()

#insert products data into the database and adjust data types
for product in products:
    #prepare data for insertion
    product_id = product['ID Référence produit']
    name = product['Nom']
    price = float(product['Prix'])
    stock = int(product['Stock'])
    cursor.execute(
        """
        INSERT OR IGNORE INTO products (product_id, product_name, product_price, product_stock) VALUES (?, ?, ?, ?)
        """,
        (product_id, name, price, stock)
    )
    conn.commit()
#retrieve shops data
responseShops = requests.get(url + urlShops)
shops = responseShops.json()

#insert shops data into the database and adjust data types
for shop in shops:
    #prepare data for insertion
    shop_id = int(shop['ID Magasin'])
    location = shop['Ville']
    employees = int(shop['Nombre de salariés'])
    cursor.execute(
        """
        INSERT OR IGNORE INTO shops (shop_id, shop_location, shop_employees) VALUES (?, ?, ?)
        """,
        (shop_id, location, employees)
    )
    conn.commit()

#retrieve sales data
responseSales = requests.get(url + urlSales)
sales = responseSales.json()

for sale in sales:
    #prepare data for insertion and adjust data types
    product_id = sale['ID Référence produit']
    shop_id = int(sale['ID Magasin'])
    #convert date to timestamp
    created_at = int(datetime.strptime(sale['Date'], '%Y-%m-%d').timestamp())
    quantity_sold = int(sale['Quantité'])
    cursor.execute(
        """
        INSERT OR IGNORE INTO sales (product_id, shop_id, created_at, quantity_sold) VALUES (?, ?, ?, ?)
        """,
        (product_id, shop_id, created_at, quantity_sold)
    )
    conn.commit()

  


