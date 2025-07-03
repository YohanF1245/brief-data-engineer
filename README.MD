# Simplon's data engineer brief

## Table of content
- [Business rules](/docs/business-rules.md)
- Merise
    - [Data dictionnary](/docs/MERISE/data-dictionnary.md)
    - [Mcd](/docs/MERISE/merise-diagrams.md#mcd)
    - [Mcd](/docs/MERISE/merise-diagrams.md#mcd)
    - [Mcd](/docs/MERISE/merise-diagrams.md#mcd)
- [Requirements](#Requirements)
- [Usage](#usage)
- [Interact with the database](#interact-with-the-database)
- [ Response to Project Brief – Notes and Answers](#response-to-project-brief--notes-and-answers)
    - [Step 1 - Project architecture](#step-1---project-architecture)
    - [Step 2 - Docker compose file](#step-2---docker-compose-file)
    - [Step 3 - Data Analysis and Database design](#step-3---data-analysis-and-database-design)
    - [Step 4 - SQL requests for data analysis](#step-4---sql-requests-for-data-analysis)
## Requirements
- Docker
- Docker compose

## Usage
1. Clone this repository
2. Open a terminal and navigate to the project folder
3. Run the following command:
```
Docker compose up --build
```

## Interact with the database
Once Docker Compose is up and running, you can open the SQLite terminal with the following command:
```
docker exec -it sqlite sqlite3
```
Inside the container's interactive terminal, connect to the database by running:
```
.open /sqlite/data-engineer.db
```
You can then execute standard SQL queries to explore or modify the data.


 ## Response to Project Brief – Notes and Answers
 ### Step 1 - Project architecture
 ![architecture](/docs/assets/docker-architecture.png)
There are three Docker Compose services forming the core architecture. I added a fourth service to handle HTTP requests, as this is required later in the brief. A shared volume is used between the Python script and the SQLite3 containers. After some research, I found that SQLite is not a server-based database system, so using a shared volume is the most reliable method I found to allow both containers to interact with the same database file.

## Step 2 - Docker compose file
- [Docker compose file link](/docker-compose.yml)
- [Api Dockerfile](/api/Dockerfile)
- [Python script Dockerfile](/app/Dockerfile)

## Step 3 - Data Analysis and Database Design
- [Merise schema link](/docs/MERISE/merise-diagrams.md)
- [Data base and table creation in hello-world.py (lines 8-82)](/app/hello-world.py)
note: the following line will create the database if it does not exist:
```
conn = sqlite3.connect('/sqlite/data-engineer.db')
```
- sample http request for fetching data from api (products): 
```
responseProducts = requests.get(url + urlProducts)
products = responseProducts.json()
```
looping over result : 
```
for product in products:
```
preparing data for insertion (with type casting for relevant values) : 
```
product_id = product['ID Référence produit']
name = product['Nom']
price = int(product['Prix'].replace('.', ''))
stock = int(product['Stock'])
```
insert and persist data : 
```
cursor.execute(
"""
INSERT OR IGNORE INTO shops (shop_id, shop_location, shop_employees) VALUES (?, ?, ?)
""",
(shop_id, location, employees)
)
conn.commit()
```
condition for avoid duplication of sales (even tho I put a composite key on shop_id, product_id, and date with unique constraint to handle it) : 
```
sale_exists = False
cursor.execute(
    """
    SELECT * FROM sales WHERE product_id = ? AND shop_id = ? AND created_at = ? ANDquantity_sold = ?
    """,
    (product_id, shop_id, created_at, quantity_sold)
)
if cursor.fetchone():
    sale_exists = True 
```
The idea is to use a select request to see if the entry already exists and setup a boolean. This boolean is then used to allow or not the db insertion :
```
 if not sale_exists:
        cursor.execute(
```
## Step 4 - SQL requests for data analysis
- Request to calculate total revenue : 
```
cursor.execute(
    """
    SELECT SUM(s.quantity_sold * p.product_price) 
    FROM products AS p 
    INNER JOIN sales AS s 
    ON p.product_id = s.product_id
    """
)   
total_revenue = cursor.fetchone()[0]
```
- persist the revenue in db : 
```
cursor.execute(
    """
    INSERT INTO Revenues (revenue_amount, created_at) VALUES (?, ?)
    """,
    (total_revenue, datetime.now().timestamp())
)
conn.commit()
```
- Request to calculate sales per product : 
```
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
```
- persist sales per product in db : 
```
for quantity in total_quantity_sold:
    cursor.execute(
        """
        INSERT INTO Units_sold_by_product (amount_sold_by_product, created_at, product_id) VALUES (?, ?, ?)
        """,
        (quantity[0], datetime.now().timestamp(), quantity[1])
    )
conn.commit()
```
- Request to calculte sales by locatiion : 
```
cursor.execute(
    """
    SELECT SUM(s.quantity_sold), sh.shop_location 
    FROM sales AS s INNER JOIN shops 
    AS sh ON s.shop_id = sh.shop_id 
    GROUP BY sh.shop_location
    """
)
total_quantity_sold_by_shop = cursor.fetchall()
```
note: I wasn't really sure what "par région" meant. I assume grouping sales by town would be enough as this was the only info mentionned in data. If it was really not negotiable to group them by regions, i could have used the GEO governement api (https://geo.api.gouv.fr/definition.yml) to group the towns by regions.
- persist quantity sold by town : 
```
for quantity in total_quantity_sold_by_shop:
    cursor.execute(
        """
        INSERT INTO Units_sold_by_town (amount_sold_by_town, created_at, shop_id) VALUES (?, ?, ?)
        """,
        (quantity[0], datetime.now().timestamp(), quantity[1])
    )
conn.commit()
```
- sql analysis results : 
![image](/docs/assets/sql-analysis-result.png)




