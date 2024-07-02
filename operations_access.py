from database import database, operations
import time


class DataManagement:
    def __init__(self):
        # Create an instance of the Operations class
        self.ops = operations.Operations()
        # Get the current time
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

    def list_items(self, table_name, columns):

        return self.ops.list_table(table_name, columns)

    def add_item(self, table_name, item_data):

        if self.ops.insert_row(table_name, item_data):
            return True
        else:
            return False

    def update_item(self, table_name, where_conditions, updated_values):

        if self.ops.update_row(table_name, updated_values, where_conditions):
            return True
        else:
            return False

    def remove_item(self, table_name, where_conditions):

        if self.ops.remove_row(table_name, where_conditions):
            return True
        else:
            return False

    def get_last_item(self, table_name, column_name):

        return self.ops.get_last_row(table_name, column_name)

    def get_item(self, table_name, column_names, where_conditions):
        result = self.ops.select_row(table_name, column_names, where_conditions)
        if result:
            return result
        else:
            return False

    def get_holded_items(self, table_name, column_names, where_conditions):
        result = self.ops.select_row(table_name, column_names, where_conditions)
        if result:
            return result

        else:
            return False
