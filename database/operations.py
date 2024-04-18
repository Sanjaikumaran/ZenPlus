import mysql.connector
from database import database


class Operations:
    def __init__(self):
        # Attempt to establish a connection to the local database during object initialization
        (
            self.success_local,
            self.connection_local,
            self.cursor_local,
            self.error_local,
        ) = database.connect_to_local_db()

    def create_table(self, table_name, column_definitions):
        if self.success_local:
            try:
                # Define the SQL query to create the table
                create_table_query = f"CREATE TABLE {table_name} ({column_definitions})"

                # Execute the query on local database
                self.cursor_local.execute(create_table_query)

                # Commit the transaction
                self.connection_local.commit()

                return "Table created successfully"
            except sqlite3.Error as err:
                print("Error:", err)

    def delete_table(self, table_name):
        if self.success_local:
            try:
                # Define the SQL query to delete the table
                drop_table_query = f"DROP TABLE {table_name}"

                # Execute the query on local database
                self.cursor_local.execute(drop_table_query)

                # Commit the transaction
                self.connection_local.commit()

                return "Table deleted successfully"
            except sqlite3.Error as err:
                print("Error:", err)

    def insert_row(self, table_name, column_values):
        if self.success_local:
            try:
                # Construct the INSERT query dynamically
                insert_query = f"INSERT INTO {table_name} ("
                insert_query += ", ".join(column_values.keys())
                insert_query += ") VALUES ("
                insert_query += ", ".join(["?" for _ in column_values])
                insert_query += ")"

                # Prepare values for the query
                query_values = list(column_values.values())

                # Execute the INSERT query with the provided data on local database
                self.cursor_local.execute(insert_query, query_values)

                # Commit the transaction
                self.connection_local.commit()

                print("Row inserted successfully.")

            except sqlite3.Error as err:
                print("Error:", err)

    def update_row(self, table_name, update_values, where_conditions):
        if self.success_local:
            try:
                # Construct the SET clause dynamically
                set_clause = ", ".join(
                    [f"{column} = ?" for column in update_values.keys()]
                )

                # Construct the WHERE clause dynamically
                where_clause = " AND ".join(
                    [f"{column} = ?" for column in where_conditions.keys()]
                )

                # Construct the UPDATE query dynamically
                update_query = (
                    f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                )

                # Prepare values for the query
                query_values = list(update_values.values()) + list(
                    where_conditions.values()
                )

                # Execute the UPDATE query with the provided data on local database
                self.cursor_local.execute(update_query, query_values)

                # Commit the transaction
                self.connection_local.commit()

                print(f"Rows updated successfully.")

            except sqlite3.Error as err:
                # Handle the error gracefully
                print("Error:", err)

    def remove_row(self, table_name, condition_dict):
        if self.success_local:
            try:
                # Construct the DELETE query
                delete_query = f"DELETE FROM {table_name}"

                # Check if any conditions are provided
                if condition_dict:
                    # Construct the WHERE clause based on the conditions
                    where_clause = " AND ".join(
                        [f"{column} = ?" for column in condition_dict.keys()]
                    )
                    delete_query += f" WHERE {where_clause}"

                    # Execute the DELETE query with the condition values on local database
                    self.cursor_local.execute(
                        delete_query, tuple(condition_dict.values())
                    )

                else:
                    # If no conditions provided, delete all rows on local database
                    self.cursor_local.execute(delete_query)

                # Commit the transaction
                self.connection_local.commit()

                print("Rows deleted successfully.")

            except sqlite3.Error as err:
                print("Error:", err)

    def list_table(self, table_name, column_values):
        if self.success_local:
            try:
                # Execute SQL query
                self.cursor_local.execute(f"SELECT {column_values} FROM {table_name}")
                rows = self.cursor_local.fetchall()
                for row in rows:
                    print(row)

            except sqlite3.Error as err:
                print("Error:", err)

    def select_row(self, table_name, columns, where_conditions):
        if self.success_local:
            try:
                # Construct the WHERE clause dynamically
                where_clause = " AND ".join(
                    [f"{column} = ?" for column in where_conditions.keys()]
                )

                # Construct the SELECT query dynamically
                select_query = (
                    f"SELECT {columns} FROM {table_name} WHERE {where_clause}"
                )

                # Prepare values for the query
                query_values = list(where_conditions.values())

                # Execute the SELECT query with the provided conditions on local database
                self.cursor_local.execute(select_query, query_values)
                row = self.cursor_local.fetchone()
                if row:
                    return row
                else:
                    print("No matching row found.")

            except sqlite3.Error as err:
                # Handle the error gracefully
                print("Error:", err)

    def close_cursor_connection(self):
        if self.cursor_local:
            self.cursor_local.close()
        if self.connection_local:
            self.connection_local.close()


"""  ====================================================== Testing Part ===============================================  """

if __name__ == "__main__":
    import time

    # Create an instance of the Operations class
    ops = Operations()
    current_time = time.time()

    # Perform operations on both remote and local databases
    ops.create_table(
        "your_table_name", "id SERIAL PRIMARY KEY, name VARCHAR(50), age INT"
    )

    ops.insert_row(
        table_name="your_table_name", column_values={"name": "John", "age": 30}
    )

    ops.update_row(
        table_name="your_table_name",
        update_values={"age": 35},
        where_conditions={"name": "John"},
    )

    ops.remove_row(table_name="your_table_name", condition_dict={"name": "John"})

    ops.list_table("your_table_name", "id, name, age")

    ops.select_row(
        table_name="your_table_name",
        columns="id, name, age",
        where_conditions={"age": 35},
    )

    # Close connections to both databases
    ops.close_cursor_connection(ops.cursor_remote, ops.connection_remote)
    ops.close_cursor_connection(ops.cursor_local, ops.connection_local)
