from tkinter import *
import sqlite3
from products_ui import ProductManagementApp
import random
from tkinter import ttk, messagebox, font as tkFont
from transactions import sales_stats_management


class DataListFrame(Frame):
    def __init__(self, master, product_var, quantity_var, price_var, discount_var):
        super().__init__(master)
        self.product_var = product_var
        self.price_var = price_var
        self.discount_var = discount_var
        self.quantity_var = quantity_var
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
                formatted_item = f"{item[3]}, {item[2]}, ₹ {item[6]}, {item[5]}"
                self.data_list.insert(END, formatted_item)
            self.data_list.config(height=10)

    def on_select(self, event):
        selected_index = self.data_list.curselection()

        if selected_index:
            selected_item_str = self.data_list.get(selected_index)
            selected_item_list = selected_item_str.split(", ")
            self.product_var.set(selected_item_list[0])
            self.price_var.set(selected_item_list[2])
            self.discount_var.set(str.strip(selected_item_list[3]) + " %")
            self.quantity_var.set(1)
            self.destroy()


class BillBookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bill Book")
        self.master.config(bg="#382D72")
        self.master.attributes("-zoomed", True)
        self.data_frame = None
        self.sales_manager = sales_stats_management()

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

        self.cart_items = []

        self.create_menu()
        self.create_customer_frame()
        self.create_item_bill_section()

    def create_menu(self):
        menu_items = [
            (
                "File",
                [
                    ("New", None),
                    ("Sync to Remote Database", None),
                    ("Sync to Local Database", None),
                    ("Open", None),
                    ("Exit", self.master.quit),
                ],
            ),
            (
                "Products",
                [
                    ("Show Product List", self.show_product_list),
                    ("Find Product", self.open_product_management_ui),
                    ("Add Product", self.add_product),
                    ("Edit Product", self.edit_product),
                    ("Remove Product", self.remove_product),
                ],
            ),
            (
                "Employee",
                [
                    ("Show Employee List", self.show_employee_list),
                    ("Find Employee", self.find_employee),
                    ("Add Employee", self.add_employee),
                    ("Edit Employee", self.edit_employee),
                    ("Remove Employee", self.remove_employee),
                ],
            ),
            (
                "Report",
                [
                    ("Daily Sales", self.daily_sales),
                    ("Gross Sales", self.gross_sales),
                    ("Shop-Wise", self.shop_wise),
                    ("Summary", self.summary),
                ],
            ),
        ]

        menu = Menu(self.master)
        self.master.config(menu=menu)

        for label, items in menu_items:
            submenu = Menu(menu)
            menu.add_cascade(label=label, menu=submenu)
            for item_label, command in items:
                submenu.add_command(label=item_label, command=command)

    def open_product_management_ui(self):
        # Create a Toplevel window for the product management UI
        self.product_management_window = Toplevel(self.master)
        # Instantiate the ProductManagementApp class in the Toplevel window
        self.product_management_app = ProductManagementApp(
            self.product_management_window
        )
        # Bind a callback to handle closing of the product management UI
        self.product_management_window.protocol(
            "WM_DELETE_WINDOW", self.close_product_management_ui
        )

    def close_product_management_ui(self):
        # Destroy the product management UI Toplevel window
        self.product_management_window.destroy()

    def show_product_list(self):
        print("Show Product List")

    def find_product(self):
        print("Find Product")

    def add_product(self):
        print("Add Product")

    def edit_product(self):
        print("Edit Product")

    def remove_product(self):
        print("Remove Product")

    def show_employee_list(self):
        print("Show Employee List")

    def find_employee(self):
        print("Find Employee")

    def add_employee(self):
        print("Add Employee")

    def edit_employee(self):
        print("Edit Employee")

    def remove_employee(self):
        print("Remove Employee")

    def daily_sales(self):
        print("Daily Sales")

    def gross_sales(self):
        print("Gross Sales")

    def shop_wise(self):
        print("Shop-Wise")

    def summary(self):
        print("Summary")

    def create_customer_frame(self):
        customer_frame = Frame(self.master, bg="#A080E1")
        customer_frame.pack(side=TOP, fill=X, padx=10, pady=10)
        title = Label(
            customer_frame,
            text="Sales Bill",
            font=("calibri", 20, "bold"),
            bg="#A080E1",
            fg="white",
        )
        title.grid(row=0, columnspan=2, padx=10, pady=10)

        Label(
            customer_frame, text="Name", font=("calibri", 15), bg="#A080E1", fg="white"
        ).grid(row=1, column=1)
        Entry(
            customer_frame, textvariable=self.name, font=("calibri", 15), width=25
        ).grid(row=1, column=2, pady=20, padx=10)

        Label(
            customer_frame,
            text="Employee",
            font=("calibri", 15),
            bg="#A080E1",
            fg="white",
        ).grid(row=1, column=5)
        Entry(
            customer_frame, textvariable=self.emp_name, font=("calibri", 15), width=25
        ).grid(row=1, column=6, padx=10)

        Label(
            customer_frame,
            text="Mobile Number",
            font=("calibri", 15),
            bg="#A080E1",
            fg="white",
        ).grid(row=1, column=3)
        Entry(
            customer_frame, textvariable=self.ph_no, font=("calibri", 15), width=25
        ).grid(row=1, column=4, padx=10)

        Label(
            customer_frame,
            text="Bill No.",
            font=("calibri", 15),
            bg="#A080E1",
            fg="white",
        ).grid(row=1, column=7)
        Entry(
            customer_frame, textvariable=self.bill_no, font=("calibri", 15), width=25
        ).grid(row=1, column=8, padx=10)

    def clear_cart(self):
        # Clear the cart items list
        self.cart_items.clear()

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
        self.create_cart_section()

    def remove_from_cart(self, index):
        # Remove item from cart_items list
        removed_item = self.cart_items[index]
        del self.cart_items[index]

        # Update the serial numbers for remaining items
        updated_cart_items = []
        for i, item in enumerate(self.cart_items, start=1):
            updated_item = list(item)  # Convert tuple to list to allow modification
            updated_item[0] = str(i)  # Update serial number
            updated_cart_items.append(updated_item)
        self.cart_items = updated_cart_items

        # Update cart section
        self.create_cart_section()

        # Update total price, taxes, and amount after removal
        total_price = sum(float(item[5][1:]) for item in self.cart_items)
        total_taxes = sum(float(item[6][1:]) for item in self.cart_items)
        total_amount = sum(float(item[7][1:]) for item in self.cart_items)

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
        column_widths = [10, 30, 10, 15, 10, 15, 15, 15, 10]
        for i, item in enumerate(self.cart_items, start=2):
            for j, value in enumerate(item, start=1):
                label = Label(
                    self.cart_inner_frame,
                    text=value,
                    font=("calibri", 15),
                    width=column_widths[j - 1],
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
                    row=i, column=len(column_widths)
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
            text="Total Price : ₹ ",
            font=("calibri", 20, "bold"),
            bg="#5C509C",
            fg="white",
        )
        total_price_label.grid(row=0, column=5, columnspan=3, padx=10, pady=10)
        total_taxes_label = Label(
            cart_head,
            text="Total Taxes : ₹ ",
            font=("calibri", 20, "bold"),
            bg="#5C509C",
            fg="white",
        )
        total_taxes_label.grid(row=0, column=9, columnspan=3, padx=10, pady=10)
        total_amount_label = Label(
            cart_head,
            text="Total Amount : ₹ ",
            font=("calibri", 20, "bold"),
            bg="#5C509C",
            fg="white",
        )
        total_amount_label.grid(row=0, column=12, columnspan=3, padx=10, pady=10)
        # Create a frame for column titles

    def create_cart_section(self):
        column_titles_frame = Frame(self.master, bg="#5C509C", name="columntitles")
        column_titles_frame.pack(fill=X, padx=10)

        # Column titles
        column_titles = [
            "S.No",
            "Product",
            "Quantity",
            "Price",
            "Discount",
            "Amount",
            "Taxes",
            "Total",
            "Remove",
        ]
        # Define the widths of each column
        column_widths = [10, 30, 10, 15, 10, 15, 15, 15, 10]
        column_titles_frame = Frame(self.master, bg="#5C509C", name="columntitles")
        column_titles_frame.pack(fill=X, padx=10)

        # Add column titles
        for i, title in enumerate(column_titles):
            # Create a frame for each column title label
            frame = Frame(
                column_titles_frame, width=column_widths[i], height=30, bg="white"
            )
            frame.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")

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
                separator = Frame(column_titles_frame, width=3, bg="black")
                separator.grid(row=0, column=i, rowspan=1, sticky="nse", padx=5)

        # Resize the weights of the columns to make them expandable
        for i in range(len(column_titles)):
            column_titles_frame.grid_columnconfigure(i, weight=1)

        self.cart_frame = Frame(self.master, bg="#5C509C", name="cartframe")
        self.cart_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

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

    def add_to_cart(self):
        product_name = self.Product.get()
        quantity = int(self.Quantity.get())
        price = float(self.Price.get()[1:])
        original_discount = float(self.Discount.get()[:-2])
        discount = (price * original_discount / 100) * quantity
        amount = float(quantity) * price

        gst = 0.18
        tax = amount * gst
        amount = float(amount - discount)
        self.Product.set("")
        self.Quantity.set("")
        self.Price.set("")
        self.Discount.set("")

        # Append the new item to cart_items
        self.cart_items.append(
            (
                len(self.cart_items) + 1,
                product_name,
                str(quantity),
                f"₹{price:.2f}",
                f"₹{discount:.2f}",
                f"₹{amount:.2f}",
                f"₹{tax:.2f}",
                f"₹{amount + tax:.2f}",
            )
        )

        # Update cart section
        self.create_cart_section()

        # Update total price, taxes, and amount after adding the item
        self.total_price = sum(float(item[5][1:]) for item in self.cart_items)
        self.total_taxes = sum(float(item[6][1:]) for item in self.cart_items)
        self.total_amount = sum(float(item[7][1:]) for item in self.cart_items)

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

        column_widths = [10, 30, 10, 15, 10, 15, 15, 15, 10]
        for i, item in enumerate(self.cart_items, start=2):
            for j, value in enumerate(item, start=1):
                label = Label(
                    self.cart_inner_frame,
                    text=value,
                    font=("calibri", 15),
                    width=column_widths[j - 1],
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
            width=25,
        ).grid(row=1, column=6)
        Entry(bill_frame, textvariable=self.Price, font=("calibri", 15), width=25).grid(
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
        print_button = Button(
            bill_frame,
            text="Print",
            font=("calibri", 15),
            bg="#FF5733",
            fg="white",
            command=self.print,
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

    def print(self):
        # Generate a unique transaction ID
        while True:
            transaction_id = random.randint(10000, 99999)
            if not self.sales_manager.get_transaction(transaction_id):
                break

        # Calculate total quantity and total discount
        total_quantity = sum(int(item[2]) for item in self.cart_items)
        total_discount = sum(float(item[4][1:]) for item in self.cart_items)
        total_price = sum(float(item[3][1:]) for item in self.cart_items)

        # Get customer ID, payment method, and employee ID from the GUI variables
        customer_id = 4567  # self.ph_no.get()  # Assuming this is the customer ID
        payment_method = "Cash"  # Assuming payment method is hardcoded to Cash
        employee_id = (
            "sk0311"  # self.emp_name.get()  # Assuming this is the employee ID
        )
        profit = 21212121
        locationid = 890
        # Prepare transaction data
        transaction_data = {
            "TransactionID": str(transaction_id),
            "ShopID": "123",  # Assuming ShopID is hardcoded
            "Quantity": total_quantity,
            "Discount": total_discount,
            "CustomerID": customer_id,
            "TotalPrice": total_price,
            "Tax": self.total_taxes,
            "Profit": profit,
            "NetSales": self.total_amount,
            "PaymentMethod": payment_method,
            "EmployeeID": employee_id,
            "LocationID": locationid,
            # Include other transaction details as needed
        }

        # Assuming sales_manager has a method for adding new transactions
        if self.sales_manager.add_transaction(transaction_data):
            # Update GUI or perform other actions upon successful addition
            messagebox.showinfo("Success", "Transaction Added")
        else:
            # Handle failure to add transaction
            messagebox.showerror("Error", "Transaction cannot be added.")

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
                    self.master, self.Product, self.Quantity, self.Price, self.Discount
                )
                self.data_frame.pack(pady=10)

                # Position the tooltip frame below the entry
                x, y, _, _ = self.product_name_entry.bbox("insert")

                self.data_frame.place(x=10, y=215)

            if not self.data_frame.listbox_created:
                self.data_frame.createBox()
            self.data_frame.update_data(matching_data)
        else:
            if self.data_frame is not None and self.data_frame.winfo_exists():
                self.data_frame.destroy()

    def item_selected(self):
        pass


if __name__ == "__main__":
    root = Tk()
    app = BillBookApp(root)
    root.mainloop()
