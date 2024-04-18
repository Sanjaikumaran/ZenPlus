# CREATE TABLE Customers (
#    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
#    FirstName VARCHAR(50),
#    LastName VARCHAR(50),
#    Email VARCHAR(100),
#    Phone VARCHAR(20),
#    Address VARCHAR(255),
#    City VARCHAR(100),
#    Country VARCHAR(100)
# );


from database import operations
import time


class CustomerManagement:
    def __init__(self):
        # Initialize database operations instance
        self.ops = operations.Operations()

        # Get current timestamp
        self.current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Method to add a new customer
    def add_customer(self, customer_data):
        # Call insert_row method to add customer record
        self.ops.insert_row("Customers", customer_data)

    # Method to update a customer record
    def update_customer(self, customer_id, updated_values):
        # Define where conditions to identify the row to be updated
        where_conditions = {"CustomerID": customer_id}

        # Call update_row method to update customer record
        self.ops.update_row("Customers", updated_values, where_conditions)

    # Method to remove a customer record
    def remove_customer(self, customer_id):
        # Define where conditions to identify the row to be removed
        where_conditions = {"CustomerID": customer_id}

        # Call remove_row method to remove customer record
        self.ops.remove_row("Customers", where_conditions)

    # Additional methods for customer-related operations can be defined here


if __name__ == "__main__":
    # Create an instance of the CustomerManagement class
    customer_management = CustomerManagement()

    # Add a new customer
    customer_data = {
        "CustomerID": 3,
        "ShopId": "123",
        "FirstName": "Alice",
        "LastName": "Smith",
        "Email": "alice@example.com",
        "Phone": "1234567890",
        "Address": "123 Main St",
        "City": "New York",
        "Country": "USA",
    }
    customer_management.add_customer(customer_data)

    # Update an existing customer
    # updated_values = {"Phone": "9876543210"}
    # customer_management.update_customer(1, updated_values)

    ## Remove a customer
    # customer_management.remove_customer(1)
