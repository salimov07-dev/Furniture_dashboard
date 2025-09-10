import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Initialize Faker for generating fake data
fake = Faker()

# Configuration
NUM_PRODUCTS = 50
NUM_CATEGORIES = 10
NUM_ORDERS = 100000
NUM_EMPLOYEES = 50
NUM_CUSTOMERS = 20000
NUM_LEADS = 50000
NUM_CALLS = 150000
LAST_12_MONTHS_START = datetime.now() - timedelta(days=365)

# Realistic Furniture Categories
CATEGORIES = [
    'Sofas', 'Chairs', 'Tables', 'Beds', 'Wardrobes',
    'Cabinets', 'Desks', 'Shelves', 'Lamps', 'Ottomans'
]

# Adjectives and Materials for realistic product names
ADJECTIVES = ['Modern', 'Vintage', 'Classic', 'Ergonomic', 'Luxury', 'Compact', 'Rustic', 'Contemporary', 'Minimalist', 'Industrial']
MATERIALS = ['Leather', 'Fabric', 'Wooden', 'Oak', 'Mahogany', 'Metal', 'Glass', 'Velvet', 'Wicker', 'Rattan']

# Price ranges per category (min, max)
PRICE_RANGES = {
    'Sofas': (300, 1500),
    'Chairs': (50, 400),
    'Tables': (100, 800),
    'Beds': (200, 1200),
    'Wardrobes': (150, 900),
    'Cabinets': (100, 600),
    'Desks': (80, 500),
    'Shelves': (40, 300),
    'Lamps': (20, 200),
    'Ottomans': (50, 300)
}

COUNTRIES = ['Uzbekistan', 'Kazakhstan', 'Russia', 'USA', 'Germany', 'China', 'Turkey', 'India', 'France', 'UK']

# Load SQL Server connection details from .env
SQL_SERVER = os.getenv('SQL_SERVER')
DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DRIVER = os.getenv('DRIVER')

# Validate environment variables
if not all([SQL_SERVER, DATABASE, USERNAME, PASSWORD, DRIVER]):
    raise ValueError("One or more environment variables are missing. Check your .env file.")

# Connection string
conn_str = f'Trusted_Connection=Yes;DRIVER={DRIVER};SERVER={SQL_SERVER};PORT=1433;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

# Function to create tables in SQL Server
def create_tables(conn):
    cursor = conn.cursor()
    # Drop tables if they exist
    cursor.execute("IF OBJECT_ID('Products') IS NOT NULL DROP TABLE Products")
    cursor.execute("IF OBJECT_ID('Employees') IS NOT NULL DROP TABLE Employees")
    cursor.execute("IF OBJECT_ID('Customers') IS NOT NULL DROP TABLE Customers")
    cursor.execute("IF OBJECT_ID('Leads') IS NOT NULL DROP TABLE Leads")
    cursor.execute("IF OBJECT_ID('Orders') IS NOT NULL DROP TABLE Orders")
    cursor.execute("IF OBJECT_ID('Warehouse') IS NOT NULL DROP TABLE Warehouse")
    cursor.execute("IF OBJECT_ID('Production') IS NOT NULL DROP TABLE Production")
    cursor.execute("IF OBJECT_ID('Calls') IS NOT NULL DROP TABLE Calls")

    # Create tables
    cursor.execute("""
        CREATE TABLE Products (
            product_id INT PRIMARY KEY,
            product_name NVARCHAR(100),
            category NVARCHAR(50),
            price FLOAT,
            cost FLOAT
        )
    """)
    cursor.execute("""
        CREATE TABLE Employees (
            employee_id INT PRIMARY KEY,
            name NVARCHAR(100),
            role NVARCHAR(50),
            hire_date DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE Customers (
            customer_id INT PRIMARY KEY,
            name NVARCHAR(100),
            country NVARCHAR(50),
            registration_date DATE,
            purchase_frequency NVARCHAR(20)
        )
    """)
    cursor.execute("""
        CREATE TABLE Leads (
            lead_id INT PRIMARY KEY,
            source NVARCHAR(50),
            date DATE,
            converted BIT,
            customer_id INT
        )
    """)
    cursor.execute("""
        CREATE TABLE Orders (
            order_id INT PRIMARY KEY,
            order_date DATE,
            customer_id INT,
            product_id INT,
            quantity INT,
            total_amount FLOAT,
            seller_id INT,
            delivery_date DATE,
            delayed BIT,
            country NVARCHAR(50)
        )
    """)
    cursor.execute("""
        CREATE TABLE Warehouse (
            product_id INT,
            stock_quantity INT,
            days_in_stock INT,
            manufactured_date DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE Production (
            production_id INT PRIMARY KEY,
            worker_id INT,
            work_date DATE,
            hours_worked FLOAT,
            items_produced INT,
            defects INT,
            product_id INT
        )
    """)
    cursor.execute("""
        CREATE TABLE Calls (
            call_id INT PRIMARY KEY,
            operator_id INT,
            call_date DATE,
            duration_minutes FLOAT,
            customer_rating FLOAT
        )
    """)
    conn.commit()

# Function to generate realistic products
def generate_products():
    products = []
    product_id = 1
    for category in CATEGORIES:
        min_price, max_price = PRICE_RANGES[category]
        for _ in range(NUM_PRODUCTS // NUM_CATEGORIES):
            adjective = random.choice(ADJECTIVES)
            material = random.choice(MATERIALS)
            base_name = category[:-1] if category.endswith('s') else category
            product_name = f"{adjective} {material} {base_name}"
            price = round(random.uniform(min_price, max_price), 2)
            cost = round(price * random.uniform(0.6, 0.8), 2)
            products.append({
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'price': price,
                'cost': cost
            })
            product_id += 1
    return pd.DataFrame(products)

# Function to generate employees
def generate_employees():
    employees = []
    for i in range(NUM_EMPLOYEES):
        is_seller = random.choice([True, False])
        employees.append({
            'employee_id': i+1,
            'name': fake.name(),
            'role': 'Seller' if is_seller else 'Worker',
            'hire_date': fake.date_between(start_date='-5y', end_date='today')
        })
    return pd.DataFrame(employees)

# Function to generate customers
def generate_customers():
    customers = []
    for i in range(NUM_CUSTOMERS):
        customers.append({
            'customer_id': i+1,
            'name': fake.name(),
            'country': random.choice(COUNTRIES),
            'registration_date': fake.date_between(start_date=LAST_12_MONTHS_START, end_date='today'),
            'purchase_frequency': random.choice(['One-time', 'Regular'])
        })
    return pd.DataFrame(customers)

# Function to generate leads
def generate_leads():
    leads = []
    sources = ['Website', 'Social Media', 'Referral', 'Ad', 'Email']
    for i in range(NUM_LEADS):
        leads.append({
            'lead_id': i+1,
            'source': random.choice(sources),
            'date': fake.date_between(start_date=LAST_12_MONTHS_START, end_date='today'),
            'converted': random.choice([True, False]),
            'customer_id': random.randint(1, NUM_CUSTOMERS) if random.choice([True, False]) else None
        })
    return pd.DataFrame(leads)

# Function to generate orders
def generate_orders(products_df, customers_df, employees_df):
    orders = []
    sellers = employees_df[employees_df['role'] == 'Seller']['employee_id'].tolist()
    for i in range(NUM_ORDERS):
        order_date = fake.date_between(start_date=LAST_12_MONTHS_START, end_date='today')
        delivery_date = order_date + timedelta(days=random.randint(1, 10))
        delayed = delivery_date > order_date + timedelta(days=5)
        quantity = random.randint(1, 10)
        product = products_df.sample(1).iloc[0]
        orders.append({
            'order_id': i+1,
            'order_date': order_date,
            'customer_id': random.choice(customers_df['customer_id']),
            'product_id': product['product_id'],
            'quantity': quantity,
            'total_amount': round(quantity * product['price'], 2),
            'seller_id': random.choice(sellers),
            'delivery_date': delivery_date,
            'delayed': delayed,
            'country': random.choice(COUNTRIES)
        })
    return pd.DataFrame(orders)

# Function to generate warehouse data
def generate_warehouse(products_df):
    warehouse = []
    for _, product in products_df.iterrows():
        stock = random.randint(50, 500)
        days_in_stock = random.randint(1, 100)
        warehouse.append({
            'product_id': product['product_id'],
            'stock_quantity': stock,
            'days_in_stock': days_in_stock,
            'manufactured_date': datetime.now() - timedelta(days=days_in_stock)
        })
    for i in range(1000):
        product = products_df.sample(1).iloc[0]
        warehouse.append({
            'product_id': product['product_id'],
            'stock_quantity': random.randint(0, 100),
            'days_in_stock': random.randint(1, 200),
            'manufactured_date': fake.date_between(start_date=LAST_12_MONTHS_START, end_date='today')
        })
    return pd.DataFrame(warehouse)

# Function to generate worker production
def generate_production(employees_df, products_df):
    production = []
    workers = employees_df[employees_df['role'] == 'Worker']['employee_id'].tolist()
    for i in range(50000):
        work_date = fake.date_between(start_date=LAST_12_MONTHS_START, end_date='today')
        worker_id = random.choice(workers)
        hours_worked = round(random.uniform(6, 10), 1)
        items_produced = random.randint(1, 20)
        defects = random.randint(0, 3) if random.random() < 0.1 else 0
        product = products_df.sample(1).iloc[0]
        production.append({
            'production_id': i+1,
            'worker_id': worker_id,
            'work_date': work_date,
            'hours_worked': hours_worked,
            'items_produced': items_produced,
            'defects': defects,
            'product_id': product['product_id']
        })
    return pd.DataFrame(production)

# Function to generate call center data
def generate_calls(employees_df):
    operators = employees_df.sample(20)['employee_id'].tolist()
    calls = []
    for i in range(NUM_CALLS):
        call_date = fake.date_between(start_date=LAST_12_MONTHS_START, end_date='today')
        duration = round(random.uniform(1, 15), 1)
        rating = round(random.uniform(1, 5), 1)
        calls.append({
            'call_id': i+1,
            'operator_id': random.choice(operators),
            'call_date': call_date,
            'duration_minutes': duration,
            'customer_rating': rating
        })
    return pd.DataFrame(calls)

# Function to insert DataFrame to SQL Server
def insert_to_sql(df, table_name, conn):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        row = row.where(pd.notnull(row), None)
        placeholders = ','.join(['?' for _ in row])
        columns = ','.join(row.index)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))
    conn.commit()

# Main function
def main():
    try:
        # Connect to SQL Server
        conn = pyodbc.connect(conn_str)
        print("Connection successful!")
        
        # Create tables
        create_tables(conn)
        
        # Generate data with realistic products
        products_df = generate_products()
        employees_df = generate_employees()
        customers_df = generate_customers()
        leads_df = generate_leads()
        orders_df = generate_orders(products_df, customers_df, employees_df)
        warehouse_df = generate_warehouse(products_df)
        production_df = generate_production(employees_df, products_df)
        calls_df = generate_calls(employees_df)
        
        # Insert data into SQL Server
        print("Inserting Products...")
        insert_to_sql(products_df, 'Products', conn)
        print("Inserting Employees...")
        insert_to_sql(employees_df, 'Employees', conn)
        print("Inserting Customers...")
        insert_to_sql(customers_df, 'Customers', conn)
        print("Inserting Leads...")
        insert_to_sql(leads_df, 'Leads', conn)
        print("Inserting Orders...")
        insert_to_sql(orders_df, 'Orders', conn)
        print("Inserting Warehouse...")
        insert_to_sql(warehouse_df, 'Warehouse', conn)
        print("Inserting Production...")
        insert_to_sql(production_df, 'Production', conn)
        print("Inserting Calls...")
        insert_to_sql(calls_df, 'Calls', conn)
        
        print("Realistic data generated and inserted into SQL Server successfully!")
        
        # Close connection
        conn.close()
        
    except pyodbc.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()