#Data dictionnary

## Shops
| Name           | Type    | Integrity Constraints | Description                     | Example |
| -------------- | ------- | --------------------- | ------------------------------- | ------- |
| shop_id        | INTEGER | PRIMARY KEY           | Unique identifier for the shop  | 1       |
| shop_location  | TEXT    | NOT NULL, UNIQUE      | Location of the shop            | "Paris" |
| shop_employees | INTEGER | NOT NULL              | Number of employees in the shop | 10      |

## Products
| Name          | Type    | Integrity Constraints | Description                       | Example     |
| ------------- | ------- | --------------------- | --------------------------------- | ----------- |
| product_id    | TEXT    | PRIMARY KEY           | Unique identifier for the product | "REF001"    |
| product_name  | TEXT    | NOT NULL              | Name of the product               | "Produit A" |
| product_stock | INTEGER | NOT NULL              | Quantity of product in stock      | 100         |
| product_price | INTEGER | NOT NULL              | Price of the product (in cents)    | 4999        |

## Sales
| Name          | Type    | Integrity Constraints                                     | Description                     | Example      |
| ------------- | ------- | --------------------------------------------------------- | ------------------------------- | ------------ |
| product_id    | TEXT    | PRIMARY KEY (with shop_id and created_at), FOREIGN KEY    | References Products(product_id) | "REF001"     |
| shop_id       | INTEGER | PRIMARY KEY (with product_id and created_at), FOREIGN KEY | References Shops(shop_id)       | 1            |
| created_at    | NUMERIC | NOT NULL PRIMARY KEY (with product_id and shop_id)        | Date and time of the sale       | "2023-05-27" |
| quantity_sold | INTEGER | NOT NULL                                                  | Quantity of the product sold    | 5            |

## Units_sold_by_product
| Name                     | Type    | Integrity Constraints                       | Description                          | Example      |
| ------------------------ | ------- | ------------------------------------------- | ------------------------------------ | ------------ |
| units_sold_by_product_id | INTEGER | PRIMARY KEY                                 | Unique identifier for the entry      | 1            |
| amount_sold_by_product   | INTEGER | NOT NULL                                    | Number of units sold for the product | 45           |
| created_at               | NUMERIC | NOT NULL                                    | Date of aggregation                  | "2023-05-27" |
| product_id               | TEXT    | FOREIGN KEY REFERENCES Products(product_id) | Associated product                   | "REF001"     |

## Revenues
| Name           | Type    | Integrity Constraints | Description                       | Example      |
| -------------- | ------- | --------------------- | --------------------------------- | ------------ |
| revenue_id     | INTEGER | PRIMARY KEY           | Unique identifier for the revenue | 1            |
| revenue_amount | INTEGER | NOT NULL              | Total revenue amount (in cents)   | 10499        |
| created_at     | NUMERIC | NOT NULL              | Date of the revenue calculation   | "2023-05-27" |

## Units_sold_by_town
| Name                | Type    | Integrity Constraints                 | Description                               | Example      |
| ------------------- | ------- | ------------------------------------- | ----------------------------------------- | ------------ |
| units_sold_by_town  | INTEGER | PRIMARY KEY                           | Unique identifier for the entry           | 1            |
| amount_sold_by_town | TEXT    | NOT NULL                              | Number of units sold in a town (string ?) | "120"        |
| created_at          | NUMERIC | NOT NULL                              | Date of aggregation                       | "2023-05-27" |
| shop_id             | INTEGER | FOREIGN KEY REFERENCES Shops(shop_id) | Associated shop (thus town via location)  | 1            |
