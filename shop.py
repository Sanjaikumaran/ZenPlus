from database import database, operations
import time
import sys

sys.path.append("../")


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

    def remove_shop(self, shop_id, shop_name):
        condition_dict = {"ShopId": shop_id, "ShopName": shop_name}
        self.ops.remove_row("ShopList", condition_dict)

    def update_shop(self, updated_values, where_conditions):
        # 'where_conditions' is a dictionary where keys are column names and values are values to match
        self.ops.update_row("ShopList", updated_values, where_conditions)


"""  ====================================================== Testing Part ===============================================  """
if __name__ == "__main__":
    # shop_management().add_shop(
    #    12213,
    #    "asdasasd2SFS@SD",
    #    "SADAS",
    #    "4321SDD",
    #    2342342234,
    #    "SKSJOP",
    #    "SK",
    #    "DDF",
    #    "EERE.CO",
    #    "SDF",
    # )
    # shop_management().remove_shop(12213, "SKSJOP")
    shop_management().update_shop(
        updated_values={"ShopName": "SKSHOP", "OwnerName": "SK"},
        where_conditions={"Password": "password23"},
    )
