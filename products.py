from database import database, operations


class product_management:
    def __init__(self):
        # Create an instance of the Operations class 2024002141724590
        self.ops = operations.Operations()

    def list_products(self):
        return self.ops.list_table(
            "Products",
            "ProductName, ProductId, Brand, CostPrice, SellingPrice, MRP, Discount, CurrentStock, HistoryStock, SoldStock, GST",
        )

        # self.ops.close_cursor_connection()

    def add_product(
        self,
        shop_id,
        brand,
        product_name,
        product_id,
        cost_price,
        selling_price,
        mrp,
        discount,
        current_stock,
        history_stock,
        sold_stock,
        gst,
    ):
        # Define the column values as a dictionary
        column_values = {
            "ShopId": shop_id,
            "Brand": brand,
            "ProductName": product_name,
            "ProductId": product_id,
            "CostPrice": cost_price,
            "SellingPrice": selling_price,
            "MRP": mrp,
            "Discount": discount,
            "CurrentStock": current_stock,
            "HistoryStock": history_stock,
            "SoldStock": sold_stock,
            "GST": gst,
        }

        # Call the insert_row method with the table name and column values
        result = self.ops.insert_row("Products", column_values)
        if result:
            return True
        else:
            return False
        # self.ops.close_cursor_connection()

    def remove_product(self, shop_id, product_id):
        condition_dict = {"ShopId": shop_id, "ProductId": product_id}
        result = self.ops.remove_row("Products", condition_dict)
        if result:
            return result
        else:
            return False
        # self.ops.close_cursor_connection(self.ops.cursor, self.ops.connection)

    def update_product(self, shop_id, product_id, updated_values):
        where_conditions = {"ShopId": shop_id, "ProductId": product_id}
        result = self.ops.update_row("Products", updated_values, where_conditions)
        if result:
            return True
        else:
            return False
        # self.ops.close_cursor_connection(self.ops.cursor, self.ops.connection)

    def update_history_stock(self, shop_id, product_id, updated_value):
        # Fetch the current history stock from the database
        current_history_stock = self.ops.select_row(
            "Products", "HistoryStock", {"ShopId": shop_id, "ProductId": product_id}
        )

        if current_history_stock is not None:
            # Extract the current history stock from the result
            current_history_stock = current_history_stock[0]

            # Calculate the updated history stock by adding the updated value to the current history stock
            updated_history_stock = current_history_stock + updated_value

            # Prepare the updated values dictionary
            updated_values = {"HistoryStock": updated_history_stock}

            # Update the history stock in the database
            self.ops.update_row(
                "Products", updated_values, {"ShopId": shop_id, "ProductId": product_id}
            )

            # Close cursor and connection
            # self.ops.close_cursor_connection(self.ops.cursor, self.ops.connection)
        else:
            # Handle the case where the current history stock could not be fetched
            print(
                "Failed to fetch current history stock for shop_id:",
                shop_id,
                "and product_id:",
                product_id,
            )


"""  ====================================================== Testing Part ===============================================  """
if __name__ == "__main__":

    # Create an instance of the product_management class
    product_manager = product_management()
    # print(product_manager.list_products()[0])
    # Call the add_product function
    # product_manager.add_product(
    #    SNo="2",
    #    shop_id="123",
    #    brand="Example Brand",
    #    product_name="Example Product",
    #    product_id="PROD123",
    #    cost_price=10.50,
    #    selling_price=15.99,
    #    mrp=20.00,
    #    current_stock=100,
    #    history_stock=500,
    #    sold_stock=400,
    #    gst=5.00,
    # )

    # Call the remove_product function
    # product_manager.remove_product(shop_id="123456", product_id="PROD123")

    # Call the update_product function
    product_manager.update_product(
        shop_id="123",
        product_id="PROD123",
        updated_values={"ProductName": "New Product Name", "CostPrice": 12.560},
    )

    # product_manager.update_history_stock(
    #    shop_id="1234756",
    #    product_id="PROD123",
    #    updated_value=50,  # Assuming you want to add 50 to the existing history stock
    # )
