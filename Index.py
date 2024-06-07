from tkinter import *
from tkinter import messagebox
from billing import BillBookApp
from cryptography.fernet import Fernet, InvalidToken
import datetime
from offlineDB import Operations
import aiohttp
from database import database
import os

import asyncio
from log_in import Login
from signUp import SignUp
from data_manager import DataManager


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
            self.configure_data = self.decrypt_config()
            self.start_event_loop(self.configure_data)

            # Open the main window
            MainWindow(self.root)
        else:
            # Close the login window
            self.signup_window = SignUp(self.root, self.on_login)

    def on_login(self, message):
        # Reopen the login window
        self.login_window = Login(self.root, self.on_signup)

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
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass  # Handle connection errors gracefully

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


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")

        self.create_menu()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)
        self.bill_book_app = BillBookApp(self.main_frame, self.root)

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        self.root.config(bg="#382D72")
        self.root.attributes("-zoomed", True)

        # Create File Menu
        self.create_sub_menu(
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
        self.create_sub_menu(
            menubar,
            "Product",
            [
                ("Find Product", lambda: self.find("Products")),
                ("Add New Product", lambda: self.add("Products")),
                ("Edit Product", lambda: self.edit("Products")),
                ("Delete Product", lambda: self.delete("Products")),
            ],
        )

        # Create Customer Menu
        self.create_sub_menu(
            menubar,
            "Customer",
            [
                ("Find Customer", lambda: self.find("Customers")),
                ("Add Customer", lambda: self.add("Customers")),
                ("Edit Customer", lambda: self.edit("Customers")),
                ("Delete Customer", lambda: self.delete("Customers")),
            ],
        )

        # Create Employee Menu
        self.create_sub_menu(
            menubar,
            "Employee",
            [
                ("Find Employee", lambda: self.find("Employees")),
                ("Add Employee", lambda: self.add("Employees")),
                ("Edit Employee", lambda: self.edit("Employees")),
                ("Delete Employee", lambda: self.delete("Employees")),
            ],
        )

        # Create Transactions Menu
        self.create_sub_menu(
            menubar,
            "Transactions",
            [
                ("Find Transaction", lambda: self.find("Transactions")),
                ("Add Transaction", lambda: self.add("Transactions")),
                ("Edit Transaction", lambda: self.edit("Transactions")),
                ("Delete Transaction", lambda: self.delete("Transactions")),
            ],
        )

        # Create Transaction Items Menu
        self.create_sub_menu(
            menubar,
            "Transaction Items",
            [
                ("Find Transaction Item", lambda: self.find("TransactionItems")),
                ("Add Transaction Item", lambda: self.add("TransactionItems")),
                ("Edit Transaction Item", lambda: self.edit("TransactionItems")),
                ("Delete Transaction Item", lambda: self.delete("TransactionItems")),
            ],
        )

    def create_sub_menu(self, parent_menu, label, commands):
        sub_menu = Menu(parent_menu, tearoff=0)
        for command_label, command_function in commands:
            sub_menu.add_command(label=command_label, command=command_function)
        parent_menu.add_cascade(label=label, menu=sub_menu)

    def new_window(self):
        self.bill_book_app.destroy()
        self.bill_book_app = BillBookApp(self.main_frame, self.root)

    def sync_to_local(self):
        self.start_event_loop(self.configure_data)

    def sync_to_remote(self):
        pass

    def exit_app(self):
        self.root.quit()

    def find(self, page):
        self.bill_book_app.destroy()
        self.bill_book_app = DataManager(self.main_frame, self.root, page)
        self.bill_book_app.search_items()

    def add(self, page):
        self.bill_book_app.destroy()
        self.bill_book_app = DataManager(self.main_frame, self.root, page)
        self.bill_book_app.add_new()

    def edit(self, page):
        self.bill_book_app.destroy()
        self.bill_book_app = DataManager(self.main_frame, self.root, page)
        self.bill_book_app.edit()

    def delete(self, page):
        self.bill_book_app.destroy()
        self.bill_book_app = DataManager(self.main_frame, self.root, page)
        self.bill_book_app.remove()


if __name__ == "__main__":
    root = Tk()
    if os.path.isfile("local_database.db"):

        MainWindow(root)
    else:

        app = LoginSignUp(root)
    root.mainloop()
