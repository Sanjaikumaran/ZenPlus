# CREATE TABLE SalesStatistics (
#    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
#    Date DATE,
#    ProductID INT,
#    Quantity INT,
#    TotalPrice DECIMAL(10, 2),
#    CustomerID INT,
#    PaymentMethod VARCHAR(50),
#    Discount DECIMAL(10, 2),
#    Tax DECIMAL(10, 2),
#    NetSales DECIMAL(10, 2),
#    Profit DECIMAL(10, 2),
#    EmployeeID INT,
#    LocationID INT
# );

from database import operations
import time


class sales_stats_management:
    def __init__(self):
        self.ops = operations.Operations()
        # Get the current time
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

    def add_transaction(
        self,
        shop_id,
        product_id,
        quantity,
        total_price,
        customer_id,
        payment_method,
        discount,
        tax,
        net_sales,
        profit,
        employee_id,
        location_id,
    ):
        # Define the column values as a dictionary
        column_values = {
            "ShopId": shop_id,
            "Timestamp": self.current_time,
            "ProductID": product_id,
            "Quantity": quantity,
            "TotalPrice": total_price,
            "CustomerID": customer_id,
            "PaymentMethod": payment_method,
            "Discount": discount,
            "Tax": tax,
            "NetSales": net_sales,
            "Profit": profit,
            "EmployeeID": employee_id,
            "LocationID": location_id,
        }

        # Call the insert_row method with the table name and column values
        self.ops.insert_row("SalesStatistics", column_values)
        self.ops.close_cursor_connection(self.ops.cursor, self.ops.connection)

    def update_transaction(
        self,
        transaction_id,
        updated_values,
    ):
        # Define the where conditions to identify the row to be updated
        where_conditions = {"TransactionID": transaction_id}

        # Call the update_row method with the table name, updated values, and where conditions
        self.ops.update_row("SalesStatistics", updated_values, where_conditions)
        self.ops.close_cursor_connection(self.ops.cursor, self.ops.connection)

    def remove_transaction(self, transaction_id):
        # Define the where conditions to identify the row to be removed
        where_conditions = {"TransactionID": transaction_id}

        # Call the remove_row method with the table name and where conditions
        self.ops.remove_row("SalesStatistics", where_conditions)
        self.ops.close_cursor_connection(self.ops.cursor, self.ops.connection)


if __name__ == "__main__":
    # Assuming you have an instance of your class named `shop_management_instance`
    # and `add_transaction` method is defined within that class
    sales_stats_management = sales_stats_management()
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
    sales_stats_management.add_transaction(**transaction_data)
    # update_data = {
    #    "Quantity": 3,  # New quantity
    #    "TotalPrice": 60.00,  # New total price
    #    "Discount": 10.00,  # New discount
    # }

    ## Call the update_transaction method with the transaction ID and updated values
    # sales_stats_management.update_transaction(1, update_data)

    # sales_stats_management.remove_transaction(1)
