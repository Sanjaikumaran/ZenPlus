from database import *
import time


class shop_management:
    def __init__(self):
        # Create an instance of the Operations class
        self.ops = operations.Operations()

        # Get the current time
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

    def add_shop(
        self,
        shop_id,
        email_address,
        password,
        gst_no,
        mobile_number,
        shop_name,
        owner_name,
        branch,
        website_url,
        greetings_message,
    ):
        # Define the column values as a dictionary
        column_values = {
            "TimeStamp": self.current_time,
            "ShopId": shop_id,
            "EmailAddress": email_address,
            "Password": password,
            "GSTNo": gst_no,
            "MobileNumber": mobile_number,
            "ShopName": shop_name,
            "OwnerName": owner_name,
            "Branch": branch,
            "WebsiteURL": website_url,
            "GreetingsMessage": greetings_message,
        }

        # Call the insert_row method with the table name and column values
        self.ops.insert_row("ShopList", column_values)


"""  ====================================================== Testing Part ===============================================  """
if __name__ == "__main__":
    shop_management().add_shop(
        12213,
        "asdasasd2SFS@SD",
        "SADAS",
        "4321SDD",
        2342342234,
        "SKSJOP",
        "SK",
        "DDF",
        "EERE.CO",
        "SDF",
    )
