import sqlite3


def list_data_from_sqlite(table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()

    try:
        # Execute a SELECT query
        cursor.execute(f"SELECT * FROM {table_name}")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Print the fetched rows
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print("Error fetching data:", e)

    finally:
        # Close the database connection
        conn.close()


import sqlite3


def delete_duplicate_rows(table_name, unique_column):
    # Connect to the SQLite database
    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()

    try:
        # Construct the SQL query to create a temporary table with duplicate rows
        temp_table_query = f"""
            CREATE TEMPORARY TABLE TempTable AS
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY {unique_column} ORDER BY (SELECT NULL)) AS rn
            FROM {table_name};
        """

        # Execute the temporary table creation query
        cursor.execute(temp_table_query)

        # Construct the SQL query to delete duplicate rows using the temporary table
        delete_query = f"""
            DELETE FROM {table_name}
            WHERE ROWID NOT IN (
                SELECT MIN(ROWID)
                FROM TempTable
                GROUP BY {unique_column}
            );
        """

        # Execute the delete query
        cursor.execute(delete_query)
        conn.commit()
        print("Duplicate rows deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting duplicate rows: {e}")

    # Close the connection
    conn.close()


# Call the function to list data

for _ in ["Products", "Customers", "Employees", "Transactions", "TransactionItems"]:
    # delete_duplicate_rows(_, "SNo")
    # if _ == "Transactions":
    list_data_from_sqlite(_)
    print("avlodha\n")
