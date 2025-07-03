CREATE TABLE Products(
   product_id TEXT,
   product_name TEXT NOT NULL,
   product_stock INTEGER NOT NULL,
   product_price INTEGER NOT NULL,
   PRIMARY KEY(product_id)
);

CREATE TABLE Shops(
   shop_id INTEGER,
   shop_location TEXT NOT NULL,
   shop_employees INTEGER NOT NULL,
   PRIMARY KEY(shop_id)
);

CREATE TABLE Units_sold_by_product(
   units_sold_by_product_id INTEGER,
   amount_sold_by_product INTEGER NOT NULL,
   created_at NUMERIC NOT NULL,
   product_id TEXT NOT NULL,
   PRIMARY KEY(units_sold_by_product_id),
   FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE TABLE Revenues(
   revenue_id INTEGER,
   revenue_amount INTEGER NOT NULL,
   created_at NUMERIC NOT NULL,
   PRIMARY KEY(revenue_id)
);

CREATE TABLE Units_sold_by_town(
   units_sold_by_town INTEGER,
   amount_sold_by_town TEXT NOT NULL,
   created_at NUMERIC NOT NULL,
   shop_id INTEGER NOT NULL,
   PRIMARY KEY(units_sold_by_town),
   FOREIGN KEY(shop_id) REFERENCES Shops(shop_id)
);

CREATE TABLE Sells(
   product_id TEXT,
   shop_id INTEGER,
   created_at NUMERIC NOT NULL,
   quantity_sold INTEGER,
   PRIMARY KEY(product_id, shop_id),
   FOREIGN KEY(product_id) REFERENCES Products(product_id),
   FOREIGN KEY(shop_id) REFERENCES Shops(shop_id)
);
