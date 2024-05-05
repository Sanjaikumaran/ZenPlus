from database import database, operations
import time


class CustomerManagement:
    def __init__(self):
        # Create an instance of the Operations class
        self.ops = operations.Operations()
        # Get the current time
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

    def list_customers(self):
        columns = "CustomerID,FirstName,LastName,Email,Phone,Address,City,Country"

        return self.ops.list_table("Customers", columns)

    def get_customer(self, customer_id):

        # Define the columns you want to retrieve
        columns = "*"

        # Define the conditions to filter the customer
        where_conditions = {"CustomerID": customer_id}

        # Execute the SELECT query to get the customer
        return self.ops.select_row("Customers", columns, where_conditions)

    def add_customer(self, customer_data):
        # Set the timestamp
        customer_data["Timestamp"] = self.current_time
        # Call insert_row method to add customer record
        if self.ops.insert_row("Customers", customer_data):
            return True
        else:
            return False

    def update_customer(self, customer_id, updated_values):
        # Define the where conditions to identify the row to be updated
        where_conditions = {"CustomerID": customer_id}

        # Call the update_row method with the table name, updated values, and where conditions
        if self.ops.update_row("Customers", updated_values, where_conditions):
            return True
        else:
            return False

    def remove_customer(self, customer_id):
        # Define the where conditions to identify the row to be removed
        where_conditions = {"CustomerID": customer_id}

        # Call the remove_row method with the table name and where conditions
        if self.ops.remove_row("Customers", where_conditions):
            return True
        else:
            return False


if __name__ == "__main__":
    # Create an instance of the CustomerManagement class
    customer_manager = CustomerManagement()
    # Example data for a customer
    customer_data = {
        "ShopID": "SHOP123",  # Sample shop ID
        "FirstName": "John",
        "LastName": "Doe",
        "Email": "john.doe@example.com",
        "Phone": "1234567890",
        "Address": "123 Main Street",
        "City": "Anytown",
        "Country": "CountryName",
    }

    # Call the add_customer method with the customer data
    customer_manager.add_customer(customer_data)
