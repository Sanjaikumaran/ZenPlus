import sqlite3
import requests
import mysql.connector
from decimal import Decimal
import datetime


class Operations:
    def __init__(self):
        # Attempt to establish connections to the databases during object initialization
        self.local_conn = sqlite3.connect("local_database.db")
        self.local_cursor = self.local_conn.cursor()

        self.remote_conn = mysql.connector.connect(
            user="u100003642_sparkle",
            password="123@Sparkle",
            host="srv947.hstgr.io",
            database="u100003642_sparkle",
        )
        self.remote_cursor = self.remote_conn.cursor()

    @staticmethod
    def check_internet_connection():
        try:
            response = requests.get("http://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def fetch_data_from_local_db(self, table_names):
        data = []

        for table_name in table_names:
            # Fetch column names
            self.local_cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in self.local_cursor.fetchall()]

            # Fetch data
            self.local_cursor.execute(f"SELECT * FROM {table_name}")
            table_data = self.local_cursor.fetchall()

            # Append table name, column names, and data to result
            data.append(
                {"table_name": table_name, "columns": columns, "data": table_data}
            )

        return data

    def insert_data_into_remote_db(self, data, primary_key_column):
        for table in data:
            table_name = table["table_name"]
            columns = table["columns"]
            table_data = table["data"]

            # Insert or update data into remote database
            try:
                # Convert Decimal and datetime.datetime values
                converted_data = []
                for row in table_data:
                    converted_row = []
                    for value in row:
                        if isinstance(value, Decimal):
                            converted_row.append(float(value))
                        elif isinstance(value, datetime.datetime):
                            converted_row.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            converted_row.append(value)
                    converted_data.append(converted_row)

                # Insert or update data
                for row in converted_data:
                    placeholders = ", ".join(["%s" for _ in columns])
                    update_clause = ", ".join([f"`{col}` = %s" for col in columns[1:]])
                    insert_query = f"INSERT INTO `{table_name}` ({', '.join(columns)}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_clause}"
                    self.remote_cursor.execute(insert_query, row)
                    print(
                        f"Row inserted or updated in table '{table_name}' successfully."
                    )

                print(
                    f"All data inserted or updated in table '{table_name}' successfully."
                )
                self.remote_conn.commit()
            except Exception as e:
                print(
                    f"Error inserting or updating data into table '{table_name}': {e}"
                )

    def main(self):
        table_names = [
            "Products",
            "Customers",
            "Employees",
            "SalesStatistics",
            # Add all your table names here
        ]
        primary_key_column = "ShopId"  # Specify the primary key column name

        if self.check_internet_connection():
            data = self.fetch_data_from_local_db(table_names)
            self.insert_data_into_remote_db(data, primary_key_column)
            print("Data inserted or updated in remote database successfully.")
        else:
            print(
                "No internet connection. Cannot insert or update data in the remote database."
            )


if __name__ == "__main__":
    Operations().main()
