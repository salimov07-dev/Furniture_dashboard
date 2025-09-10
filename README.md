Overview
This project generates synthetic data for a Power BI Dashboard designed for a furniture store, as per the technical specifications provided. The dashboard visualizes key business metrics, including sales, delivery, warehouse status, employee performance, customer leads, and call center analytics. The data is generated using Python and stored in a SQL Server database, ready for integration with Power BI to create an interactive and visually appealing dashboard.
The project meets the requirements for:

Data Volume: Minimum 100,000 order records covering the last 12 months.
Analysis Areas: Sales, delivery, warehouse, employees, customers, leads, and call center performance.
Power BI Features: Bookmarks, drill-through, page navigation, and dynamic tooltips.
Design: Custom background created in Figma (wood texture, neutral colors) for a professional look.


Features
The generated dataset supports the following analyses in Power BI:

Sales Analysis:

Total sales volume and revenue by product and category.
Dynamic ranking of top and bottom-selling products.
Monthly sales trends.


Delivery Metrics:

Average delivery days by product and country.
On-time vs. delayed deliveries (SLA: 5 days).
Export share by country (visualized on a map).


Warehouse Status:

Current stock levels and days in storage.
Highlight products stored for over 60 days.
Comparison of manufactured vs. stored products.


Employee Performance:

Monthly sales by seller.
Daily production by workers (by category).
Average working hours compared to an 8-hour benchmark.
Defect rates for quality analysis.


Customer and Leads:

Lead funnel by source (e.g., website, social media).
Purchase frequency (one-time vs. regular customers).
New potential customers per month.


Call Center Analysis:

Operator working hours and customer ratings.
Identification of top-performing operators based on ratings and call duration.




Project Structure
The repository contains the following components:

Python Script (main.py): Generates synthetic data and inserts it into a SQL Server database.
SQL Server Database (Furniture_project): Stores the generated data in tables: Products, Employees, Customers, Leads, Orders, Warehouse, Production, and Calls.
Figma Design: Custom background image (wood texture, neutral colors) in PNG/SVG format for Power BI dashboard.
Power BI File (FurnitureDashboard.pbix): The Power BI dashboard file (to be created by the user based on the generated data).
Technical Specification (TechSpec.docx): The project requirements document.


Prerequisites
To run the data generation script and set up the project, ensure you have the following:

Python 3.8+ with the following packages:
bashpip install pandas numpy faker pyodbc

SQL Server: Installed and running (local or remote). SQL Server Management Studio (SSMS) is recommended for database management.
ODBC Driver: {ODBC Driver 17 for SQL Server} installed. Download from Microsoft.
Power BI Desktop: For creating and visualizing the dashboard.
Figma: For designing and exporting the custom background.


Setup Instructions

Clone the Repository:
bashgit clone https://github.com/your-username/furniture-store-dashboard.git
cd furniture-store-dashboard

Configure SQL Server:

Create a database named Furniture_project in SQL Server:
sqlCREATE DATABASE Furniture_project;

Ensure SQL Server is configured for SQL Server Authentication (or use Windows Authentication).
Update the connection details in main.py:
pythonSQL_SERVER = 'localhost'  # Replace with your server name or IP
DATABASE = 'Furniture_project'  # Database name
USERNAME = 'sa'  # SQL Server username
PASSWORD = 'your_secure_password'  # SQL Server password
DRIVER = '{ODBC Driver 17 for SQL Server}'  # Verify driver name



Run the Data Generation Script:

Execute the Python script to generate and insert data into SQL Server:
bashpython main.py

The script creates tables and populates them with synthetic data for 50 products, 100,000 orders, 50 employees, 20,000 customers, 50,000 leads, and 150,000 call records.


Verify Data in SQL Server:

Use SSMS to connect to the Furniture_project database and verify tables (e.g., SELECT * FROM Products).


Create the Power BI Dashboard:

Open Power BI Desktop and connect to the SQL Server database (Furniture_project).
Import the tables and create relationships based on keys (e.g., product_id, customer_id).
Design the dashboard using the provided Figma background and implement required features (bookmarks, drill-through, etc.).


Export Figma Background:

Open the Figma design file (not included in this repository; create your own with wood texture and neutral colors).
Export the background as PNG or SVG and apply it in Power BI.




Data Schema
The generated data is stored in the following SQL Server tables:

Products:

product_id (INT, PK), product_name (NVARCHAR), category (NVARCHAR), price (FLOAT), cost (FLOAT)


Employees:

employee_id (INT, PK), name (NVARCHAR), role (NVARCHAR), hire_date (DATE)


Customers:

customer_id (INT, PK), name (NVARCHAR), country (NVARCHAR), registration_date (DATE), purchase_frequency (NVARCHAR)


Leads:

lead_id (INT, PK), source (NVARCHAR), date (DATE), converted (BIT), customer_id (INT)


Orders:

order_id (INT, PK), order_date (DATE), customer_id (INT), product_id (INT), quantity (INT), total_amount (FLOAT), seller_id (INT), delivery_date (DATE), delayed (BIT), country (NVARCHAR)


Warehouse:

product_id (INT), stock_quantity (INT), days_in_stock (INT), manufactured_date (DATE)


Production:

production_id (INT, PK), worker_id (INT), work_date (DATE), hours_worked (FLOAT), items_produced (INT), defects (INT), product_id (INT)


Calls:

call_id (INT, PK), operator_id (INT), call_date (DATE), duration_minutes (FLOAT), customer_rating (FLOAT)




Power BI Dashboard Requirements
The dashboard must include:

Bookmarks: For switching between summary and detailed views.
Drill-through: At least one drill-through page (e.g., product details).
Navigation: User-friendly buttons for page transitions.
Conditional Formatting: Highlight products stored over 60 days in the warehouse.
Visuals: KPI cards, tornado charts, maps for export analysis, and funnel charts for leads.
Design: Use the Figma background with sufficient contrast and hierarchical page layout.

Optional Features

Financial analysis (profit margins, discounts).
Geo heat map for export locations.
AI-based forecasting (e.g., using Python Prophet or Power BI Forecast).
Mobile-optimized view.
Dark/light theme switching via bookmarks.
Alerts for high defect rates.
Customer segmentation (one-time vs. regular buyers).


Deliverables

FurnitureDashboard.pbix: The Power BI dashboard file.
TechSpec.docx: The technical specification document.
background.png/svg: The Figma-designed background image.
SQL Server database (Furniture_project) with populated data.


Troubleshooting

SQL Server Connection Issues:

Ensure the SQL Server service is running and the server is accessible.
Verify the ODBC driver ({ODBC Driver 17 for SQL Server}) is installed.
Check firewall settings (port 1433 for remote connections).
Use Windows Authentication if SQL Server Authentication fails:
pythonconn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={DATABASE};Trusted_Connection=Yes'



Slow Data Insertion:

The script uses row-by-row insertion for reliability. For faster performance, consider bulk insert methods (contact the developer for assistance).


Power BI Data Import:

Ensure correct table relationships in Power BI (e.g., product_id joins Products and Orders).




Contributing
This project is for educational purposes and follows the provided technical specifications. Contributions are welcome for improving data generation, optimizing performance, or enhancing the dashboard design. Please submit a pull request or open an issue for suggestions.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or support, contact the project developer at salimovmironshoh07@gmail.com.

Generated on September 7, 2025, at 05:40 PM +05.