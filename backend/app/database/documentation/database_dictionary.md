# AI Retail Store - Database Dictionary
**Version:** 1.0.0  
**Database Type:** SQLite3  
**Size:** ~20.7 MB  
**Tables:** 16  
**Total Records:** ~300,000+

## 1. Overview
The AI Retail Store database is a fully relational, enterprise-grade synthetic dataset designed to test and benchmark the LangChain AI SQL Database Agent. It features realistic long-tail distributions, seasonal order patterns, and strict referential integrity.

---

## 2. Entity Relationship Groups

### 2.1 Geography
* `Countries`: Defines the root operating country (Pakistan).
* `States`: Administrative regions.
* `Cities`: Operating cities where branches and suppliers are located.

### 2.2 Organization & HR
* `Departments`: Functional areas within the company (Sales, HR, IT, etc).
* `Branches`: Physical store locations spanning multiple cities. Includes size, opening dates, and a designated manager.
* `Employees`: The workforce. Features a hierarchical `manager_id` foreign key back to itself, department assignments, branch assignments, and realistic salaries.

### 2.3 Catalog & Supply Chain
* `Suppliers`: Third-party vendors supplying products, featuring ratings and active statuses.
* `Categories`: A recursive table (`parent_category_id`) allowing infinite depth of product classification (e.g. Electronics -> Audio -> Headphones).
* `Products`: The core SKU catalog. 2,000 products linked to suppliers and categories, with unit prices and cost prices.

### 2.4 Inventory & Logistics
* `Inventory`: A composite mapping of `Products` to `Branches`. Tracks `quantity_on_hand` and `reorder_levels`. Designed with occasional zero-stock anomalies to test AI reasoning.

### 2.5 Customers & Marketing
* `Customers`: 10,000 registered users with demographic data and loyalty points. Registration dates span years to allow cohort analysis.
* `Discounts`: Defined discount rules (Percentage or FixedAmount) that can apply to specific Products or whole Categories.
* `Promotions`: High-level marketing campaigns (e.g., "Summer Sale") that optionally tie to Discounts and Branches.

### 2.6 Transactions (The Core Load)
* `Orders`: The central transaction header. 50,000 records. Generated using a Pareto distribution (a small set of highly loyal customers placing many orders, while most place few).
* `OrderItems`: The line items for each order. ~174,000 records. Product selection uses a long-tail exponential distribution to simulate best-sellers.
* `Payments`: The financial settlement for orders.
* `Reviews`: 11,000+ customer reviews on products, heavily skewed toward 3-5 stars for realism. Only generated for 'Completed' orders.
* `Returns`: 5,000 reverse-logistics records. Only eligible on 'Completed' orders.

---

## 3. Notable SQL Agent Query Patterns
This schema was explicitly designed to support complex, multi-join analytical queries from the AI Agent:

1. **Top Performers (Multi-Join Aggregation)**
   > *"Which branch manager oversees the branch with the highest total revenue this year?"*
   > Requires joining Employees -> Branches -> Orders.

2. **Supply Chain Risks (Filtering & Grouping)**
   > *"List all suppliers who provide products that are currently out of stock (quantity_on_hand = 0) in more than 3 branches."*
   > Requires joining Suppliers -> Products -> Inventory.

3. **Customer Cohort Analysis (Date Math)**
   > *"What is the average order value for customers who registered in 2022 versus 2023?"*
   > Requires joining Customers -> Orders.

4. **Product Margins (Arithmetic)**
   > *"Which top-level category has the highest average profit margin (unit_price - cost_price)?"*
   > Requires joining Categories -> Products and handling the recursive parent category logic.
