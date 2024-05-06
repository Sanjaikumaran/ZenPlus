from database import database, operations
import time


class TransactionItemManagement:
    def __init__(self):
        # Create an instance of the Operations class
        self.ops = operations.Operations()
        # Get the current time
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

    # Other methods...

    def list_transaction_items(self):
        columns = (
            " TransactionID, ProductID, Quantity, Price, Discount, Amount, Taxes, Total"
        )

        return self.ops.list_table("TransactionItems", columns)

    def get_transaction_item(self, transaction_id, product_id):

        # Define the columns you want to retrieve
        columns = "*"

        # Define the conditions to filter the transaction item
        where_conditions = {"TransactionID": transaction_id, "ProductID": product_id}

        # Execute the SELECT query to get the transaction item
        return self.ops.select_row("TransactionItems", columns, where_conditions)

    def add_transaction_item(self, item_data):
        # Call insert_row method to add transaction item record

        if self.ops.insert_row("TransactionItems", item_data):
            return True
        else:
            return False

    def update_transaction_item(self, transaction_id, product_id, updated_values):
        # Define the where conditions to identify the row to be updated
        where_conditions = {"TransactionID": transaction_id, "ProductID": product_id}

        # Call the update_row method with the table name, updated values, and where conditions
        if self.ops.update_row("TransactionItems", updated_values, where_conditions):
            return True
        else:
            return False

    def remove_transaction_item(self, transaction_id, product_id):
        # Define the where conditions to identify the row to be removed
        where_conditions = {"TransactionID": transaction_id, "ProductID": product_id}

        # Call the remove_row method with the table name and where conditions
        if self.ops.remove_row("TransactionItems", where_conditions):
            return True
        else:
            return False
