import mysql.connector
from database import database


class Operations:
    def __init__(self):
        # Attempt to establish a connection to the database during object initialization

        self.success, self.connection, self.cursor, self.error = (
            database.connect_to_db()
        )

    def insert_row(self, table_name, column_values):
        if self.success:
            try:
                # Construct the INSERT query dynamically
                insert_query = f"INSERT INTO {table_name} ("
                insert_query += ", ".join(column_values.keys())
                insert_query += ") VALUES ("
                insert_query += ", ".join(["%s" for _ in column_values])
                insert_query += ")"

                # Prepare values for the query
                query_values = list(column_values.values())

                # Execute the INSERT query with the provided data
                self.cursor.execute(insert_query, query_values)

                # Commit the changes
                self.connection.commit()

                print("Row inserted successfully.")

            except mysql.connector.Error as err:
                print("Error:", err)

            finally:
                # Close cursor and connection
                if self.cursor:
                    self.cursor.close()
                if self.connection:
                    self.connection.close()

    def update_row(self, table_name, update_values, where_conditions):
        if self.success:
            try:
                # Construct the SET clause dynamically
                set_clause = ", ".join(
                    [f"{column} = %s" for column in update_values.keys()]
                )

                # Construct the WHERE clause dynamically
                where_clause = " AND ".join(
                    [f"{column} = %s" for column in where_conditions.keys()]
                )

                # Construct the UPDATE query dynamically
                update_query = (
                    f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                )

                # Prepare values for the query
                query_values = list(update_values.values()) + list(
                    where_conditions.values()
                )

                # Execute the UPDATE query with the provided data
                with self.connection.cursor() as cursor:
                    cursor.execute(update_query, query_values)

                # Commit the changes
                self.connection.commit()

                print(f"Rows updated successfully.")

            except mysql.connector.Error as err:
                # Handle the error gracefully
                print("Error:", err)

            finally:
                # Close connection
                if self.connection:
                    self.connection.close()

    def remove_row(self, table_name, condition_dict):
        if self.success:
            try:
                # Construct the DELETE query
                delete_query = f"DELETE FROM {table_name}"

                # Check if any conditions are provided
                if condition_dict:
                    # Construct the WHERE clause based on the conditions
                    where_clause = " AND ".join(
                        [f"{column} = %s" for column in condition_dict.keys()]
                    )
                    delete_query += f" WHERE {where_clause}"

                    # Execute the DELETE query with the condition values
                    self.cursor.execute(delete_query, tuple(condition_dict.values()))

                else:
                    # If no conditions provided, delete all rows
                    self.cursor.execute(delete_query)

                # Commit the changes
                self.connection.commit()

                print("Rows deleted successfully.")

            except mysql.connector.Error as err:
                print("Error:", err)

            finally:
                # Close cursor and connection
                if self.cursor:
                    self.cursor.close()
                if self.connection:
                    self.connection.close()

    def list_table(self, table_name, column_values):
        # Check if the connection is successful
        if self.success:
            # Perform database operations using the connection and cursor
            try:
                # Example: Execute SQL queries
                self.cursor.execute(f"SELECT {column_values} FROM {table_name}")
                rows = self.cursor.fetchall()
                for row in rows:
                    print(row)

            finally:
                # Close the cursor and connection when done
                if self.cursor:
                    self.cursor.close()
                if self.connection:
                    self.connection.close()
        else:
            # Handle the case when connection fails
            print("Database connection failed. Error:", self.error)


"""  ====================================================== Testing Part ===============================================  """

if __name__ == "__main__":
    import time

    # Create an instance of the Operations class
    ops = Operations()
    current_time = time.time()

    ops.list_table("ShopList", "ShopId,Branch")

    # ops.remove_row("ShopList", "Branch", "asd")

    # ops.insert_row(
    #    table_name="ShopList",
    #    column_values={
    #        "TimeStamp": time.strftime(
    #            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
    #        ),
    #        "ShopId": "12345",
    #        "EmailAddress": "example@example.com",
    #        "Password": "password123",
    #        "GSTNo": "ABCDE1234F",
    #        "MobileNumber": "9876543210",
    #        "ShopName": "Example Shop",
    #        "OwnerName": "John Doe",
    #        "Branch": "Main Branch",
    #        "WebsiteURL": "http://example.com",
    #        "GreetingsMessage": "Welcome to our shop!",
    #    },
    # )

    # ops.update_row(
    #    update_values={
    #        "EmailAddress": "new_email@example.com",
    #        "ShopName": "New Shop Name",
    #    },
    #    where_column="ShopId",
    #    where_value="2024002141724590",
    # )
