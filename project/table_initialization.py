import psycopg2

conn = psycopg2.connect(host="localhost", port="5432", database="postgres", user="postgres", password="1234")
cursor = conn.cursor()

tables = [
    """
    CREATE TABLE IF NOT EXISTS Contact (
        Contact_ID Int PRIMARY KEY,
        Phone_Number Char(11),
        Street_Address Varchar(255),
        City Varchar(255),
        State Char(2),
        Postal_Code Varchar(5)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Branch (
        Branch_ID Int PRIMARY KEY,
        Manager_ID Int,
        Branch_Contact_ID Int,
        Opening_Date Date,
        FOREIGN KEY (Manager_ID) REFERENCES Employee(Employee_ID),
        FOREIGN KEY (Branch_Contact_ID) REFERENCES Contact(Contact_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Employee (
        Employee_ID Int PRIMARY KEY,
        Supervisor_ID Int,
        Name Varchar(255),
        Position Text,
        Hire_Date Date,
        Salary Float,
        Employee_Contact_ID Int,
        E_Shift_ID Int,
        E_Branch_ID Int,
        FOREIGN KEY (Employee_Contact_ID) REFERENCES Contact(Contact_ID),
        FOREIGN KEY (E_Shift_ID) REFERENCES Shift(Shift_ID),
        FOREIGN KEY (E_Branch_ID) REFERENCES Branch(Branch_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Shift (
        Shift_ID Int PRIMARY KEY,
        Shift_Start Time,
        Shift_End Time,
        S_Employee_ID Int,
        S_Branch_ID Int,
        FOREIGN KEY (S_Employee_ID) REFERENCES Employee(Employee_ID),
        FOREIGN KEY (S_Branch_ID) REFERENCES Branch(Branch_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Financial_Transactions (
        Transaction_ID Int PRIMARY KEY,
        Amount Float,
        Branch_ID Int,
        Transaction_Date Date,
        FOREIGN KEY (Branch_ID) REFERENCES Branch(Branch_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Customer (
        Customer_ID Int PRIMARY KEY,
        Loyalty_Points Int,
        Name Varchar(255),
        Last_Visited_Date Date,
        Customer_Contact_ID Int,
        FOREIGN KEY (Customer_Contact_ID) REFERENCES Contact(Contact_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Orders (
        Order_ID Int PRIMARY KEY,
        Order_Branch_ID Int,
        Order_Customer_ID Int,
        Order_Transaction_ID Int,
        FOREIGN KEY (Order_Branch_ID) REFERENCES Branch(Branch_ID),
        FOREIGN KEY (Order_Customer_ID) REFERENCES Customer(Customer_ID), 
        FOREIGN KEY (Order_Transaction_ID) REFERENCES Financial_Transactions(Transaction_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Menu_Items (
        Menu_Item_ID Int PRIMARY KEY,
        Name Varchar(255),
        Description Text,
        Price Float
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Order_Details (
        Order_Detail_ID Int PRIMARY KEY,
        OD_Order_ID Int,
        OD_Menu_Item_ID Int,
        FOREIGN KEY (OD_Order_ID) REFERENCES Orders(Order_ID), 
        FOREIGN KEY (OD_Menu_Item_ID) REFERENCES Menu_Items(Menu_Item_ID)
    );
    """
]

for query in tables:
    cursor.execute(query)
    
conn.commit()

cursor.close()
conn.close()