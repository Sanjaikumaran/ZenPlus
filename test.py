from tkinter import *
import sqlite3


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
        self.master.state("normal")
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

        self.cart_items = []

        self.create_menu()
        self.create_customer_frame()
        self.create_item_bill_section()

    def create_menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        menu_items = [
            ("Sales", ["Daily Sales", "Gross Sales", "Shop-Wise", "Summary"]),
            ("Stock", ["Daily Sales", "Gross Sales", "Shop-Wise", "Summary"]),
            ("Report", ["Daily Sales", "Gross Sales", "Shop-Wise", "Summary"]),
        ]

        for label, items in menu_items:
            submenu = Menu(menu)
            menu.add_cascade(label=label, menu=submenu)
            for item in items:
                submenu.add_command(label=item)

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

    def create_cart_section(self):
        self.cart_frame = Frame(self.master, bg="#5C509C", name="cartframe")
        self.cart_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Create a canvas for the scrollable area
        cart_canvas = Canvas(self.cart_frame, bg="#5C509C")
        cart_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Add scrollbar for the canvas
        cart_scrollbar = Scrollbar(
            self.cart_frame, orient=VERTICAL, command=cart_canvas.yview
        )
        cart_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure canvas to use the scrollbar
        cart_canvas.config(yscrollcommand=cart_scrollbar.set)

        # Create a frame to contain the item rows
        self.cart_inner_frame = Frame(cart_canvas, bg="#5C509C")
        cart_canvas.create_window((0, 0), window=self.cart_inner_frame, anchor="nw")

        # Bind scrolling to the canvas
        def on_canvas_configure(event):
            cart_canvas.configure(scrollregion=cart_canvas.bbox("all"))

        self.cart_inner_frame.bind("<Configure>", on_canvas_configure)

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

        # Find the cart frame directly
        cart_frame = self.master.nametowidget(".cartframe")

        if cart_frame:
            self.cart_inner_frame = cart_frame.winfo_children()[0]

            matching_item_index = None
            for i, item in enumerate(self.cart_items):
                if (
                    item[1] == product_name
                    and float(item[3][1:]) == price
                    and float(item[4][1:]) == discount
                ):
                    matching_item_index = i
                    break

            if matching_item_index is not None:
                matching_item = self.cart_items[matching_item_index]
                item_quantity = int(matching_item[2])
                updated_quantity = str(item_quantity + quantity)
                updated_amount = f"₹{float(matching_item[5][1:]) + amount:.2f}"
                updated_tax = f"₹{float(matching_item[6][1:]) + tax:.2f}"
                updated_total = f"₹{float(matching_item[7][1:]) + amount + tax:.2f}"

                updated_item = (
                    matching_item[0],
                    matching_item[1],
                    updated_quantity,
                    matching_item[3],
                    matching_item[4],
                    updated_amount,
                    updated_tax,
                    updated_total,
                )
                self.cart_items[matching_item_index] = updated_item
            else:
                same_item = False
                for item in self.cart_items:
                    if item[1] == product_name and float(item[3][1:]) == price:
                        same_item = True
                        break
                if not same_item:
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

            # Update total price, taxes, and amount
            total_price = sum(float(item[5][1:]) for item in self.cart_items)
            total_taxes = sum(float(item[6][1:]) for item in self.cart_items)
            total_amount = sum(float(item[7][1:]) for item in self.cart_items)

            # Update labels with calculated values
            for child in self.master.winfo_children():
                if child.winfo_name() == "carthead":
                    for label in child.winfo_children():
                        if label.cget("text").startswith("Total Price"):
                            label.config(
                                text="Total Price : ₹ {:.2f}".format(total_price)
                            )
                        elif label.cget("text").startswith("Total Taxes"):
                            label.config(
                                text="Total Taxes : ₹ {:.2f}".format(total_taxes)
                            )
                        elif label.cget("text").startswith("Total Amount"):
                            label.config(
                                text="Total Amount : ₹ {:.2f}".format(total_amount)
                            )

            # Clear existing widgets inside the cart inner frame
            for widget in self.cart_inner_frame.winfo_children():
                widget.destroy()

            column_widths = [10, 30, 10, 15, 10, 15, 15, 15, 10]
            # Add items to the cart
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

            # Update the scroll region after adding new items
            self.cart_frame.update_idletasks()

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
        )
        add_item_button.grid(
            row=1, column=7, columnspan=3, rowspan=2
        )  # Spanning two rows and three columns, move to the right

        self.cart_head("", "", "")
        self.create_cart_section()

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
