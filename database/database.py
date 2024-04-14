import mysql.connector


def connect_to_db():
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


"""  ====================================================== Testing Part ===============================================  """

if __name__ == "__main__":
    # Attempt to connect to the database
    success, cnx, cursor, error = connect_to_db()

    # Check if the connection was successful
    if success:
        print("Connection to the database successful!")
        # Perform any additional actions here
    else:
        print("Failed to connect to the database:", error)
