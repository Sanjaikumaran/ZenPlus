from tkinter import *
from tkinter import messagebox
from billing import BillBookApp
from cryptography.fernet import Fernet, InvalidToken
import datetime
from offlineDB import Operations
import aiohttp
from database import database

import asyncio
from log_in import Login
from signUp import SignUp
from products_ui import ProductManagementApp
from customers_ui import customerManagementApp
from employee_ui import EmployeeManagementApp
from transactions_ui import transactionManagementApp
from transactionItems_ui import transactionItemsManagementApp


class LoginSignUp:
    def __init__(self, root, callback=None):
        self.root = root
        self.callback = callback  # Assign the callback function
        (
            self.root.success_remote,
            self.root.cnx_remote,
            self.root.cursor_remote,
            self.root.error_remote,
        ) = database.connect_to_remote_db()
        self.login_window = Login(
            self.root, self.on_signup
        )  # Pass the callback function

    def on_signup(self, message):
        if message == "Success":
            # Close the login window

            # Open the main window
            MainWindow(self.root)
        # Close the login window
        else:

            self.signup_window = SignUp(self.root, self.on_login)

    def on_login(self, message):

        # Reopen the login window
        self.login_window = Login(self.root, self.on_signup)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")

        self.create_menu()
        self.main_frame = Frame(self.root)
        self.configure_data = self.decrypt_config()
        self.start_event_loop(self.configure_data)
        self.main_frame.pack(fill=BOTH, expand=True)
        self.bill_book_app = BillBookApp(self.main_frame, self.root)

    def start_event_loop(self, configure_data):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.perform_operations(configure_data))

    async def perform_operations(self, configure_data):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://www.google.com", timeout=5) as response:
                    if response.status == 200:
                        print(configure_data[2])
                        Operations().main(configure_data[2])
                        print()
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass  # Handle connection errors gracefully

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        self.root.config(bg="#382D72")
        self.root.attributes("-zoomed", True)

        # Create File Menu
        file_menu = self.create_sub_menu(
            menubar,
            "File",
            [
                ("New Window", self.new_window),
                ("Sync to Local", self.sync_to_local),
                ("Sync to Remote", self.sync_to_remote),
                ("Exit", self.exit_app),
            ],
        )

        # Create Product Menu
        product_menu = self.create_sub_menu(
            menubar,
            "Product",
            [
                ("Find Product", self.find_product),
                ("Add New Product", self.add_new_product),
                ("Edit Product", self.edit_product),
                ("Delete Product", self.delete_product),
            ],
        )

        # Create Customer Menu
        customer_menu = self.create_sub_menu(
            menubar,
            "Customer",
            [
                ("Find Customer", self.find_customer),
                ("Add Customer", self.add_customer),
                ("Edit Customer", self.edit_customer),
                ("Delete Customer", self.delete_customer),
            ],
        )

        # Create Employee Menu
        employee_menu = self.create_sub_menu(
            menubar,
            "Employee",
            [
                ("Find Employee", self.find_employee),
                ("Add Employee", self.add_employee),
                ("Edit Employee", self.edit_employee),
                ("Delete Employee", self.delete_employee),
            ],
        )

        # Create Transactions Menu
        transaction_menu = self.create_sub_menu(
            menubar,
            "Transactions",
            [
                ("Find Transaction", self.find_transaction),
                ("Add Transaction", self.add_transaction),
                ("Edit Transaction", self.edit_transaction),
                ("Delete Transaction", self.delete_transaction),
            ],
        )

        # Create Transaction Items Menu
        transaction_item_menu = self.create_sub_menu(
            menubar,
            "Transaction Items",
            [
                ("Find Transaction Item", self.find_transaction_item),
                ("Add Transaction Item", self.add_transaction_item),
                ("Edit Transaction Item", self.edit_transaction_item),
                ("Delete Transaction Item", self.delete_transaction_item),
            ],
        )

    def create_sub_menu(self, parent_menu, label, commands):
        sub_menu = Menu(parent_menu, tearoff=0)
        for command_label, command_function in commands:
            sub_menu.add_command(label=command_label, command=command_function)
        parent_menu.add_cascade(label=label, menu=sub_menu)
        return sub_menu

    def decrypt_config(self):
        with open("configure.enc", "rb") as f:
            key = f.readline().strip()
            cipher_suite = Fernet(key)
            encrypted_data = f.read()
            try:
                decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
                return list(eval(decrypted_data))
            except InvalidToken:
                print("Invalid or corrupted encryption key or data.")

    def new_window(self):
        self.bill_book_app = BillBookApp(self.main_frame, self.root)
        # Define the functionality for opening a new window here
        pass

    def sync_to_local(self):
        # Define the functionality for syncing to local here
        self.start_event_loop(self.configure_data)

        pass

    def sync_to_remote(self):
        # Define the functionality for syncing to remote here
        pass

    def exit_app(self):
        # Define the functionality for exiting the application here
        pass

    def find_product(self):
        self.bill_book_app.destroy()
        self.product_app = ProductManagementApp(self.main_frame, self.root)
        self.product_app.search_product()
        # Define the functionality for finding a product here
        pass

    def add_new_product(self):
        self.bill_book_app.destroy()
        self.product_app = ProductManagementApp(self.main_frame, self.root)
        self.product_app.add_new_product()
        # Define the functionality for adding a new product here
        pass

    def edit_product(self):
        self.bill_book_app.destroy()
        self.product_app = ProductManagementApp(self.main_frame, self.root)
        self.product_app.edit_product()
        # Define the functionality for editing a product here
        pass

    def delete_product(self):
        self.bill_book_app.destroy()
        self.product_app = ProductManagementApp(self.main_frame, self.root)
        self.product_app.remove_product()
        # Define the functionality for deleting a product here
        pass

    def find_customer(self):
        self.bill_book_app.destroy()
        self.customer_app = customerManagementApp(self.main_frame, self.root)
        self.customer_app.search_customer()

        # Define the functionality for finding a customer here
        pass

    def add_customer(self):
        self.bill_book_app.destroy()
        self.customer_app = customerManagementApp(self.main_frame, self.root)
        self.customer_app.add_new_customer()
        pass

    def edit_customer(self):
        self.bill_book_app.destroy()
        self.customer_app = customerManagementApp(self.main_frame, self.root)
        self.customer_app.edit_customer()
        # Define the functionality for editing a customer here
        pass

    def delete_customer(self):
        self.bill_book_app.destroy()
        self.customer_app = customerManagementApp(self.main_frame, self.root)
        self.customer_app.remove_customer()
        # Define the functionality for deleting a customer here
        pass

    def find_employee(self):
        self.bill_book_app.destroy()
        self.employee_app = EmployeeManagementApp(self.main_frame, self.root)
        self.employee_app.search_employee()

    def add_employee(self):
        # Define the functionality for adding a new employee here
        self.bill_book_app.destroy()
        self.employee_app = EmployeeManagementApp(self.main_frame, self.root)
        self.employee_app.add_new_employee()
        pass

    def edit_employee(self):
        self.bill_book_app.destroy()
        self.employee_app = EmployeeManagementApp(self.main_frame, self.root)
        self.employee_app.edit_employee()
        # Define the functionality for editing an employee here
        pass

    def delete_employee(self):
        self.bill_book_app.destroy()
        self.employee_app = EmployeeManagementApp(self.main_frame, self.root)
        self.employee_app.remove_employee()

        # Define the functionality for deleting an employee here
        pass

    def find_transaction(self):
        self.bill_book_app.destroy()
        self.transaction_app = transactionManagementApp(self.main_frame, self.root)
        self.transaction_app.search_transaction()

        # Define the functionality for finding a transaction here
        pass

    def add_transaction(self):
        self.bill_book_app.destroy()
        self.transaction_app = transactionManagementApp(self.main_frame, self.root)
        self.transaction_app.add_new_transaction()
        # Define the functionality for adding a new transaction here
        pass

    def edit_transaction(self):
        self.bill_book_app.destroy()
        self.transaction_app = transactionManagementApp(self.main_frame, self.root)
        self.transaction_app.edit_transaction()
        # Define the functionality for editing a transaction here
        pass

    def delete_transaction(self):
        self.bill_book_app.destroy()
        self.transaction_app = transactionManagementApp(self.main_frame, self.root)
        self.transaction_app.remove_transaction()
        # Define the functionality for deleting a transaction here
        pass

    def find_transaction_item(self):
        self.bill_book_app.destroy()
        self.transactionItems_app = transactionItemsManagementApp(
            self.main_frame, self.root
        )
        self.transactionItems_app.search_transaction_items()
        # Define the functionality for finding a transaction item here
        pass

    def add_transaction_item(self):
        self.bill_book_app.destroy()
        self.transactionItems_app = transactionItemsManagementApp(
            self.main_frame, self.root
        )
        self.transactionItems_app.add_new_transaction_items()
        # Define the functionality for adding a new transaction item here
        pass

    def edit_transaction_item(self):
        self.bill_book_app.destroy()
        self.transactionItems_app = transactionItemsManagementApp(
            self.main_frame, self.root
        )
        self.transactionItems_app.edit_transaction_items()
        # Define the functionality for editing a transaction item here
        pass

    def delete_transaction_item(self):
        self.bill_book_app.destroy()
        self.transactionItems_app = transactionItemsManagementApp(
            self.main_frame, self.root
        )
        self.transactionItems_app.remove_transaction_items()
        # Define the functionality for deleting a transaction item here
        pass


if __name__ == "__main__":
    root = Tk()
    app = LoginSignUp(root)
    root.mainloop()
