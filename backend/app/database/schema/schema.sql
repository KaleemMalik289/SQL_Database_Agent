-- AI Retail Store - Database Schema
-- Ensures referential integrity, strong typing, and query optimization.
-- Compatible with SQLite.

PRAGMA foreign_keys = ON;

-- ==========================================
-- 1. GEOGRAPHY
-- ==========================================
CREATE TABLE IF NOT EXISTS Countries (
    country_id INTEGER PRIMARY KEY,
    country_name TEXT NOT NULL UNIQUE,
    country_code TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS States (
    state_id INTEGER PRIMARY KEY,
    state_name TEXT NOT NULL,
    state_code TEXT NOT NULL,
    country_id INTEGER NOT NULL,
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
);

CREATE TABLE IF NOT EXISTS Cities (
    city_id INTEGER PRIMARY KEY,
    city_name TEXT NOT NULL,
    state_id INTEGER NOT NULL,
    FOREIGN KEY (state_id) REFERENCES States(state_id)
);

-- ==========================================
-- 2. ORGANIZATION
-- ==========================================
CREATE TABLE IF NOT EXISTS Departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Branches (
    branch_id INTEGER PRIMARY KEY,
    branch_name TEXT NOT NULL,
    branch_code TEXT NOT NULL UNIQUE,
    city_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    manager_employee_id INTEGER, -- FK added after Employees
    opening_date DATE NOT NULL,
    branch_size_sqft INTEGER,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (city_id) REFERENCES Cities(city_id)
);

CREATE TABLE IF NOT EXISTS Employees (
    employee_id INTEGER PRIMARY KEY,
    branch_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    manager_id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    job_title TEXT NOT NULL,
    hire_date DATE NOT NULL,
    termination_date DATE,
    salary REAL NOT NULL,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES Employees(employee_id)
);

-- ==========================================
-- 3. CATALOG & SUPPLIERS
-- ==========================================
CREATE TABLE IF NOT EXISTS Suppliers (
    supplier_id INTEGER PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    contact_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    city_id INTEGER,
    rating REAL CHECK (rating >= 0 AND rating <= 5),
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (city_id) REFERENCES Cities(city_id)
);

CREATE TABLE IF NOT EXISTS Categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL,
    parent_category_id INTEGER,
    description TEXT,
    FOREIGN KEY (parent_category_id) REFERENCES Categories(category_id)
);

CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    sku TEXT UNIQUE NOT NULL,
    category_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    brand TEXT,
    unit_of_measure TEXT,
    unit_price REAL NOT NULL,
    cost_price REAL NOT NULL,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- ==========================================
-- 4. OPERATIONS
-- ==========================================
CREATE TABLE IF NOT EXISTS Inventory (
    inventory_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    quantity_on_hand INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 10,
    reorder_quantity INTEGER NOT NULL DEFAULT 50,
    last_restock_date DATE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id),
    UNIQUE(product_id, branch_id)
);

CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    city_id INTEGER,
    date_of_birth DATE,
    gender TEXT,
    registration_date DATE NOT NULL,
    loyalty_points INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (city_id) REFERENCES Cities(city_id)
);

CREATE TABLE IF NOT EXISTS Discounts (
    discount_id INTEGER PRIMARY KEY,
    discount_name TEXT NOT NULL,
    discount_type TEXT NOT NULL, -- Percentage, FixedAmount
    discount_value REAL NOT NULL,
    product_id INTEGER,
    category_id INTEGER,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE IF NOT EXISTS Promotions (
    promotion_id INTEGER PRIMARY KEY,
    promotion_name TEXT NOT NULL,
    description TEXT,
    promotion_type TEXT NOT NULL,
    discount_id INTEGER,
    branch_id INTEGER,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (discount_id) REFERENCES Discounts(discount_id),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id)
);

-- ==========================================
-- 5. TRANSACTIONS (Added for Completion)
-- ==========================================
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    order_date DATETIME NOT NULL,
    status TEXT NOT NULL, -- Completed, Pending, Cancelled, Returned
    total_amount REAL NOT NULL,
    payment_method TEXT NOT NULL, -- Card, Cash, Wallet
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id)
);

CREATE TABLE IF NOT EXISTS OrderItems (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    discount_amount REAL DEFAULT 0,
    total_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE IF NOT EXISTS Payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL UNIQUE,
    payment_method TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_date DATETIME NOT NULL,
    status TEXT NOT NULL, -- Success, Failed, Refunded
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE IF NOT EXISTS Reviews (
    review_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    review_date DATETIME NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE IF NOT EXISTS Returns (
    return_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    return_date DATETIME NOT NULL,
    refund_amount REAL NOT NULL,
    status TEXT NOT NULL, -- Processed, Pending, Rejected
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id)
);

-- ==========================================
-- 6. INDEXES FOR PERFORMANCE
-- ==========================================
CREATE INDEX IF NOT EXISTS idx_products_category ON Products(category_id);
CREATE INDEX IF NOT EXISTS idx_inventory_product_branch ON Inventory(product_id, branch_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON Orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_branch ON Orders(branch_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON OrderItems(order_id);
CREATE INDEX IF NOT EXISTS idx_reviews_product ON Reviews(product_id);
