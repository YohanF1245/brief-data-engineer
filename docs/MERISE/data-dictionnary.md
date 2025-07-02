#Data dictionnary

## Shops
| Name           | Type    | Integrity Constraints | Description                     | Example |
| -------------- | ------- | --------------------- | ------------------------------- | ------- |
| shop_id        | INTEGER | PRIMARY KEY           | Unique identifier for the shop  | 1       |
| shop_location  | TEXT    | NOT NULL              | Location of the shop            | "Paris" |
| shop_employees | INTEGER | NOT NULL              | Number of employees in the shop | 10      |

## Products
| Name          | Type          | Integrity Constraints | Description                       | Example     |
| ------------- | ------------- | --------------------- | --------------------------------- | ----------- |
| product_id    | TEXT          | PRIMARY KEY           | Unique identifier for the product | "REF001"    |
| product_name  | TEXT          | NOT NULL              | Name of the product               | "Produit A" |
| product_stock | INTEGER       | NOT NULL              | Quantity of product in stock      | 100         |
| product_price | NUMERIC(15,2) | NOT NULL              | Price of the product              | 49.99       |


## Sales
| Name          | Type    | Integrity Constraints                      | Description                     | Example      |
| ------------- | ------- | ------------------------------------------ | ------------------------------- | ------------ |
| product_id    | TEXT    | PRIMARY KEY (with shop_id), FOREIGN KEY    | References Products(product_id) | "REF001"     |
| shop_id       | INTEGER | PRIMARY KEY (with product_id), FOREIGN KEY | References Shops(shop_id)       | 1            |
| created_at    | NUMERIC | NOT NULL                                   | Date and time of the sale       | "2023-05-27" |
| quantity_sold | INTEGER |                                            | Quantity of the product sold    | 5            |
