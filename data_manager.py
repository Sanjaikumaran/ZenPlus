from tkinter import *
from tkinter import ttk, messagebox, font as tkFont
from database import database
import time
import random
from operations_access import DataManagement

# from products import product_management


class DataManager:

    def __init__(self, master, window, page, shop_id):

        self.master = master
        self.window = window
        self.master.pack(fill=BOTH, expand=True)

        self.shop_id = shop_id
        self.manager = DataManagement()
        self.page = page
        if page == "Product":
            self.window.title("Product Management")
            self.conditions_cols = '"SNo","Product ID"'
            self.list_columns = "ProductId, ProductName, Brand, CostPrice, SellingPrice, MRP, Discount, CurrentStock, HistoryStock, SoldStock, GST"
            self.list_table_name = "Products"
            self.remove_cols = [1, 2]
            self.columns = (
                "SNo",
                "Product ID",
                "Product Name",
                "Brand",
                "Cost Price",
                "Selling Price",
                "MRP",
                "Discount",
                "Current Stock",
                "History Stock",
                "Sold Stock",
                "GST",
            )
        elif page == "TransactionItems":

            self.window.title("Transaction Items Management")
            self.conditions_cols = "SNo"
            self.remove_cols = [1, 2]
            self.list_columns = " TransactionID, ProductID, Quantity, Price, Discount, Amount, Taxes, Total"
            self.list_table_name = "TransactionItems"
            self.columns = [
                "SNo",
                "Transaction ID",
                "Product ID",
                "Quantity",
                "Price",
                "Discount",
                "Amount",
                "Taxes",
                "Total",
            ]
        elif page == "Customer":

            self.window.title("Customers Management")
            self.conditions_cols = '"SNo", "Customer ID", "Timestamp"'
            self.remove_cols = [1, 2]
            self.list_columns = (
                "CustomerID,FirstName,LastName,Email,Phone,Address,City,Country"
            )
            self.list_table_name = "Customers"
            self.columns = [
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
        elif page == "Employee":

            self.window.title("Employee Management")
            self.conditions_cols = '"SNo", "Customer ID", "Timestamp"'
            self.remove_cols = [1, 2, 3]
            self.list_columns = "EmployeeID, ShopId, FirstName, LastName, Department, Position, Salary, Timestamp"
            self.list_table_name = "Employees"
            self.columns = [
                "SNo",
                "Employee ID",
                "Shop ID",
                "First Name",
                "Last Name",
                "Department",
                "Position",
                "Salary",
                "Timestamp",
            ]
        elif page == "Transactions":

            self.window.title("Transaction Management")
            self.conditions_cols = '"SNo", "Transaction ID", "Timestamp"'
            self.remove_cols = [1]
            self.list_columns = "TransactionID,Timestamp,Quantity,TotalPrice,CustomerID,PaymentMethod,Discount,Tax,NetSales,Profit,EmployeeID,LocationID"
            self.list_table_name = "Transactions"
            self.columns = [
                "SNo",
                "Transaction ID",
                "Timestamp",
                "Quantity",
                "Total Price",
                "Customer ID",
                "Payment Method",
                "Discount",
                "Tax",
                "Net Sales",
                "Profit",
                "Employee ID",
                "Location ID",
            ]

        self.create_search_frame()
        self.create_table_frame()
        self.window.bind("<Alt-s>", lambda event: self.search_entry.focus())
        self.window.bind("<Alt-n>", lambda event: self.add_new())
        self.window.bind("<Delete>", lambda event: self.remove())
        self.window.bind("<Alt-e>", lambda event: self.edit())
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

    def create_search_frame(self):
        self.search_frame = Frame(self.master, bg="#382D72")
        self.search_frame.pack(padx=10, pady=10, fill="x")

        self.search_label = Label(
            self.search_frame, text="Search:", bg="#382D72", fg="white"
        )
        self.search_label.pack(side=LEFT)

        self.search_entry = Entry(self.search_frame, bg="white", width=30)
        self.search_entry.pack(side=LEFT, padx=(5, 0), fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_items)

        self.add_button = Button(
            self.search_frame, text="Add New", command=self.add_new
        )
        self.edit_button = Button(self.search_frame, text="Edit ", command=self.edit)
        self.remove_button = Button(
            self.search_frame, text="Remove ", command=self.remove
        )

        self.remove_button.pack(side=RIGHT, padx=(5, 0))
        self.edit_button.pack(side=RIGHT, padx=(5, 0))
        self.add_button.pack(side=RIGHT, padx=(5, 0))

    def create_table_frame(self):
        self.table_frame = Frame(self.master)
        self.table_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.tree = MultiColumnListbox(
            self.table_frame,
            columns=self.columns,
            show="headings",
        )

        for col in self.columns:
            self.tree.heading(col, text=col)
        for col in self.columns:
            self.tree.column(col, width=tkFont.Font().measure(col))

        self.original_data = self.manager.list_items(
            self.list_table_name, self.list_columns
        )

        self.insert_data_into_treeview(self.original_data)

        for col in self.columns:
            self.tree.heading(
                col, text=col, command=lambda _col=col: self.treeview_sort_column(_col)
            )

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        yscrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview
        )
        yscrollbar.pack(side=RIGHT, fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)

    def insert_data_into_treeview(self, data):
        for i, row in enumerate(data, start=1):
            self.tree.insert("", "end", values=(i,) + row)

    def treeview_sort_column(self, col):
        values = [
            (self.tree.set(child, col), child) for child in self.tree.get_children("")
        ]
        try:
            sorted_values = sorted(values, key=lambda x: float(x[0]))
        except ValueError:
            sorted_values = sorted(values)
        for index, (val, child) in enumerate(sorted_values):
            self.tree.move(child, "", index)

    def search_items(self, event=None):
        self.search_entry.focus()
        query = self.search_entry.get().lower()
        if query:
            self.tree.delete(*self.tree.get_children())
            filtered_data = [
                row
                for row in self.original_data
                if any(query in str(value).lower() for value in row)
            ]
            self.insert_data_into_treeview(filtered_data)
        else:
            self.tree.delete(*self.tree.get_children())
            self.insert_data_into_treeview(self.original_data)

    def add_new(self, event=None):
        self.add_window = Toplevel(self.master)
        self.add_window.title(f"Add New {self.page}")
        self.add_window.bind("<Control-s>", lambda event: self.save_new())
        self.add_window.bind("<Return>", lambda event: self.save_new())
        self.add_window.bind("<Escape>", lambda event: self.add_window.destroy())

        # Exclude trsave_new ID and Shop ID from the labels
        if not self.page == "TransactionItems":
            self.labels = self.columns[2:]
        else:
            self.labels = self.columns[2:]

        self.entries = []

        for i, label in enumerate(self.labels):
            Label(self.add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(self.add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        save_button = Button(self.add_window, text="Save", command=self.save_new)
        save_button.grid(row=len(self.labels) + 1, columnspan=2, padx=10, pady=10)

    def save_new(self):
        unique_id = self.generate_id()

        # Get data from entry widgets and construct a dictionary

        transaction_data = {list(self.list_columns.split(","))[0]: unique_id}
        for label, entry in zip(self.labels, self.entries):
            # Remove spaces from column names
            column_name = label.replace(" ", "")
            transaction_data[column_name] = entry.get()

        # Generate a random transaction ID not in the table

        transaction_data["SNo"] = len(self.original_data) + 1

        transaction_data["ShopID"] = self.shop_id
        if not self.page == "TransactionItems":
            transaction_data["Timestamp"] = self.current_time

        # Assuming manager has a method for adding new transactions
        if self.manager.add_item(self.list_table_name, transaction_data):
            self.tree.delete(*self.tree.get_children())
            self.original_data = self.manager.list_items(
                self.list_table_name, self.list_columns
            )
            for i, row in enumerate(self.original_data, start=1):
                self.tree.insert("", "end", values=(i,) + row)
            self.add_window.destroy()
            messagebox.showinfo("Success", f"{self.page} Added")
        else:
            self.add_window.destroy()
            messagebox.showerror("Error", f"{self.page} cannot be added.")

    def edit(self, event=None):
        selected_items = self.tree.selection()
        if len(selected_items) != 1:
            messagebox.showinfo(
                f"Edit {self.page}", f"Please select exactly one {self.page} to edit."
            )
            return
        selected_item = selected_items[0]
        if selected_item:
            selected_item_values = self.tree.item(selected_item, "values")
            self.edit_window = Toplevel(self.master)
            self.edit_window.title(f"Edit {self.page}")
            self.edit_window.bind(
                "<Control-s>", lambda event: self.save_changes(selected_item)
            )
            self.edit_window.bind(
                "<Return>", lambda event: self.save_changes(selected_item)
            )
            self.edit_window.bind("<Escape>", lambda event: self.edit_window.destroy())

            self.edit_window_entries = []
            for i, column in enumerate(self.columns):
                if column in (self.conditions_cols):
                    entry = Entry(self.edit_window)
                    entry.insert(0, selected_item_values[i])
                    self.edit_window_entries.append(entry)
                    entry.grid_forget()
                else:
                    Label(self.edit_window, text=f"{column}:").grid(
                        row=i, column=0, padx=10, pady=5, sticky="e"
                    )
                    entry = Entry(self.edit_window)
                    entry.insert(0, selected_item_values[i])
                    entry.grid(row=i, column=1, padx=10, pady=5)
                    self.edit_window_entries.append(entry)

            save_button = Button(
                self.edit_window,
                text="Save Changes",
                command=lambda: self.save_changes(selected_item),
            )
            save_button.grid(row=len(self.columns), columnspan=2, padx=10, pady=10)
        else:
            messagebox.showinfo(
                f"Edit {self.page}", f"Please select a {self.page} to edit."
            )

    def save_changes(self, selected_item):
        sno_value = self.tree.item(selected_item, "values")[0]
        default_values = {
            self.columns[i].replace(" ", ""): self.tree.item(selected_item, "values")[i]
            for i in self.remove_cols
        }

        updated_values = {}
        for i, entry in enumerate(self.edit_window_entries):
            if i == 0:
                continue
            elif i == 2:
                updated_values[self.columns[i]] = entry.get()
                continue
            else:
                updated_values[self.columns[i]] = entry.get()

        modified_values = {}
        for key, value in updated_values.items():
            modified_values[key.replace(" ", "")] = value
        new_values = [sno_value] + list(updated_values.values())
        self.tree.item(selected_item, values=new_values)
        self.edit_window.destroy()

        if self.manager.update_item(
            self.list_table_name, default_values, modified_values
        ):
            messagebox.showinfo("Success", f"{self.page} Updated")
        else:
            messagebox.showerror("Error", f"{self.page} cannot be Updated")

    def remove(self, event=None):
        selected_items = self.tree.selection()

        if selected_items:
            # Extract transaction ids with labels
            selected_transaction_ids = [
                {
                    self.columns[i].replace(" ", ""): self.tree.item(item, "values")[i]
                    for i in self.remove_cols
                }
                for item in selected_items
            ]

            # Create confirmation message
            confirmation_message = (
                f"Are you sure you want to remove the following {self.page}?\n\n"
            )
            confirmation_message += "\n".join(
                ",".join(map(str, transaction_id.values()))
                for transaction_id in selected_transaction_ids
            )

            # Confirm removal with user
            if messagebox.askyesno("Confirm Removal", confirmation_message):
                # Attempt to delete each selected item from the tree
                for item in selected_items:
                    try:
                        self.tree.delete(item)
                    except tk.TclError as e:
                        print(f"Error deleting item {item}: {e}")

                # Initialize lists to track deletion results
                deleted_items = [[], []]  # [successfully_deleted, failed_to_delete]

                # Iterate over the selected transactions and attempt to remove them using the manager
                for transaction_id_dict in selected_transaction_ids:
                    if self.manager.remove_item(
                        self.list_table_name, transaction_id_dict
                    ):
                        deleted_items[0].append(
                            ",".join(map(str, transaction_id_dict.values()))
                        )
                    else:
                        deleted_items[1].append(
                            ",".join(map(str, transaction_id_dict.values()))
                        )

                # Display appropriate message based on deletion results
                if deleted_items[0] and deleted_items[1]:
                    messagebox.showinfo(
                        "Success",
                        f"{self.page} { ','.join(map(str, deleted_items[0]))} Removed",
                    )
                    messagebox.showerror(
                        "Error",
                        f"{self.page} {','.join(map(str, deleted_items[1]))} Cannot be Removed",
                    )
                elif deleted_items[0]:
                    messagebox.showinfo(
                        "Success",
                        f"{self.page} {','.join(map(str, deleted_items[0]))} Removed",
                    )
                elif deleted_items[1]:
                    messagebox.showerror(
                        "Error",
                        f"{self.page} {','.join(map(str, deleted_items[1]))} Cannot be Removed",
                    )

                # Check if all {self.page} have been removed
                if not self.tree.get_children():
                    messagebox.showinfo(
                        "All Rows Deleted", f"All {self.page} have been removed."
                    )
        else:
            messagebox.showinfo(
                f"Remove {self.page}", f"Please select a {self.page} to remove."
            )

    def generate_id(self):
        if self.page == "Customer":
            return self.entries[4].get()
        else:
            last_id = self.manager.get_last_item(
                self.list_table_name, list(self.list_columns.split(","))[0]
            )

            if self.page == "Transactions":
                id_type = "TRN"
            elif self.page == "Product":
                id_type = "PRD"
            elif self.page == "Employee":
                id_type = "EMP"
            else:
                return str(
                    self.manager.get_last_item(
                        "Transactions", list(self.list_columns.split(","))[0]
                    )[0]
                )
            return id_type + str(int(last_id[0][3:]) + 1)

    def destroy(self):
        # Destroy all children of the master widget
        for child in self.master.winfo_children():
            child.destroy()


class MultiColumnListbox(ttk.Treeview):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._columns = None
        self.tag_configure("button", foreground="blue", font=("Arial", 10, "underline"))
        self.tag_bind("button", "<ButtonRelease-1>", self.button_click)

    def button_click(self, event):
        item = self.identify("item", event.x, event.y)
        column = self.identify_column(event.x)
        if column == "#13":
            self.event_generate("<<EditButtonClicked>>", when="tail")
        elif column == "#14":
            self.event_generate("<<RemoveButtonClicked>>", when="tail")

    def insert(self, parent, index, *args, **kwargs):
        super().insert(parent, index, *args, **kwargs)
        self.tag_configure("button", foreground="blue", font=("Arial", 10, "underline"))


if __name__ == "__main__":
    root = Tk()
    app = transactionItemsManagementApp(root, root, "TransactionItems")
    root.mainloop()
