import sqlite3
import mysql.connector


def connect_to_remote_db():
    try:
        cnx = mysql.connector.connect(
            user="u100003642_sparkle",
            password="123@Sparkle",
            host="srv947.hstgr.io",
            database="u100003642_sparkle",
        )
        cursor = cnx.cursor()
        # Optionally, you can return the connection and cursor objects along with a success flag
        return True, cnx, cursor, None

    except mysql.connector.Error as err:
        # Return False for the success flag and the error message
        return False, None, None, err


def connect_to_local_db():
    try:
        # Connect to SQLite database locally
        cnx = sqlite3.connect("local_database.db")
        cursor = cnx.cursor()
        # Optionally, you can return the connection and cursor objects along with a success flag
        return True, cnx, cursor, None

    except sqlite3.Error as err:
        # Return False for the success flag and the error message
        return False, None, None, err


"""  ====================================================== Testing Part ===============================================  """

if __name__ == "__main__":
    # Attempt to connect to the remote database
    success_remote, cnx_remote, cursor_remote, error_remote = connect_to_remote_db()

    # Check if the connection to the remote database was successful
    if success_remote:
        print("Connection to the remote database successful!")
        # Perform any additional actions here
    else:
        print("Failed to connect to the remote database:", error_remote)

    # Attempt to connect to the local SQLite database
    success_local, cnx_local, cursor_local, error_local = connect_to_local_db()

    # Check if the connection to the local SQLite database was successful
    if success_local:
        print("Connection to the local SQLite database successful!")
        # Perform any additional actions here
    else:
        print("Failed to connect to the local SQLite database:", error_local)
