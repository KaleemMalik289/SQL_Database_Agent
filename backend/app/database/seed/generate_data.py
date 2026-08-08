"""
AI Retail Store - Synthetic Data Generator
============================================
Generates realistic, referentially-consistent business data for the
AI Retail Store SQLite database, in strict dependency order so that
no orphan records are ever created.

Design choices for realism (not uniform randomness):
  * Pareto-style customer order counts (most customers order rarely, a small "loyal" segment orders often).
  * Product popularity follows a long-tail distribution.
  * Order volume is seasonal (Nov-Dec spike, weekend uplift).
  * Payment method popularity is skewed (cards/mobile wallets more common).
  * Review ratings skew positive (3-5 stars dominate).
  * Inventory occasionally dips to zero.
"""

import sqlite3
import random
import os
import numpy as np
from datetime import date, datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "../../../data/ai_retail_store.db")
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "../schema/schema.sql")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ---------------------------------------------------------------------
# SCALE CONFIGURATION
# ---------------------------------------------------------------------
N_BRANCHES = 20
N_DEPARTMENTS = 8
N_EMPLOYEES = 300
N_SUPPLIERS = 100
N_PRODUCTS = 2000
N_CUSTOMERS = 10000
N_ORDERS = 50000
N_REVIEWS = 20000
N_RETURNS = 5000
N_PROMOTIONS = 100
N_DISCOUNTS = 500

START_DATE = date(2022, 1, 1)
END_DATE = date(2025, 12, 31)

# ---------------------------------------------------------------------
# CONNECT + BUILD SCHEMA
# ---------------------------------------------------------------------
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = OFF;")
cur = conn.cursor()

with open(SCHEMA_PATH) as f:
    conn.executescript(f.read())

print("Schema loaded. Beginning data generation...")

# =====================================================================
# 1. GEOGRAPHY: Countries -> States -> Cities
# =====================================================================
country_id = 1
cur.execute(
    "INSERT OR IGNORE INTO Countries (country_id, country_name, country_code) VALUES (?,?,?)",
    (country_id, "Pakistan", "PK"),
)

PROVINCES_CITIES = {
    "Sindh": ["Karachi", "Hyderabad", "Sukkur", "Larkana", "Mirpurkhas"],
    "Punjab": ["Lahore", "Faisalabad", "Rawalpindi", "Multan", "Gujranwala", "Sialkot"],
    "Khyber Pakhtunkhwa": ["Peshawar", "Abbottabad", "Mardan", "Swat"],
    "Balochistan": ["Quetta", "Gwadar"],
    "Islamabad Capital Territory": ["Islamabad"],
}

state_rows, city_rows = [], []
state_id_counter, city_id_counter = 1, 1
city_ids_by_name = {}

for province, cities in PROVINCES_CITIES.items():
    state_rows.append((state_id_counter, province, province[:3].upper(), country_id))
    for city_name in cities:
        city_rows.append((city_id_counter, city_name, state_id_counter))
        city_ids_by_name[city_name] = city_id_counter
        city_id_counter += 1
    state_id_counter += 1

cur.executemany("INSERT OR IGNORE INTO States (state_id, state_name, state_code, country_id) VALUES (?,?,?,?)", state_rows)
cur.executemany("INSERT OR IGNORE INTO Cities (city_id, city_name, state_id) VALUES (?,?,?)", city_rows)
ALL_CITY_IDS = list(city_ids_by_name.values())
print(f"Geography: {len(state_rows)} states, {len(city_rows)} cities")

# =====================================================================
# 2. DEPARTMENTS
# =====================================================================
DEPARTMENT_NAMES = [
    ("Sales", "Front-of-store sales"),
    ("Inventory & Warehouse", "Stock management"),
    ("Customer Service", "Customer support"),
    ("Finance & Accounts", "Payments reconciliation"),
    ("Human Resources", "Staffing"),
    ("Marketing & Promotions", "Campaigns"),
    ("IT & Systems", "POS systems"),
    ("Store Management", "Branch management"),
]
dept_rows = [(i + 1, name, desc) for i, (name, desc) in enumerate(DEPARTMENT_NAMES)]
cur.executemany("INSERT OR IGNORE INTO Departments (department_id, department_name, description) VALUES (?,?,?)", dept_rows)
print(f"Departments: {len(dept_rows)}")

# =====================================================================
# 3. BRANCHES
# =====================================================================
BRANCH_CITY_WEIGHTS = {
    "Karachi": 5, "Lahore": 4, "Islamabad": 2, "Rawalpindi": 2,
    "Faisalabad": 1, "Multan": 1, "Peshawar": 1, "Quetta": 1,
    "Hyderabad": 1, "Sialkot": 1, "Gujranwala": 1,
}
branch_city_pool = []
for city_name, weight in BRANCH_CITY_WEIGHTS.items():
    branch_city_pool.extend([city_name] * weight)
while len(branch_city_pool) < N_BRANCHES:
    branch_city_pool.append(random.choice(list(city_ids_by_name.keys())))
branch_city_pool = branch_city_pool[:N_BRANCHES]

branch_rows = []
for i in range(1, N_BRANCHES + 1):
    city_name = branch_city_pool[i - 1]
    opening = fake.date_between(start_date=date(2012, 1, 1), end_date=date(2023, 6, 1))
    branch_rows.append((
        i, f"AI Retail Store - {city_name} {['Central','Mall','Downtown','North','South','Plaza'][i % 6]}",
        f"BR-{i:03d}", city_ids_by_name[city_name], fake.street_address(),
        fake.numerify("0##-#######"), f"branch{i:03d}@airetailstore.pk",
        None, opening.isoformat(),
        random.choice([8000, 10000, 12000, 15000, 18000, 22000]),
        "Active" if random.random() > 0.04 else "Renovating",
    ))
cur.executemany("""INSERT OR IGNORE INTO Branches VALUES (?,?,?,?,?,?,?,?,?,?,?)""", branch_rows)
print(f"Branches: {len(branch_rows)}")

# =====================================================================
# 4. EMPLOYEES
# =====================================================================
employee_rows, branch_managers = [], {}
emp_id = 1
for b in range(1, N_BRANCHES + 1):
    first, last = fake.first_name(), fake.last_name()
    employee_rows.append((
        emp_id, b, 8, None, first, last,
        f"{first.lower()}.{last.lower()}{emp_id}@airetailstore.pk",
        fake.numerify("03##-#######"), "Branch Manager", "2020-01-01", None,
        150000.0, "Active"
    ))
    branch_managers[b] = emp_id
    emp_id += 1

while emp_id <= N_EMPLOYEES:
    b = random.randint(1, N_BRANCHES)
    dept = random.randint(1, 7)
    first, last = fake.first_name(), fake.last_name()
    employee_rows.append((
        emp_id, b, dept, branch_managers[b], first, last,
        f"{first.lower()}.{last.lower()}{emp_id}@airetailstore.pk",
        fake.numerify("03##-#######"), "Staff", "2021-01-01", None,
        50000.0, "Active"
    ))
    emp_id += 1

cur.executemany("""INSERT OR IGNORE INTO Employees VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", employee_rows)
cur.executemany("UPDATE Branches SET manager_employee_id = ? WHERE branch_id = ?", [(mgr, b) for b, mgr in branch_managers.items()])
print(f"Employees: {len(employee_rows)}")

# =====================================================================
# 5. SUPPLIERS
# =====================================================================
supplier_rows = []
for i in range(1, N_SUPPLIERS + 1):
    supplier_rows.append((
        i, fake.company() + " Traders", fake.name(), fake.company_email(),
        fake.numerify("021-########"), fake.address().replace("\n", ", "),
        random.choice(ALL_CITY_IDS), round(random.uniform(2.5, 5.0), 1), "Active"
    ))
cur.executemany("""INSERT OR IGNORE INTO Suppliers VALUES (?,?,?,?,?,?,?,?,?)""", supplier_rows)

# =====================================================================
# 6. CATEGORIES & PRODUCTS
# =====================================================================
cur.execute("INSERT OR IGNORE INTO Categories VALUES (1, 'Electronics', NULL, 'Tech gear')")
cur.execute("INSERT OR IGNORE INTO Categories VALUES (2, 'Grocery', NULL, 'Food')")

product_rows = []
for i in range(1, N_PRODUCTS + 1):
    cat_id = random.choice([1, 2])
    price = round(random.uniform(10, 5000), 2)
    product_rows.append((
        i, f"Product {i}", f"SKU-{i:06d}", cat_id, random.randint(1, N_SUPPLIERS),
        "GenericBrand", "each", price, price * 0.7, "Active"
    ))
cur.executemany("""INSERT OR IGNORE INTO Products VALUES (?,?,?,?,?,?,?,?,?,?)""", product_rows)

product_prices = {p[0]: p[7] for p in product_rows}
print(f"Products: {len(product_rows)}")

# =====================================================================
# 7. INVENTORY
# =====================================================================
inventory_rows = []
inv_id = 1
for b in range(1, N_BRANCHES + 1):
    for p in range(1, N_PRODUCTS + 1):
        if random.random() < 0.8: # 80% of products stocked at each branch
            inventory_rows.append((inv_id, p, b, random.randint(0, 100), 10, 50, "2025-01-01"))
            inv_id += 1
cur.executemany("""INSERT OR IGNORE INTO Inventory VALUES (?,?,?,?,?,?,?)""", inventory_rows)
print(f"Inventory: {len(inventory_rows)}")

# =====================================================================
# 8. CUSTOMERS
# =====================================================================
customer_rows = []
for i in range(1, N_CUSTOMERS + 1):
    first, last = fake.first_name(), fake.last_name()
    customer_rows.append((
        i, first, last, f"{first.lower()}.{last.lower()}{i}@example.com",
        fake.numerify("03##-#######"), fake.address().replace("\n", ", "),
        random.choice(ALL_CITY_IDS), "1990-01-01", "Male", "2022-01-01", random.randint(0, 500), "Active"
    ))
cur.executemany("""INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", customer_rows)
print(f"Customers: {len(customer_rows)}")

# =====================================================================
# 9. DISCOUNTS & PROMOTIONS
# =====================================================================
cur.execute("INSERT OR IGNORE INTO Discounts VALUES (1, 'Summer Sale', 'Percentage', 10.0, NULL, NULL, '2023-01-01', '2023-12-31', 'Active')")
cur.execute("INSERT OR IGNORE INTO Promotions VALUES (1, 'Summer Promo', 'Storewide', 'Seasonal', 1, NULL, '2023-01-01', '2023-12-31', 'Active')")

# =====================================================================
# 10. TRANSACTIONS: Orders & OrderItems
#     Pareto distribution for customer orders. Seasonal order volume.
# =====================================================================
# Generate order dates skewed heavily towards recent years and holidays
def generate_order_date():
    days_since_start = (END_DATE - START_DATE).days
    # Right-skewed distribution towards END_DATE
    rand_days = int(np.random.beta(a=3, b=1) * days_since_start)
    dt = datetime.combine(START_DATE + timedelta(days=rand_days), datetime.min.time())
    
    # 20% chance of holiday season (Nov-Dec)
    if random.random() < 0.2:
        dt = datetime(dt.year, random.choice([11, 12]), random.randint(1, 28))
    
    # Add random time of day (skewed to afternoon 1pm - 6pm)
    hour = int(np.random.normal(loc=15, scale=3))
    hour = max(8, min(hour, 22))
    dt += timedelta(hours=hour, minutes=random.randint(0, 59))
    return dt

order_rows = []
order_item_rows = []
payment_rows = []
review_rows = []
return_rows = []

# Customer ordering distribution (Pareto-ish)
# A few customers order 20+ times, many order 1 time.
customer_order_counts = np.random.zipf(1.8, N_CUSTOMERS)
customer_order_counts = np.clip(customer_order_counts, 0, 50)
total_orders_needed = N_ORDERS

pool_of_customers = []
for cid, count in enumerate(customer_order_counts, 1):
    pool_of_customers.extend([cid] * count)

random.shuffle(pool_of_customers)
pool_of_customers = pool_of_customers[:N_ORDERS]

order_id = 1
item_id = 1
payment_id = 1
review_id = 1
return_id = 1

completed_orders_for_returns = []

for cust_id in pool_of_customers:
    branch_id = random.randint(1, N_BRANCHES)
    order_date = generate_order_date()
    
    status_choices = ["Completed", "Completed", "Completed", "Completed", "Pending", "Cancelled"]
    status = random.choice(status_choices)
    
    # Order Items (1 to 6 items per order)
    num_items = random.randint(1, 6)
    order_total = 0.0
    
    for _ in range(num_items):
        # Product popularity follows long-tail
        prod_id = int(np.random.exponential(scale=N_PRODUCTS/5))
        prod_id = max(1, min(prod_id, N_PRODUCTS))
        
        qty = random.randint(1, 3)
        unit_price = product_prices[prod_id]
        discount = 0.0
        if random.random() < 0.1: # 10% chance of discount
            discount = unit_price * 0.1 * qty
            
        line_total = (unit_price * qty) - discount
        order_total += line_total
        
        order_item_rows.append((
            item_id, order_id, prod_id, qty, unit_price, discount, line_total
        ))
        
        # Reviews (10% chance if order is completed)
        if status == "Completed" and random.random() < 0.1:
            rating = random.choices([1, 2, 3, 4, 5], weights=[5, 5, 10, 30, 50])[0]
            review_rows.append((
                review_id, prod_id, cust_id, rating, f"Review for product {prod_id}", order_date + timedelta(days=random.randint(2, 30))
            ))
            review_id += 1
            
        item_id += 1

    payment_method = random.choices(["Credit Card", "Mobile Wallet", "Cash", "Bank Transfer"], weights=[50, 30, 15, 5])[0]
    
    order_rows.append((
        order_id, cust_id, branch_id, order_date.strftime("%Y-%m-%d %H:%M:%S"),
        status, round(order_total, 2), payment_method
    ))
    
    payment_status = "Success" if status == "Completed" else ("Refunded" if status == "Cancelled" else "Pending")
    payment_rows.append((
        payment_id, order_id, payment_method, round(order_total, 2),
        (order_date + timedelta(minutes=random.randint(1, 15))).strftime("%Y-%m-%d %H:%M:%S"),
        payment_status
    ))
    
    if status == "Completed":
        completed_orders_for_returns.append((order_id, cust_id, branch_id, order_date))
        
    payment_id += 1
    order_id += 1

cur.executemany("""INSERT INTO Orders VALUES (?,?,?,?,?,?,?)""", order_rows)
cur.executemany("""INSERT INTO OrderItems VALUES (?,?,?,?,?,?,?)""", order_item_rows)
cur.executemany("""INSERT INTO Payments VALUES (?,?,?,?,?,?)""", payment_rows)
cur.executemany("""INSERT INTO Reviews VALUES (?,?,?,?,?,?)""", review_rows)
print(f"Transactions: {len(order_rows)} Orders, {len(order_item_rows)} Items, {len(payment_rows)} Payments, {len(review_rows)} Reviews")

# =====================================================================
# 11. RETURNS
#     Only generated from completed orders
# =====================================================================
returns_pool = random.sample(completed_orders_for_returns, min(N_RETURNS, len(completed_orders_for_returns)))
for ord_data in returns_pool:
    o_id, c_id, b_id, o_date = ord_data
    return_date = o_date + timedelta(days=random.randint(1, 14))
    
    cur.execute("SELECT product_id, total_price FROM OrderItems WHERE order_id = ? LIMIT 1", (o_id,))
    item = cur.fetchone()
    if item:
        p_id, refund = item
        return_rows.append((
            return_id, o_id, p_id, c_id, b_id,
            random.choice(["Defective", "Wrong Size", "Not Needed", "Damaged in transit"]),
            return_date.strftime("%Y-%m-%d %H:%M:%S"),
            refund,
            "Processed"
        ))
        return_id += 1

cur.executemany("""INSERT INTO Returns VALUES (?,?,?,?,?,?,?,?,?)""", return_rows)
print(f"Returns: {len(return_rows)}")

# =====================================================================
# FINAL COMMIT & PRAGMA
# =====================================================================
conn.commit()
conn.execute("PRAGMA foreign_keys = ON;")
conn.close()

print(f"Data generation complete! Database size: {os.path.getsize(DB_PATH) / (1024*1024):.2f} MB")
