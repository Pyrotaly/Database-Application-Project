import hashlib
import requests

BASE_URL = "http://127.0.0.1:5000"

# -- Backend, Ignore -- #
def create_index():
    response = requests.post(f"{BASE_URL}/create_index")
    if response.status_code == 200:
        print("Index creation.")
    else:
        print(f"Failed index creation: {response.status_code}")

def password_request():
    password = input("Enter password: ")
    password_encoded = password.encode()
    hashed_password = hashlib.md5(password_encoded)

    hex_digest = hashed_password.hexdigest()
    
    print(f"Your hashed password is: {hex_digest}")
# -- Baackend, Ignore -- #

def add_customer_and_contact():
    # Get contact
    contact_id = input("Enter Contact ID: (int)")
    phone_number = input("Enter Phone Number: (11 Char)")
    street_address = input("Enter Street Address: ")
    city = input("Enter City: ")
    state = input("Enter State: (2 Char)")
    postal_code = input("Enter Postal Code: (5 Char)")
    
    contact_data = {
        "contact_id": contact_id,
        "phone_number": phone_number,
        "street_address": street_address,
        "city": city,
        "state": state,
        "postal_code": postal_code
    }

    # Send contact data
    contact_response = requests.post(f"{BASE_URL}/contacts", json=contact_data)
    if contact_response.status_code != 201:
        print(f"Failed to add contact: {contact_response.status_code}")
        return
    
    # Get customer
    customer_id = input("Enter Customer ID: ")
    name = input("Enter Customer Name: ")
    loyalty_points = input("Enter Loyalty Points: ")
    last_visited_date = input("Enter Last Visited Date (YYYY-MM-DD): ")
    
    customer_data = {
        "customer_id": customer_id,
        "name": name,
        "loyalty_points": loyalty_points,
        "last_visited_date": last_visited_date,
        "contact_id": contact_id
    }

    # Send customer data
    customer_response = requests.post(f"{BASE_URL}/customers", json=customer_data)
    if customer_response.status_code == 201 or 200:
        print(f"Customer '{name}' and contact added successfully. {customer_response.status_code}")
    else:
        print(f"Failed to add customer: {customer_response.status_code}")

def add_contact():
    contact_id = input("Enter Contact ID: (int)")
    phone_number = input("Enter Phone Number: (11 Char)")
    street_address = input("Enter Street Address: ")
    city = input("Enter City: ")
    state = input("Enter State: (2 Char)")
    postal_code = input("Enter Postal Code: (5 Char)")
    
    data = {
        "contact_id": contact_id,
        "phone_number": phone_number,
        "street_address": street_address,
        "city": city,
        "state": state,
        "postal_code": postal_code
    }

    response = requests.post(f"{BASE_URL}/contacts", json=data)
    if response.status_code == 201:
        print(f"Contact with ID {contact_id} added successfully.")
    else:
        print(f"Failed to add contact: {response.status_code}")

def add_customer():
    customer_id = input("Enter Customer ID: ")
    name = input("Enter Customer Name: ")
    loyalty_points = input("Enter Loyalty Points: ")
    last_visited_date = input("Enter Last Visited Date (YYYY-MM-DD): ")
    contact_id = input("Enter Contact ID: ")
    
    data = {
        "customer_id": customer_id,
        "name": name,
        "loyalty_points": loyalty_points,
        "last_visited_date": last_visited_date,
        "contact_id": contact_id
    }

    response = requests.post(f"{BASE_URL}/customers", json=data)
    if response.status_code == 201:
        print(f"Customer '{name}' added successfully.")
    else:
        print(f"Failed to add customer: {response.status_code}")

def get_all_customers():
    response = requests.get(f"{BASE_URL}/customers")
    if response.status_code == 200:
        customers = response.json()
        print("\n--- Customers ---")
        for customer in customers:
            print(f"ID: {customer['customer_id']}, Name: {customer['name']}, Points: {customer['loyalty_points']}")
    else:
        print(f"Failed to fetch customers: {response.status_code}")

def update_customer_loyalty():
    customer_id = input("Enter Customer ID: ")
    loyalty_points = input("Enter Loyalty Points: ")
    last_visited_date = input("Enter Last Visited Date (YYYY-MM-DD): ")

    data = {
        "customer_id": customer_id,
        "loyalty_points": loyalty_points,
        "last_visited_date": last_visited_date
    }

    response = requests.put(f"{BASE_URL}/customers/loyalty", json=data)

    if response.status_code == 200:
        print(f"Loyalty points updated for Customer ID {data['customer_id']}.")
    else:
        print(f"Failed to update loyalty points: {response.status_code}")

def get_top_loyal_customers():
    response = requests.get(f"{BASE_URL}/customers/top-loyal")
    if response.status_code == 200:
        top_customers = response.json()
        print("\n--- Top Loyal Customers ---")
        for customer in top_customers:
            print(f"ID: {customer['customer_id']}, Name: {customer['name']}, Points: {customer['loyalty_points']}")
    else:
        print(f"Failed to get top loyal customers: {response.status_code}")

def get_sales_of_each_branch():
    branch_id = input("Please enter the branch ID: ")
    response = requests.get(f"{BASE_URL}/report/branch-sales/{branch_id}")
    if response.status_code == 200:
        sales_report = response.json()
        print("\n--- Branch Sales ---")
        for item in sales_report:
            print(
                f"Menu Item ID: {item['menu_item_id']}, "
                f"Item Name: {item['menu_item_name']}, "
                f"Total Sold: {item['total_sold']}, "
                f"Total Sales: ${item['total_sales']:.2f}"
            )
    else:
        print(f"Failed to get branch sales: {response.status_code}")

def get_sales_at_branch():
    response = requests.get(f"{BASE_URL}/report/branch-performance")
    if response.status_code == 200:
        branch_performance = response.json()
        print("\n--- Branch Performance ---")
        for branch in branch_performance:
            print(f"Branch ID: {branch['branch_id']}, Total Sales: ${branch['total_sales']}, Items Sold: {branch['total_items_sold']}, Avg Sales per Item: ${branch['avg_sales_per_item']}")
    else:
        print(f"Failed to get branch performance: {response.status_code}")
    pass

def get_number_of_times_item_ordered():
    response = requests.get(f"{BASE_URL}/menu-items/order-count")
    if response.status_code == 200:
        item_orders = response.json()
        print("\n--- Menu Item Order Counts ---")
        for item in item_orders:
            print(f"Menu Item ID: {item['Menu_Item_ID']}, Name: {item['Menu_Item_Name']}, Times Ordered: {item['Times_Ordered']}")
    else:
        print(f"Failed to get menu item order counts: {response.status_code}")

def delete_customer():
    customer_id = input("Enter the customer ID to delete: ")
    try:
        customer_id = int(customer_id)
    except ValueError:
        print("Invalid customer ID.")
        return

    response = requests.delete(f"{BASE_URL}/del_customers/{customer_id}")
    
    if response.status_code == 200:
        print(f"Customer with ID {customer_id} deleted successfully.")
    else:
        print(f"Failed to delete customer: {response.status_code}")

def special_5_query_join():
    response = requests.get(f"{BASE_URL}/report/customer-orders")
    if response.status_code == 200:
        report = response.json()
        print("\n--- Customer Orders Report ---")
        for row in report:
            print(f"Customer ID: {row['customer_id']}, Customer Name: {row['customer_name']}, Order ID: {row['order_id']}, Item: {row['menu_item_name']}, Price: ${row['item_price']}")
    else:
        print(f"Failed to fetch customer orders report: {response.status_code}")

def main():
    print("=== Mock Up Login ===")
    password_request()

    print("=== 431W CLI Frontend ===")
    print("1. Add Customer and Contact")
    print("2. Add Customer")
    print("3. Add Contact")
    print("4. Get All Customers")
    print("5. Update Customer Loyalty Points")
    print("6. Get Top 5 Customers with Highest Loyalty Points")
    print("7. Get Sales of Each Branch")
    print("8. Get Sales at a Branch")
    print("9. Get Number of Times a Menu Item Was Ordered")
    print("10. Delete a Customer")
    print("11. Special 5 Table Join Query")

    choice = input("Select an option: ")

    if choice == "1":
        add_customer_and_contact()
    elif choice == "2":
        add_customer()
    elif choice == "3":
        add_contact()
    elif choice == "4":
        get_all_customers()
    elif choice == "5":
        update_customer_loyalty()
    elif choice == "6":
        get_top_loyal_customers()
    elif choice == "7":
        get_sales_of_each_branch()
    elif choice == "8":
        get_sales_at_branch()
    elif choice == "9":
        get_number_of_times_item_ordered()
    elif choice == "10":
        delete_customer()
    elif choice == "11":
        special_5_query_join()
    elif choice == "12": # Hidden backend  
        create_index()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
