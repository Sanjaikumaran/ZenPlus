from database import database, operations
import time


class sales_stats_management:
    def __init__(self):
        # Create an instance of the Operations class
        self.ops = operations.Operations()
        # Get the current time
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

    def list_transactions(self):
        columns = "TransactionID,Timestamp,Quantity,TotalPrice,CustomerID,PaymentMethod,Discount,Tax,NetSales,Profit,EmployeeID,LocationID"

        return self.ops.list_table("Transactions", columns)

    def get_transaction(self, transaction_id):

        # Define the columns you want to retrieve
        columns = "*"

        # Define the conditions to filter the employee
        where_conditions = {"TransactionID": transaction_id}

        # Execute the SELECT query to get the employee
        return self.ops.select_row("Transactions", columns, where_conditions)

    def add_transaction(self, transaction_data):
        transaction_data["Timestamp"] = self.current_time
        # Call insert_row method to add transaction record

        if self.ops.insert_row("Transactions", transaction_data):
            return True
        else:
            return False

    def update_transaction(self, transaction_id, updated_values):
        # Define the where conditions to identify the row to be updated
        where_conditions = {"TransactionID": transaction_id}
        print(where_conditions, updated_values)
        # Call the update_row method with the table name, updated values, and where conditions
        if self.ops.update_row("Transactions", updated_values, where_conditions):
            return True
        else:
            return False

    def remove_transaction(self, transaction_id):
        # Define the where conditions to identify the row to be removed
        where_conditions = {"TransactionID": transaction_id}

        # Call the remove_row method with the table name and where conditions
        if self.ops.remove_row("Transactions", where_conditions):
            return True
        else:
            return False


if __name__ == "__main__":
    # Create an instance of the sales_stats_management class
    sales_stats_manager = sales_stats_management()
    # Example data for a transaction
    transaction_data = {
        "shop_id": 123,  # Sample shop ID
        "product_id": 456,  # Sample product ID
        "quantity": 2,
        "total_price": 50.00,
        "customer_id": 789,  # Sample customer ID
        "payment_method": "Credit Card",
        "discount": 5.00,
        "tax": 2.50,
        "net_sales": 47.50,
        "profit": 20.00,
        "employee_id": 101,  # Sample employee ID
        "location_id": 201,  # Sample location ID
    }

    # Call the add_transaction method with the transaction data
    sales_stats_manager.add_transaction(**transaction_data)
