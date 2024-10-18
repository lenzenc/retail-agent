CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100),
    order_date DATETIME,
    order_status VARCHAR(20),
    tracking_number VARCHAR(50),
    estimated_delivery_date DATE,
    actual_delivery_date DATE,
    item_id INTEGER
);
