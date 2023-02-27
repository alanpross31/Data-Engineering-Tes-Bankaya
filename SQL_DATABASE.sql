CREATE TABLE IF NOT EXISTS  Customers (
   customers_id INTEGER PRIMARY KEY,
   first_name VARCHAR (200),
   last_name VARCHAR (200),
   phone_number VARCHAR (50),
   curp VARCHAR(200) NOT NULL,
   rfc VARCHAR(200),
   address VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS  Items (
   item_id INTEGER PRIMARY KEY,
   item_name VARCHAR (200),
   item_price INTEGER
);

CREATE TABLE IF NOT EXISTS  Items_Bougth (
   item_id INTEGER,
   customers_id INTEGER,
   order_number INTEGER ,
   date  TIMESTAMP,
   price INTEGER,
   comments VARCHAR(200),
   PRIMARY KEY (item_id,customers_id),
   FOREING KEY (item_id)
      REFERENCE Items (item_id),
   FOREING KEY (customers_id)
      REFERENCE Customers (customer_id)   
);