from faker import Faker
import psycopg2
import os
from dotenv import load_dotenv

fake = Faker()
load_dotenv()
db_password = os.getenv('DB_PASSWORD')

conn = psycopg2.connect(host="localhost", port="5432", database="postgres", user="postgres", password=db_password)
cursor = conn.cursor()

def populate_contacts(n):
    for i in range(1, n + 1):
        phone = fake.numerify("###########")  # 11 digit
        address = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        postal_code = fake.zipcode()
        cursor.execute(
            "INSERT INTO Contact (Contact_ID, Phone_Number, Street_Address, City, State, Postal_Code) VALUES (%s, %s, %s, %s, %s, %s)",
            (i, phone, address, city, state, postal_code)
        )
    conn.commit()

def populate_customers(n):
    for i in range(1, n + 1):
        name = fake.name()
        loyalty_points = fake.random_int(min=0, max=1000)
        last_visited_date = fake.date_this_year()
        contact_id = i  # Ensure mapping
        cursor.execute(
            "INSERT INTO Customer (Customer_ID, Loyalty_Points, Name, Last_Visited_Date, Customer_Contact_ID) VALUES (%s, %s, %s, %s, %s)",
            (i, loyalty_points, name, last_visited_date, contact_id)
        )
    conn.commit()

def populate_menu_items(n):
    for i in range(1, n + 1):
        name = fake.word().capitalize()
        description = fake.sentence()
        price = round(fake.random.uniform(5.0, 50.0), 2)
        cursor.execute(
            "INSERT INTO Menu_Items (Menu_Item_ID, Name, Description, Price) VALUES (%s, %s, %s, %s)",
            (i, name, description, price)
        )
    conn.commit()

def populate_branches(n):
    for i in range(1, n + 1):
        branch_contact_id = i  # Ensure Branch maps
        opening_date = fake.date_this_decade()
        cursor.execute(
            "INSERT INTO Branch (Branch_ID, Branch_Contact_ID, Opening_Date) VALUES (%s, %s, %s)",
            (i, branch_contact_id, opening_date)
        )
    conn.commit()

def populate_orders(n):
    for i in range(1, n + 1):
        branch_id = fake.random_int(min=1, max=5)
        customer_id = fake.random_int(min=1, max=10)
        cursor.execute(
            "INSERT INTO Orders (Order_ID, Order_Branch_ID, Order_Customer_ID) VALUES (%s, %s, %s)",
            (i, branch_id, customer_id)
        )
    conn.commit()

def populate_order_details(n):
    for i in range(1, n + 1):
        order_id = fake.random_int(min=1, max=10)
        menu_item_id = fake.random_int(min=1, max=10)
        cursor.execute(
            "INSERT INTO Order_Details (Order_Detail_ID, OD_Order_ID, OD_Menu_Item_ID) VALUES (%s, %s, %s)",
            (i, order_id, menu_item_id)
        )
    conn.commit()

def main():
    populate_contacts(10)
    populate_customers(10)
    populate_menu_items(10)
    populate_branches(5)
    populate_orders(10)
    populate_order_details(10)

if __name__ == '__main__':
    main()

cursor.close()
conn.close()
