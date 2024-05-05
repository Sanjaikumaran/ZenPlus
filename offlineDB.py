import sqlite3
import requests
import mysql.connector
from decimal import Decimal
import datetime

from database import database


class Operations:
    def __init__(self):
        # Attempt to establish a connection to the database during object initialization
        self.success, self.connection, self.cursor, self.error = (
            database.connect_to_remote_db()
        )

    @staticmethod
    def check_internet_connection():
        try:
            response = requests.get("http://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def fetch_schema_and_data_from_remote_db(self, table_names, shop_id):
        data = []

        for table_name in table_names:

            # Fetch schema
            self.cursor.execute(f"DESCRIBE {table_name}")
            schema = self.cursor.fetchall()

            # Fetch data
            self.cursor.execute(
                f"SELECT * FROM {table_name} WHERE ShopId = %s", (shop_id,)
            )
            table_data = self.cursor.fetchall()

            # Append schema and data to result
            data.append(
                {"table_name": table_name, "schema": schema, "data": table_data}
            )

        return data

    def insert_data_into_local_db(self, data, table_info):
        # Connect to the local SQLite database
        local_conn = sqlite3.connect("local_database.db")
        local_cursor = local_conn.cursor()

        for table in data:
            table_name = table["table_name"]
            schema = table["schema"]
            table_data = table["data"]

            # Create table if not exists
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            # Construct column definitions
            for col in schema:
                # Remove 'unsigned' from column definition
                col_definition = f"{col[0]} {col[1]}".replace(" unsigned", "")
                create_table_query += f"{col_definition}, "
            create_table_query = create_table_query[:-2] + ")"

            try:
                local_cursor.execute(create_table_query)
                print(f"Table '{table_name}' created successfully.")
            except sqlite3.Error as e:
                print(f"Error creating table '{table_name}': {e}")

            # Insert or update data into local database
            try:
                for row in table_data:
                    # Convert Decimal and datetime.datetime values
                    converted_row = []
                    for value in row:
                        if isinstance(value, Decimal):
                            converted_row.append(float(value))
                        elif isinstance(value, datetime.datetime):
                            converted_row.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            converted_row.append(value)

                    # Check if data already exists based on unique columns
                    select_query = f"SELECT COUNT(*) FROM {table_name} WHERE "
                    criteria = [
                        f"{col[0]} = ?"
                        for col in schema
                        if col[0] in table_info[table_name]
                    ]  # Unique columns as criteria
                    select_query += " AND ".join(criteria)
                    local_cursor.execute(
                        select_query,
                        [
                            converted_row[i]
                            for i in range(len(converted_row))
                            if schema[i][0] in table_info[table_name]
                        ],
                    )
                    row_count = local_cursor.fetchone()[0]

                    if row_count > 0:
                        # If row exists, update it

                        update_query = f"UPDATE {table_name} SET "
                        update_query += ", ".join(f"{col[0]} = ?" for col in schema)
                        update_query += f" WHERE {criteria[0]}"
                        where_index = [col[0] for col in schema].index(criteria[0][:-4])

                        # Print converted_row with the value for the WHERE clause
                        converted_row.append(converted_row[where_index])
                        local_cursor.execute(update_query, converted_row)
                        print(f"Row updated in table '{table_name}' successfully.")
                    else:
                        # If row does not exist, insert it
                        # Construct INSERT INTO query with column names
                        column_names = ", ".join(col[0] for col in schema)
                        placeholders = ", ".join(["?" for _ in schema])
                        insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
                        local_cursor.execute(insert_query, converted_row)
                        print(f"Row inserted into table '{table_name}' successfully.")

                print(
                    f"All data inserted or updated into table '{table_name}' successfully."
                )
            except sqlite3.Error as e:
                print(
                    f"Error inserting or updating data into table '{table_name}': {e}"
                )

        # Commit changes and close connection
        local_conn.commit()
        local_conn.close()

    def main(self):
        table_info = {
            "Customers": {"CustomerID"},
            "Employees": {"EmployeeId"},  # Assuming EmployeeID is the unique column
            "Products": {"ProductId"},  # Assuming ProductID is the unique column
            "Transactions": {
                "TransactionID"
            },  # Assuming TransactionID is the unique column
            "TransactionItems": {
                "TransactionID",
                "ProductID",
            },  # Assuming ItemID is the unique column
        }  # Dictionary containing table names and unique columns

        shop_id = "123"  # Replace with the shop ID you're interested in

        if self.check_internet_connection():
            data = self.fetch_schema_and_data_from_remote_db(table_info, shop_id)
            self.insert_data_into_local_db(data, table_info)
            print("Data inserted into local database successfully.")
        else:
            print("No internet connection. Cannot fetch data from the remote database.")


if __name__ == "__main__":
    Operations().main()
