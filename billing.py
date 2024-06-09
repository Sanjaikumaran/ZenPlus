from tkinter import *
import sqlite3

import random
from tkinter import ttk, messagebox, font as tkFont
from operations_access import DataManagement


import time


class DataListFrame(Frame):
    def __init__(
        self, master, product_var, quantity_var, price_var, discount_var, product_id_var
    ):
        super().__init__(master)
        self.product_var = product_var
        self.price_var = price_var

        self.discount_var = discount_var
        self.quantity_var = quantity_var
        self.product_id_var = product_id_var  # Assign product_id_var
        self.listbox_created = False

    def createBox(self):
        # Set the maximum height of the listbox
        max_listbox_height = 10  # Adjust this value as needed

        self.data_list = Listbox(self, width=50)
        self.data_list.pack(side=LEFT)  # Fill both X and Y directions
        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.data_list.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Configure listbox to use the scrollbar
        self.data_list.config(yscrollcommand=self.scrollbar.set)

        # Bind events
        self.data_list.bind("<ButtonRelease-1>", self.on_select)
        self.data_list.bind("<Return>", self.on_select)

        self.listbox_created = True

        # Update the height after items are added
        self.updateListboxHeight(max_listbox_height)

    def updateListboxHeight(self, max_height):
        # Set the maximum height for the listbox
        num_items = self.data_list.size()
        self.data_list.configure(height=min(num_items, max_height))

    def update_data(self, data):
        if self.listbox_created:
            self.data_list.delete(0, END)
            for item in data:

                formatted_item = (
                    f"{item[5]}, {item[4]}, {item[3]}, ₹ {item[8]}, {item[9]}"
                )
                self.data_list.insert(END, formatted_item)
            self.data_list.config(height=10)

    def on_select(self, event):
        selected_index = self.data_list.curselection()

        if selected_index:
            selected_item_str = self.data_list.get(selected_index)
            selected_item_list = selected_item_str.split(", ")

            self.product_id_var = selected_item_list[0]
            self.product_var.set(selected_item_list[1])
            self.price_var.set(selected_item_list[3])
            self.discount_var.set(str.strip(selected_item_list[4]) + " %")
            self.quantity_var.set(1)
            self.destroy()


class BillBookApp:
    columns = [
        "SNo",
        "Customer ID",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Address",
        "City",
        "Country",
    ]

    def __init__(self, master, window, shop_id):
        self.shop_id = shop_id
        self.master = master
        self.master.place(x=0, y=0)
        self.window = window
        self.manager = DataManagement()
        self.window.title("Bill Book")
        self.master.config(bg="#382D72")
        # self.master.attributes("-zoomed", True)
        self.data_frame = None

        self.name = StringVar()
        self.ph_no = StringVar()
        self.bill_no = StringVar()
        self.emp_name = StringVar()
        self.S_no = StringVar()
        self.Product = StringVar()
        self.Quantity = StringVar()
        self.Discount = StringVar()
        self.Amount = StringVar()
        self.Price = StringVar()
        self.product_id_var = None

        self.cart_items = []

        # self.create_menu()
        self.create_customer_frame()
        self.create_item_bill_section()
        self.window.bind("<Control-p>", lambda event: self.add_new_customer())
        self.window.bind("<Escape>", lambda event: self.clear_cart())
        # self.window.bind("<Return>", lambda event: self.add_to_cart())
        self.window.bind("<Return>", self.on_enter_pressed)
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

    def create_customer_frame(self):
        customer_frame = Frame(self.master, bg="#A080E1")
        customer_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        # Configure column weights to center the content
        for i in range(6):
            customer_frame.columnconfigure(i, weight=1)

        title = Label(
            customer_frame,
            text="  Zen Plus",
            font=("calibri", 50, "bold"),
            bg="#A080E1",
            fg="white",
        )
        title.grid(row=0, column=1, pady=20, sticky="N")

        # Your existing customer details entry fields
        name_frame = Frame(customer_frame, bg="#A080E1")
        name_frame.grid(row=1, column=0, pady=10)

        name_label = Label(
            name_frame, text="Name", font=("calibri", 15), bg="#A080E1", fg="white"
        )
        name_label.pack(side=LEFT, padx=5)

        name_entry = Entry(name_frame, font=("calibri", 15), width=25)
        name_entry.pack(side=LEFT, padx=5)

        bill_no_frame = Frame(customer_frame, bg="#A080E1")
        bill_no_frame.grid(row=1, column=1, pady=10, sticky="en")

        Label(
            bill_no_frame,
            text="Bill No.",
            font=("calibri", 15),
            bg="#A080E1",
            fg="white",
        ).pack(side=LEFT, padx=5)
        self.bill_entry = Entry(
            bill_no_frame, font=("calibri", 15), width=25, textvariable=self.bill_no
        )
        self.bill_entry.pack(side=RIGHT, padx=5)

        # Bind the <FocusIn> event to the entry widget
        # self.bill_entry.bind("<FocusIn>", self.on_focus)

        transaction_id = self.manager.get_last_item("Transactions", "TransactionID")
        self.transaction_id = "TRN" + str(int(transaction_id[0][3:]) + 1)
        self.bill_no.set(self.transaction_id)

        # Add a label for the clock
        self.clock_label = Label(
            customer_frame, text="", font=("calibri", 15), bg="#A080E1", fg="white"
        )
        self.clock_label.grid(row=1, column=3, padx=20)

        # Update the clock periodically
        self.update_clock()

    def update_clock(self):
        current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_datetime)
        # Update every second (1000 milliseconds)
        self.master.after(1000, self.update_clock)

    def clear_cart(self):
        # Clear the cart items list
        # self.cart_items.clear()
        for widget in self.cart_inner_frame.winfo_children():
            widget.destroy()

        # Update the total price, taxes, and amount
        total_price = 0
        total_taxes = 0
        total_amount = 0

        # Update labels with calculated values
        for child in self.master.winfo_children():
            if child.winfo_name() == "carthead":
                for label in child.winfo_children():
                    if label.cget("text").startswith("Total Price"):
                        label.config(text="Total Price : ₹ {:.2f}".format(total_price))
                    elif label.cget("text").startswith("Total Taxes"):
                        label.config(text="Total Taxes : ₹ {:.2f}".format(total_taxes))
                    elif label.cget("text").startswith("Total Amount"):
                        label.config(
                            text="Total Amount : ₹ {:.2f}".format(total_amount)
                        )

        # Update the cart section in the GUI
        # self.create_cart_section()

    def remove_from_cart(self, index):
        # Remove the item from the cart_items list
        del self.cart_items[index]

        # Recalculate the serial numbers
        for i, item in enumerate(self.cart_items):
            self.cart_items[i] = (i + 1,) + item[1:]  # Update serial number

        # Recalculate the totals
        self.total_price = sum(float(item[6][1:]) for item in self.cart_items)
        self.total_taxes = sum(float(item[7][1:]) for item in self.cart_items)
        self.total_amount = sum(float(item[8][1:]) for item in self.cart_items)

        # Update labels with recalculated values
        for child in self.master.winfo_children():
            if child.winfo_name() == "carthead":
                for label in child.winfo_children():
                    if label.cget("text").startswith("Total Price"):
                        label.config(
                            text="Total Price : ₹ {:.2f}".format(self.total_price)
                        )
                    elif label.cget("text").startswith("Total Taxes"):
                        label.config(
                            text="Total Taxes : ₹ {:.2f}".format(self.total_taxes)
                        )
                    elif label.cget("text").startswith("Total Amount"):
                        label.config(
                            text="Total Amount : ₹ {:.2f}".format(self.total_amount)
                        )

        # Clear the cart display frame
        for widget in self.cart_inner_frame.winfo_children():
            widget.destroy()

        # Redisplay the items
        column_widths = [5, 15, 30, 12, 12, 12, 13, 13, 13, 10]
        for i, item in enumerate(self.cart_items, start=2):
            for j, value in enumerate(item):
                label = Label(
                    self.cart_inner_frame,
                    text=value,
                    font=("calibri", 15),
                    width=column_widths[j],
                )
                label.grid(row=i, column=j, padx=5, pady=5)

            remove_button = Button(
                self.cart_inner_frame,
                text="Remove",
                font=("calibri", 12),
                bg="#FF5733",
                fg="white",
                command=lambda idx=i - 2: self.remove_from_cart(idx),
            )
            remove_button.grid(
                row=i, column=len(column_widths), padx=10
            )  # Place the button in the last column

    def cart_head(self, total_price, total_taxes, total_amount):

        cart_head = Frame(self.master, bg="#5C509C", name="carthead")
        cart_head.pack(fill=X, padx=10, pady=10)

        cart_title = Label(
            cart_head,
            text="🛒 Cart",
            font=("calibri", 30, "bold"),
            bg="#5C509C",
            fg="white",
        )
        cart_title.grid(row=0, column=0, columnspan=2, padx=(10, 500), pady=10)

        # Placeholders for total price, taxes, and amount
        total_price_label = Label(
            cart_head,
            text="Total Price : ₹ 0.00",
            font=("calibri", 20, "bold"),
            bg="#5C509C",
            fg="white",
        )
        total_price_label.grid(row=0, column=5, columnspan=3, padx=10, pady=10)
        total_taxes_label = Label(
            cart_head,
            text="Total Taxes : ₹ 0.00",
            font=("calibri", 20, "bold"),
            bg="#5C509C",
            fg="white",
        )
        total_taxes_label.grid(row=0, column=9, columnspan=3, padx=10, pady=10)
        total_amount_label = Label(
            cart_head,
            text="Total Amount : ₹ 0.00",
            font=("calibri", 20, "bold"),
            bg="#5C509C",
            fg="white",
        )
        total_amount_label.grid(row=0, column=12, columnspan=3, padx=10, pady=10)
        # Create a frame for column titles

    def create_cart_section(self):
        column_titles_frame = Frame(
            self.master,
            bg="#5C509C",
            name="columntitles",
        )

        column_titles_frame.pack(fill=X, padx=10)

        # Column titles
        column_titles = [
            "SNo",
            "Product ID",
            "Product Name",
            "Quantity",
            "Price",
            "Discount",
            "Amount",
            "Taxes",
            "Total",
            "Remove",
        ]
        # Define the widths of each column
        column_widths = [5, 14, 22, 12, 10, 12, 12, 12, 12, 10]

        # Add column titles
        for i, title in enumerate(column_titles):
            # Create a frame for each column title label
            frame = Frame(
                column_titles_frame, width=column_widths[i], height=30, bg="white"
            )
            frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

            # Create the label inside the frame
            label = Label(
                frame,
                text=title,
                font=("calibri", 15, "bold"),
                bg="#5C509C",
                fg="white",
                width=column_widths[i],
            )
            label.pack(expand=True, fill=BOTH)

            # Add vertical line to separate cells with different colors
            if i < len(column_titles) - 1:
                separator = Frame(column_titles_frame, width=4, bg="#382D72")
                separator.grid(row=0, column=i, rowspan=1, sticky="nse", padx=5)

        # Resize the weights of the columns to make them expandable
        for i in range(len(column_titles)):
            column_titles_frame.grid_columnconfigure(i, weight=1)
        self.inner_cart()

    def inner_cart(self):
        self.cart_frame = Frame(self.master, bg="#5C509C", name="cartframe")
        self.cart_frame.pack(side="bottom", fill=BOTH, expand=True, padx=10, pady=10)

        # Create a canvas for the scrollable area
        self.cart_canvas = Canvas(self.cart_frame, bg="#5C509C")
        self.cart_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Add scrollbar for the canvas
        cart_scrollbar = Scrollbar(
            self.cart_frame, orient=VERTICAL, command=self.cart_canvas.yview
        )
        cart_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure canvas to use the scrollbar
        self.cart_canvas.config(yscrollcommand=cart_scrollbar.set)

        # Create a frame to contain the item rows
        self.cart_inner_frame = Frame(self.cart_canvas, bg="#5C509C")
        self.cart_canvas.create_window(
            (0, 0), window=self.cart_inner_frame, anchor="nw"
        )

        # Bind scrolling to the canvas
        def on_canvas_configure(event):
            self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))

        self.cart_inner_frame.bind("<Configure>", on_canvas_configure)

        # Bind mousewheel scrolling (optional)
        def scroll(event):
            self.cart_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.cart_canvas.bind_all("<MouseWheel>", scroll)

        self.cart_frame.configure(height=565)
        self.cart_canvas.configure(height=565)

    def add_to_cart(self, item=False):
        if item:

            self.product_id_var = item[3]
            product_name = "i"
            quantity = item[4]
            price = item[5]
            discount = item[6]
            amount = item[7]
            tax = item[8]
            total = item[9]
        else:
            product_name = self.Product.get()
            quantity = int(self.Quantity.get())
            price = float(self.Price.get()[1:])
            original_discount = float(self.Discount.get()[:-1])
            discount = (price * original_discount / 100) * quantity
            amount = float(quantity) * price
            self.product_id_var = self.data_frame.product_id_var

            gst = 0.18
            tax = amount * gst
            amount = float(amount - discount)
            self.Product.set("")
            self.Quantity.set("")
            self.Price.set("")
            self.Discount.set("")
            total = amount + tax

        # Append the new item to cart_items
        self.cart_items.append(
            (
                len(self.cart_items) + 1,  # Serial number
                self.product_id_var,
                product_name,
                str(quantity),
                f"₹{price:.2f}",
                f"₹{discount:.2f}",
                f"₹{amount:.2f}",
                f"₹{tax:.2f}",
                f"₹{total:.2f}",
            )
        )

        # Update total price, taxes, and amount after adding the item
        self.total_price = sum(float(item[6][1:]) for item in self.cart_items)
        self.total_taxes = sum(float(item[7][1:]) for item in self.cart_items)
        self.total_amount = sum(float(item[8][1:]) for item in self.cart_items)

        # Update labels with calculated values
        for child in self.master.winfo_children():
            if child.winfo_name() == "carthead":
                for label in child.winfo_children():
                    if label.cget("text").startswith("Total Price"):
                        label.config(
                            text="Total Price : ₹ {:.2f}".format(self.total_price)
                        )
                    elif label.cget("text").startswith("Total Taxes"):
                        label.config(
                            text="Total Taxes : ₹ {:.2f}".format(self.total_taxes)
                        )
                    elif label.cget("text").startswith("Total Amount"):
                        label.config(
                            text="Total Amount : ₹ {:.2f}".format(self.total_amount)
                        )

        column_widths = [5, 15, 24, 12, 12, 12, 13, 13, 13, 10]

        # Clear the cart display frame
        for widget in self.cart_inner_frame.winfo_children():
            widget.destroy()

        for i, item in enumerate(self.cart_items, start=2):
            for j, value in enumerate(item):
                label = Label(
                    self.cart_inner_frame,
                    text=value,
                    font=("calibri", 15),
                    width=column_widths[j],
                )
                label.grid(row=i, column=j, padx=5, pady=5)

            remove_button = Button(
                self.cart_inner_frame,
                text="Remove",
                font=("calibri", 12),
                bg="#FF5733",
                fg="white",
                width=column_widths[-1],
                command=lambda idx=i - 2: self.remove_from_cart(idx),
            )
            remove_button.grid(
                row=i, column=len(column_widths), padx=9
            )  # Place the button in the last column

    def on_enter_pressed(self, event):
        if self.window.focus_get() == self.bill_entry:
            # If bill_entry is focused
            transaction_items = self.manager.get_item(
                "TransactionItems", "*", {"TransactionID": self.bill_no.get()}
            )
            if transaction_items:
                self.cart_items.clear()
                for item in transaction_items:
                    self.add_to_cart(item)
        else:
            # If bill_entry is not focused
            self.add_to_cart()

    def create_item_bill_section(self):
        bill_frame = Frame(self.master, bg="#5C509C")
        bill_frame.pack(fill=X, padx=10, pady=10)

        Label(
            bill_frame,
            text="Product (Name,Price,ID,Brand)",
            font=("calibri", 15),
            bg="#E5CCF4",
            fg="black",
            width=30,
        ).grid(row=1, column=2, columnspan=2)
        self.product_name_entry = Entry(
            bill_frame, textvariable=self.Product, font=("calibri", 15), width=30
        )
        self.product_name_entry.grid(row=2, column=2, columnspan=2)
        self.product_name_entry.bind("<KeyRelease>", self.check_matching_data)

        Label(
            bill_frame,
            text="Quantity",
            font=("calibri", 15),
            bg="#E5CCF4",
            fg="black",
            width=18,
        ).grid(row=1, column=4)
        Entry(
            bill_frame, textvariable=self.Quantity, font=("calibri", 15), width=18
        ).grid(row=2, column=4)

        Label(
            bill_frame,
            text="Discount",
            font=("calibri", 15),
            bg="#E5CCF4",
            fg="black",
            width=18,
        ).grid(row=1, column=5)
        Entry(
            bill_frame, textvariable=self.Discount, font=("calibri", 15), width=18
        ).grid(row=2, column=5)

        Label(
            bill_frame,
            text="Price",
            font=("calibri", 15),
            bg="#E5CCF4",
            fg="black",
            width=15,
        ).grid(row=1, column=6)
        Entry(bill_frame, textvariable=self.Price, font=("calibri", 15), width=15).grid(
            row=2, column=6
        )

        add_item_button = Button(
            bill_frame,
            text="Add Item",
            font=("calibri", 15),
            bg="#FF5733",
            fg="white",
            command=self.add_to_cart,
            padx=20,
        )
        add_item_button.grid(
            row=1, column=7, padx=30, rowspan=2
        )  # Spanning two rows and three columns, move to the right
        clear_button = Button(
            bill_frame,
            text="Clear Cart",
            font=("calibri", 15),
            bg="#FF5733",
            fg="white",
            command=self.clear_cart,
            padx=20,
        )
        clear_button.grid(row=1, column=8, padx=30, rowspan=2)
        hold_button = Button(
            bill_frame,
            text="Hold",
            font=("calibri", 15),
            bg="#FF5733",
            fg="white",
            command=self.hold_bill,
            padx=20,
        )
        hold_button.grid(row=1, column=9, padx=30, rowspan=2)

        print_button = Button(
            bill_frame,
            text="Print",
            font=("calibri", 15),
            bg="#FF5733",
            fg="white",
            command=self.add_new_customer,
            padx=20,
        )
        print_button.grid(
            row=1,
            column=10,
            rowspan=2,
            padx=30,
        )

        self.cart_head("", "", "")
        self.create_cart_section()

    def hold_bill(self):

        self.transaction_id = "H-" + self.transaction_id

        self.return_value = True
        self.print_transaction()

    def add_new_customer(self, event=None):
        self.add_window = Toplevel(self.master)
        self.add_window.title("Customer Details")
        self.add_window.bind("<Control-s>", lambda event: self.save_new_customer())
        self.add_window.bind("<Return>", lambda event: self.save_new_customer())

        # Exclude trsave_new_customer ID and Shop ID from the labels
        self.labels = self.columns[2:]
        self.entries = []

        for i, label in enumerate(self.labels):
            Label(self.add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(self.add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)
        options = ["Cash", "Card", "UPI"]
        Label(self.add_window, text="Payment Method").grid(
            row=i + 1, column=0, padx=10, pady=5
        )
        # Create a variable to store the selected option
        self.selected_option = StringVar(self.add_window)
        self.selected_option.set(options[0])  # Set the default selected option

        # Create the dropdown menu
        self.dropdown = OptionMenu(self.add_window, self.selected_option, *options)
        self.dropdown.grid(row=i + 1, column=1, padx=10, pady=5)

        save_button = Button(
            self.add_window, text="Save", command=self.save_new_customer
        )
        save_button.grid(row=len(self.labels) + 1, columnspan=2, padx=10, pady=10)

    def save_new_customer(self):
        # Get data from entry widgets and construct a dictionary
        self.customer_data = {}
        for label, entry in zip(self.labels, self.entries):
            # Remove spaces from column names
            column_name = label.replace(" ", "")
            self.customer_data[column_name] = entry.get()
        self.customer_data["CustomerID"] = self.entries[3].get()
        self.customer_data["ShopID"] = self.shop_id
        self.customer_data["Timestamp"] = self.current_time
        # Generate a random customer ID not in the table

        # self.original_data = self.customer_manager.list_customers()

        # Assuming customer_manager has a method for adding new customers
        if self.manager.add_item("Customers", self.customer_data):

            # self.original_data = self.manager.list_c()

            self.add_window.destroy()
            self.return_value = True
            self.print_transaction()

        else:
            self.return_value = False

            messagebox.showerror("Error", "customer cannot be added.")
            self.add_window.destroy()

    def print_transaction(self):

        if self.return_value:

            # Generate a unique transaction ID

            # Get customer ID, payment method, and employee ID from the GUI variables
            if self.transaction_id[0] == "H":
                customer_id = "In Hold"
                payment_method = "In Hold"
            else:
                customer_id = self.customer_data[
                    "Phone"
                ]  # self.ph_no.get()  # Assuming this is the customer ID
                payment_method = self.selected_option.get()
            employee_id = (
                "sk0311"  # self.emp_name.get()  # Assuming this is the employee ID
            )
            profit = 21212121
            locationid = 890

            # Initialize variables for total quantity and total discount
            total_quantity = 0
            total_discount = 0

            # Prepare a list to hold transaction item data
            transaction_item_list = []

            # Iterate over each item in the cart and prepare transaction item data
            for cart_item in self.cart_items:
                (
                    product_id,
                    product_name,
                    quantity,
                    price,
                    discount,
                    amount,
                    tax,
                    total,
                ) = cart_item

                # Increment total quantity and total discount
                total_quantity += int(quantity)
                total_discount += float(discount[1:])

                # Prepare transaction item data
                transaction_item_data = {
                    "TransactionID": str(self.transaction_id),
                    "ShopId": self.shop_id,  # Assuming ShopID is hardcoded
                    "ProductID": product_id,  # Assuming ProductID is hardcoded or retrieved from the database
                    "Quantity": int(quantity),
                    "Price": float(price[1:]),
                    "Discount": float(discount[1:]),
                    "Amount": float(amount[1:]),
                    "Taxes": float(tax[1:]),
                    "Total": float(total[1:]),
                    # Include other transaction item details as needed
                }

                # Add transaction item data to the list
                transaction_item_list.append(transaction_item_data)
            items_added = 0
            # Assuming there's a method to insert transaction items into the database
            for transaction_item_data in transaction_item_list:
                if self.manager.add_item("TransactionItems", transaction_item_data):
                    items_added += 1
                    continue  # Successfully added transaction item
                else:
                    messagebox.showerror("Error", "Transaction item cannot be added.")
                    return

            # Prepare transaction data

            if items_added == len(transaction_item_list):
                transaction_data = {
                    "Timestamp": self.current_time,
                    "TransactionID": str(self.transaction_id),
                    "ShopId": self.shop_id,  # Assuming ShopID is hardcoded
                    "CustomerID": customer_id,
                    "Quantity": total_quantity,
                    "Discount": total_discount,
                    "TotalPrice": self.total_price,
                    "Tax": self.total_taxes,
                    "Profit": profit,
                    "NetSales": self.total_amount,
                    "PaymentMethod": payment_method,
                    "EmployeeID": employee_id,
                    "LocationID": locationid,
                    # Include other transaction details as needed
                }
                # Assuming sales_manager has a method for adding new transactions
                if self.manager.add_item("Transactions", transaction_data):
                    # Update GUI or perform other actions upon successful addition
                    messagebox.showinfo("Success", "Printed")
                    self.clear_cart()
                    self.transaction_id = "TRN" + str(int(self.transaction_id[3:]) + 1)
                    self.bill_no.set(self.transaction_id)
            else:
                # Handle failure to add transaction
                messagebox.showerror("Error", "Cannot Print")

        else:
            # Handle failure to add transaction items
            messagebox.showerror("Error", "Transaction items cannot be added.")

    def check_matching_data(self, event):

        input_text = self.product_name_entry.get()
        if input_text:
            connection = sqlite3.connect("local_database.db")
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Products WHERE ProductId LIKE ? OR ProductName LIKE ? OR Brand LIKE ? OR SellingPrice LIKE ?",
                (
                    "%" + input_text + "%",
                    "%" + input_text + "%",
                    "%" + input_text + "%",
                    "%" + input_text + "%",
                ),
            )
            matching_data = cursor.fetchall()
            if self.data_frame is None or not self.data_frame.winfo_exists():
                # Create a new DataListFrame
                self.data_frame = DataListFrame(
                    self.master,
                    self.Product,
                    self.Quantity,
                    self.Price,
                    self.Discount,
                    self.product_id_var,
                )
                self.data_frame.pack(pady=10)

                # Position the tooltip frame below the entry
                x, y, _, _ = self.product_name_entry.bbox("insert")

                self.data_frame.place(x=10, y=280)

            if not self.data_frame.listbox_created:
                self.data_frame.createBox()
            self.data_frame.update_data(matching_data)
        else:
            if self.data_frame is not None and self.data_frame.winfo_exists():
                self.data_frame.destroy()

    def item_selected(self):
        pass

    def destroy(self):
        # Destroy all children of the master widget
        for child in self.master.winfo_children():
            child.destroy()


if __name__ == "__main__":
    root = Tk()
    app = BillBookApp(root)
    root.mainloop()
