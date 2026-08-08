import sqlite3
import os
import random
from datetime import datetime, timedelta

def create_and_seed_db():
    """
    Creates a sample SQLite database for the AI Agent to query.
    Simulates a basic E-commerce platform.
    """
    os.makedirs("./data", exist_ok=True)
    db_path = "./data/database.db"
    
    # Connect to (or create) the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            country TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # 2. Clear existing data to ensure a fresh seed
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM customers")
    
    # 3. Insert Dummy Data
    customers = [
        ("Alice", "Smith", "alice@example.com", "USA"),
        ("Bob", "Johnson", "bob@example.com", "UK"),
        ("Charlie", "Brown", "charlie@example.com", "Canada"),
        ("Diana", "Prince", "diana@example.com", "USA"),
        ("Evan", "Wright", "evan@example.com", "Australia")
    ]
    cursor.executemany("INSERT INTO customers (first_name, last_name, email, country) VALUES (?, ?, ?, ?)", customers)
    
    products = [
        ("Laptop Pro", "Electronics", 1299.99, 50),
        ("Wireless Mouse", "Electronics", 49.99, 200),
        ("Desk Chair", "Furniture", 199.50, 20),
        ("Coffee Mug", "Accessories", 15.00, 500),
        ("Mechanical Keyboard", "Electronics", 149.99, 100)
    ]
    cursor.executemany("INSERT INTO products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)", products)
    
    # Create some random orders over the last 30 days
    statuses = ["completed", "completed", "completed", "pending", "shipped", "cancelled"]
    
    for i in range(1, 16):
        cust_id = random.randint(1, len(customers))
        status = random.choice(statuses)
        amount = round(random.uniform(15.0, 1500.0), 2)
        days_ago = random.randint(0, 30)
        order_date = datetime.now() - timedelta(days=days_ago)
        
        cursor.execute(
            "INSERT INTO orders (customer_id, status, total_amount, order_date) VALUES (?, ?, ?, ?)",
            (cust_id, status, amount, order_date.strftime("%Y-%m-%d %H:%M:%S"))
        )
        
    conn.commit()
    conn.close()
    print(f"Database successfully created and seeded at {db_path}!")

if __name__ == "__main__":
    create_and_seed_db()
