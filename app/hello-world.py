print("Hello, World!")

import sqlite3
import requests
from datetime import datetime
from decimal import Decimal
# Database creation
conn = sqlite3.connect('/sqlite/data-engineer.db')

cursor = conn.cursor()
# Tables creation
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        product_price INTEGER NOT NULL,
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

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Revenues(
        revenue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        revenue_amount INTEGER NOT NULL,
        created_at NUMERIC NOT NULL
    );
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Units_sold_by_town(
        units_sold_by_town_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount_sold_by_town TEXT NOT NULL,
        created_at NUMERIC NOT NULL,
        shop_id INTEGER NOT NULL,
        FOREIGN KEY(shop_id) REFERENCES Shops(shop_id)
    );
    """
)

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS Units_sold_by_product(
        units_sold_by_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount_sold_by_product INTEGER NOT NULL,
        created_at NUMERIC NOT NULL,
        product_id TEXT NOT NULL,
        FOREIGN KEY(product_id) REFERENCES Products(product_id)
    );
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
    price = int(product['Prix'].replace('.', ''))
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

    #check if sale already exists
    sale_exists = False
    cursor.execute(
        """
        SELECT * FROM sales WHERE product_id = ? AND shop_id = ? AND created_at = ? AND quantity_sold = ?
        """,
        (product_id, shop_id, created_at, quantity_sold)
    )
    if cursor.fetchone():
        sale_exists = True 
    
    #insert sale if it doesn't exist
    if not sale_exists:
        cursor.execute(
            """
            INSERT OR IGNORE INTO sales (product_id, shop_id, created_at, quantity_sold) VALUES (?, ?, ?, ?)
            """,
            (product_id, shop_id, created_at, quantity_sold)
        )
    else:
        print("Sale is already in the database")
    conn.commit()

#   SELECT SUM(s.quantity_sold * p.product_price)
#    ...> FROM products AS p
#    ...> INNER JOIN sales AS s
#    ...> ON p.product_id = s.product_id;

#calculate total revenue
cursor.execute(
    """
    SELECT SUM(s.quantity_sold * p.product_price) 
    FROM products AS p 
    INNER JOIN sales AS s 
    ON p.product_id = s.product_id
    """
)   
total_revenue = cursor.fetchone()[0]
# Persist total revenue in the database
cursor.execute(
    """
    INSERT INTO Revenues (revenue_amount, created_at) VALUES (?, ?)
    """,
    (total_revenue, datetime.now().timestamp())
)
conn.commit()
print(f"Total revenue: {total_revenue/100}")

# sqlite> SELECT SUM(s.quantity_sold), p.product_name
#    ...> FROM sales AS s
#    ...> INNER JOIN products AS p
#    ...> ON p.product_id = s.product_id
#    ...> GROUP BY p.product_id;

cursor.execute(
    """
    SELECT SUM(s.quantity_sold), p.product_name 
    FROM sales AS s 
    INNER JOIN products AS p 
    ON p.product_id = s.product_id 
    GROUP BY p.product_id
    """
)
total_quantity_sold = cursor.fetchall()
# Persist total quantity sold by product in the database
for quantity in total_quantity_sold:
    cursor.execute(
        """
        INSERT INTO Units_sold_by_product (amount_sold_by_product, created_at, product_id) VALUES (?, ?, ?)
        """,
        (quantity[0], datetime.now().timestamp(), quantity[1])
    )
conn.commit()
print(f"Total quantity sold: {total_quantity_sold}")

# sqlite> SELECT SUM(s.quantity_sold), sh.shop_location
#    ...> FROM sales AS s
#    ...> INNER JOIN shops AS sh
#    ...> ON s.shop_id = sh.shop_id
#    ...> GROUP BY sh.shop_location;

cursor.execute(
    """
    SELECT SUM(s.quantity_sold), sh.shop_location 
    FROM sales AS s INNER JOIN shops 
    AS sh ON s.shop_id = sh.shop_id 
    GROUP BY sh.shop_location
    """
)
total_quantity_sold_by_shop = cursor.fetchall()
# Persist total quantity sold by shop in the database
for quantity in total_quantity_sold_by_shop:
    cursor.execute(
        """
        INSERT INTO Units_sold_by_town (amount_sold_by_town, created_at, shop_id) VALUES (?, ?, ?)
        """,
        (quantity[0], datetime.now().timestamp(), quantity[1])
    )
conn.commit()

print(f"Total quantity sold by shop: {total_quantity_sold_by_shop}")

conn.close()

