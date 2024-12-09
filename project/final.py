from flask import Flask, request, jsonify
from dotenv import load_dotenv
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>431W Project</h1>", 200

def get_db_connection():
    load_dotenv()
    db_password = os.getenv('DB_PASSWORD')
    return psycopg2.connect(host="localhost", port="5432", database="postgres", user="postgres", password=db_password)

def create_index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_customer_id ON Orders(Order_Customer_ID);")
    conn.commit()
    conn.close()
    print("Index created.")

# Endpoint for index creation
@app.route('/create_index', methods=['POST'])
def create_index_endpoint():
    create_index()
    return jsonify({"d": "Index endpoint good."}), 200

# Query Type 1: Adding Contact
@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.json
    contact_id = data.get('contact_id')
    phone_number = data.get('phone_number')
    street_address = data.get('street_address')
    city = data.get('city')
    state = data.get('state')
    postal_code = data.get('postal_code')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Contact (Contact_ID, Phone_Number, Street_Address, City, State, Postal_Code)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, 
    (contact_id, phone_number, street_address, city, state, postal_code))
    conn.commit()
    conn.close()
    return jsonify({"d": f"Contact with ID {contact_id} added."}), 201

# Query Type 1: Adding Customer
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    customer_id = data.get('customer_id')
    name = data.get('name')
    loyalty_points = data.get('loyalty_points')
    last_visited_date = data.get('last_visited_date')
    contact_id = data.get('contact_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Customer (Customer_ID, Name, Loyalty_Points, Last_Visited_Date, Customer_Contact_ID)
        VALUES (%s, %s, %s, %s, %s)
    """, 
    (customer_id, name, loyalty_points, last_visited_date, contact_id))
    conn.commit()
    conn.close()
    return jsonify({"d": f"Customer '{name}' added."}), 201

# Query Type 1: Adding Customer and Contact
@app.route('/customers', methods=['POST'])
def add_customer_and_contact():
    data = request.json
    customer_id = data.get('customer_id')
    name = data.get('name')
    loyalty_points = data.get('loyalty_points')
    last_visited_date = data.get('last_visited_date')
    contact_id = data.get('contact_id')
    phone_number = data.get('phone_number')
    street_address = data.get('street_address')
    city = data.get('city')
    state = data.get('state')
    postal_code = data.get('postal_code')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        conn.autocommit = 0
        
        # Check if the contact already exists
        cursor.execute("SELECT COUNT(*) FROM Contact WHERE Contact_ID = %s", (contact_id,))
        exists_contact = cursor.fetchone()[0] > 0
        
        if exists_contact:
            return jsonify({"d": f"Contact {contact_id} already exists."}), 400
        
        # Insert new contact
        cursor.execute(""" 
            INSERT INTO Contact (Contact_ID, Phone_Number, Street_Address, City, State, Postal_Code)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, 
        (contact_id, phone_number, street_address, city, state, postal_code))

        # Check if the customer already exists
        cursor.execute("SELECT COUNT(*) FROM Customer WHERE Customer_ID = %s", (customer_id,))
        exists_customer = cursor.fetchone()[0] > 0
        
        if exists_customer:
            return jsonify({"d": f"Customer with ID {customer_id} already exists."}), 400
        
        # Insert new customer
        cursor.execute("""
            INSERT INTO Customer (Customer_ID, Name, Loyalty_Points, Last_Visited_Date, Customer_Contact_ID)
            VALUES (%s, %s, %s, %s, %s)
        """, 
        (customer_id, name, loyalty_points, last_visited_date, contact_id))

        conn.commit()
        return jsonify({"d": f"Customer '{name}' and contact added."}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"d": "Error happened, rollback"}), 500

    finally:
        conn.close()

# Query Type 2: Getting All Customers in Database
@app.route('/customers', methods=['GET'])
def get_all_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer;")
    customers = cursor.fetchall()
    conn.close()
    
    # a list of lists
    customer_list = []
    for customer in customers:
        customer_list.append({
            "customer_id": customer[0],
            "loyalty_points": customer[1],
            "name": customer[2],
            "last_visited_date": customer[3],
            "contact_id": customer[4]
        })
    return jsonify(customer_list)

# Query Type 3: Update customer loyalty
@app.route('/customers/loyalty', methods=['PUT'])
def update_customer_loyalty():
    data = request.json
    customer_id = data.get('customer_id')
    loyalty_points = data.get('loyalty_points')
    last_visited_date = data.get('last_visited_date')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE Customer
        SET Loyalty_Points = Loyalty_Points + %s, Last_Visited_Date = %s
        WHERE Customer_ID = %s
    """, 
    (loyalty_points, last_visited_date, customer_id))
    conn.commit()
    conn.close()
    
    return jsonify({"d": f"Loyalty points and last visited date updated for Customer {customer_id}."}), 200

# Query Type 4: Top 5 Customer Loyalty Points
@app.route('/customers/top-loyal', methods=['GET'])
def get_top_loyal_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT Customer_ID, Name, Loyalty_Points
        FROM Customer
        ORDER BY Loyalty_Points DESC
        LIMIT 5;
        """)
    result = cursor.fetchall()
    conn.close()

    top_customers = []
    for row in result:
        top_customers.append({
            "customer_id": row[0],
            "name": row[1],
            "loyalty_points": row[2]
        })
    
    return jsonify(top_customers)

# Query Type 5: Sales of each branch
@app.route('/report/branch-sales/<int:branch_id>', methods=['GET'])
def get_branch_sales(branch_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            m.Menu_Item_ID,
            m.Name AS Menu_Item_Name,
            COUNT(od.OD_Menu_Item_ID) AS Total_Sold,
            SUM(m.Price) AS Total_Sales
        FROM Branch b
        JOIN Orders o ON b.Branch_ID = o.Order_Branch_ID
        JOIN Order_Details od ON o.Order_ID = od.OD_Order_ID
        JOIN Menu_Items m ON od.OD_Menu_Item_ID = m.Menu_Item_ID
        WHERE b.Branch_ID = %s
        GROUP BY m.Menu_Item_ID
        ORDER BY Total_Sold DESC;
        """, 
    (branch_id,))
    result = cursor.fetchall()
    conn.close()

    report = []
    for row in result:
        report.append({
            "menu_item_id": row[0],
            "menu_item_name": row[1],
            "total_sold": row[2],
            "total_sales": round(row[3], 2)
        })
    
    return jsonify(report)

# Query Type 6: Sales at a branch
@app.route('/report/branch-performance', methods=['GET'])
def get_branch_performance():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            b.Branch_ID,
            SUM(m.Price) AS Total_Sales,
            COUNT(od.OD_Menu_Item_ID) AS Total_Items_Sold,
            SUM(m.Price) / COUNT(od.OD_Menu_Item_ID) AS Avg_Sales_Per_Item
        FROM Branch b
        JOIN Orders o ON b.Branch_ID = o.Order_Branch_ID
        JOIN Order_Details od ON o.Order_ID = od.OD_Order_ID
        JOIN Menu_Items m ON od.OD_Menu_Item_ID = m.Menu_Item_ID
        GROUP BY b.Branch_ID
        ORDER BY Avg_Sales_Per_Item DESC;
        """)
    result = cursor.fetchall()
    conn.close()

    performance_data = []
    for row in result:
        performance_data.append({
            "branch_id": row[0],
            "total_sales": row[1],
            "total_items_sold": row[2],
            "avg_sales_per_item": round(row[3], 2)
        })
    
    return jsonify(performance_data)

# Query type 7: Number of times each menu item was ordered 
@app.route('/menu-items/order-count', methods=['GET'])
def get_menu_item_order_count():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.Menu_Item_ID,
            m.Name AS Menu_Item_Name,
            COUNT(od.OD_Menu_Item_ID) AS Times_Ordered
        FROM
            Menu_Items m
        LEFT JOIN
            Order_Details od ON m.Menu_Item_ID = od.OD_Menu_Item_ID
        GROUP BY
            m.Menu_Item_ID, m.Name
        ORDER BY
            Times_Ordered DESC;
    """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    menu_items = []
    for row in result:
        menu_item = {
            'Menu_Item_ID': row[0],
            'Menu_Item_Name': row[1],
            'Times_Ordered': row[2]
        }
        menu_items.append(menu_item)
    
    return jsonify(menu_items)

# Query type 8: Deleting a Customer
@app.route('/del_customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM customer WHERE customer_ID = %s", (customer_id,))
    exists = cursor.fetchone()[0] > 0
    
    if not exists:
        return jsonify({"d": f"Customer with ID {customer_id} does not exist."}), 404
    
    cursor.execute("DELETE FROM customer WHERE customer_ID = %s", (customer_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"d": f"customer with ID {customer_id} deleted."}), 200

# Query type 9: 5 table join query
@app.route('/report/customer-orders', methods=['GET'])
def get_customer_order_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.Customer_ID AS Customer_ID,
            c.Name AS Customer_Name,
            o.Order_ID AS Order_ID,
            m.Menu_Item_ID AS Menu_Item_ID,
            m.Name AS Menu_Item_Name,
            m.Price AS Item_Price,
            b.Branch_ID AS Branch_ID
        FROM customer c
        JOIN Orders o ON c.Customer_ID = o.Order_Customer_ID
        JOIN Order_Details od ON o.Order_ID = od.OD_Order_ID
        JOIN Menu_Items m ON od.OD_Menu_Item_ID = m.Menu_Item_ID
        JOIN Branch b ON o.Order_Branch_ID = b.Branch_ID
        ORDER BY c.Customer_ID, o.Order_ID;
        """)
    result = cursor.fetchall()
    conn.close()

    report = []
    for row in result:
        report.append({
            "customer_id": row[0],
            "customer_name": row[1],
            "order_id": row[2],
            "menu_item_id": row[3],
            "menu_item_name": row[4],
            "item_price": row[5],
            "branch_id": row[6],
        })
    
    return jsonify(report)


if __name__ == '__main__':
    app.run(debug=True)
    