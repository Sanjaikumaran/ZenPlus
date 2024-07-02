from tkinter import *
from tkinter import messagebox
from billing import BillBookApp
from cryptography.fernet import Fernet, InvalidToken
import datetime
from offlineDB import Operations
import aiohttp
from database import database
import os
import main
import tkinter as tk
import asyncio
from log_in import Login
from signUp import SignUp
from data_manager import DataManager


class LoginSignUp:
    def __init__(self, root, callback=None):
        if root:
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
            MainWindow(self.root, self.configure_data[2])
        else:
            # Close the login window
            self.signup_window = SignUp(self.root, self.on_login)

    def on_login(self, message):
        # Reopen the login window
        self.login_window = Login(self.root, self.on_signup)

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


class MainWindow:
    def __init__(self, root, shop_id):
        self.root = root
        self.shop_id = shop_id
        self.root.title("Main Window")

        self.create_menu()
        self.main_frame = Frame(self.root)
        # self.main_frame.pack(fill=BOTH, expand=True)
        # self.main_frame.grid(row=0, column=0)
        # self.main_frame.place(x=0, y=0)
        self.bill_book_app = BillBookApp(self.main_frame, self.root, self.shop_id)

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        self.root.config(bg="#382D72")
        self.root.attributes("-zoomed", True)

        # Define the menu configurations
        menu_configs = [
            "File",
            "Product",
            "Customer",
            "Employee",
            "Transactions",
            "Transaction Items",
        ]

        # Define the common items for all menus except "File"
        common_items = [
            ("Find {item}", lambda item: lambda: self.action(item, "search_items")),
            ("Add New {item}", lambda item: lambda: self.action(item, "add_new")),
            ("Edit {item}", lambda item: lambda: self.action(item, "edit")),
            ("Delete {item}", lambda item: lambda: self.action(item, "remove")),
        ]

        # Define the items specifically for the "File" menu
        file_items = [
            ("New Window", self.new_window),
            ("Find Bill", self.find_bill),
            ("Hold Bills", self.hold_bills),
            ("Sync to Local", self.sync_to_local),
            ("Sync to Remote", self.sync_to_remote),
            ("Exit", self.exit_app),
        ]

        # Loop through the menu configurations to create submenus
        for menu in menu_configs:
            if menu == "File":
                items = file_items
            else:
                entity = menu.replace(" ", "")  # Remove spaces for the function calls
                items = [
                    (name.format(item=entity), action(entity))
                    for name, action in common_items
                ]

            self.create_sub_menu(menubar, menu, items)

    def create_sub_menu(self, parent_menu, label, commands):
        sub_menu = Menu(parent_menu, tearoff=0)
        for command_label, command_function in commands:
            sub_menu.add_command(label=command_label, command=command_function)
        parent_menu.add_cascade(label=label, menu=sub_menu)

    def new_window(self):
        try:
            self.data_manager_app.destroy()
            self.bill_book_app.destroy()
            self.hold_frame.destroy()
        except:
            pass
        finally:
            self.bill_book_app = BillBookApp(self.main_frame, self.root, self.shop_id)

    def find_bill(self):
        pass

    def hold_bills(self):
        try:
            print(self.bill_book_app.exist())
            # self.hold_book_app.destroy()
            self.data_manager_app.destroy()
        except:
            pass

        def close_window():

            self.hold_frame.destroy()

        # Create hold_frame and place it
        self.hold_frame = Frame(self.root)
        self.hold_frame.place(x=0, y=0)

        # Create close button and pack it in hold_frame
        self.close_button = Button(self.hold_frame, text="Close", command=close_window)
        self.close_button.pack()

        # Initialize BillBookApp within hold_frame
        self.hold_book_app = BillBookApp(
            self.hold_frame, self.root, self.shop_id, "Hold Window"
        )

    def sync_to_local(self):
        self.start_event_loop(self.configure_data)

    def sync_to_remote(self):
        pass

    def exit_app(self):
        self.root.quit()

    def action(self, page, action):
        try:
            self.bill_book_app.destroy()
            self.hold_frame.destroy()
            self.data_manager_app.destroy()
        except:
            pass
        finally:
            self.data_manager_app = DataManager(
                self.main_frame, self.root, page, self.shop_id
            )
            getattr(self.data_manager_app, action)()


if __name__ == "__main__":
    root = Tk()
    if os.path.isfile("local_database.db"):
        configure_data = LoginSignUp("").decrypt_config()

        MainWindow(root, configure_data[2])
    else:

        app = LoginSignUp(root)
    root.mainloop()
