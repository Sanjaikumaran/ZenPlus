from tkinter import *
from tkinter import ttk, messagebox
from database import database
from products import product_management


class ProductManagementApp:
    columns = (
        "Sno",
        "Product Name",
        "Product ID",
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

    def __init__(self, master):
        self.master = master
        self.master.title("Product Management")
        self.master.config(bg="#382D72")
        self.master.attributes("-zoomed", True)
        self.product_manager = product_management()
        self.create_search_frame()
        self.create_table_frame()
        self.master.bind("<Alt-s>", lambda event: self.search_entry.focus())
        self.master.bind("<Alt-n>", lambda event: self.add_new_product())
        self.master.bind("<Delete>", lambda event: self.remove_product())
        self.master.bind("<Alt-e>", lambda event: self.edit_product())
        self.master.bind("<Escape>", lambda event: self.close_windows_except_master)

    def close_windows_except_master(self):
        # Destroy all Toplevel windows except the master window
        for window in self.master.winfo_children():
            if isinstance(window, Toplevel):
                window.destroy()

    def create_search_frame(self):
        self.search_frame = Frame(self.master, bg="#382D72")
        self.search_frame.pack(padx=10, pady=10, fill="x")

        self.search_label = Label(
            self.search_frame, text="Search:", bg="#382D72", fg="white"
        )
        self.search_label.pack(side=LEFT)

        self.search_entry = Entry(self.search_frame, bg="white", width=30)
        self.search_entry.pack(side=LEFT, padx=(5, 0), fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_product)

        self.add_button = Button(
            self.search_frame, text="Add New", command=self.add_new_product
        )
        self.edit_button = Button(
            self.search_frame, text="Edit ", command=self.edit_product
        )
        self.remove_button = Button(
            self.search_frame, text="Remove ", command=self.remove_product
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

        self.original_data = self.product_manager.list_products()
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

    def search_product(self, event=None):
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

    def add_new_product(self, event=None):
        self.add_window = Toplevel(self.master)
        self.add_window.title("Add New Product")
        self.add_window.bind("<Control-s>", lambda event: self.save_new_product())
        self.add_window.bind("<Return>", lambda event: self.save_new_product())

        self.labels = self.columns[1:]
        self.entries = []
        for i, label in enumerate(self.labels):
            Label(self.add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(self.add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        save_button = Button(
            self.add_window, text="Save", command=self.save_new_product
        )
        save_button.grid(row=len(self.labels), columnspan=2, padx=10, pady=10)

    def save_new_product(self):
        product_name = self.entries[0].get()
        product_id = self.entries[1].get()
        brand = self.entries[2].get()
        cost_price = self.entries[3].get()
        selling_price = self.entries[4].get()
        mrp = self.entries[5].get()
        discount = self.entries[6].get()
        current_stock = self.entries[7].get()
        history_stock = self.entries[8].get()
        sold_stock = self.entries[9].get()
        gst = self.entries[10].get()
        shop_id = "123"
        product_exists = any(product_id == row[1] for row in self.original_data)
        if product_exists:
            messagebox.showerror("Error", "Product ID already exists.")
        else:
            if self.product_manager.add_product(
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
                self.tree.delete(*self.tree.get_children())
                self.original_data = self.product_manager.list_products()
                for i, row in enumerate(self.original_data, start=1):
                    self.tree.insert("", "end", values=(i,) + row)
                self.add_window.destroy()
                messagebox.showinfo("Success", "Product Added")
            else:
                self.add_window.destroy()
                messagebox.showerror("Error", "Product cannot be added.")

    def edit_product(self, event=None):
        selected_items = self.tree.selection()
        if len(selected_items) != 1:
            messagebox.showinfo(
                "Edit Product", "Please select exactly one product to edit."
            )
            return
        selected_item = selected_items[0]
        if selected_item:
            selected_item_values = self.tree.item(selected_item, "values")
            self.edit_window = Toplevel(self.master)
            self.edit_window.title("Edit Product")
            self.edit_window.bind(
                "<Control-s>", lambda event: self.save_changes(selected_item)
            )
            self.edit_window.bind(
                "<Return>", lambda event: self.save_changes(selected_item)
            )

            self.edit_window_entries = []
            for i, column in enumerate(self.columns):
                if column in ("Sno", "Product ID"):
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
            messagebox.showinfo("Edit Product", "Please select a product to edit.")

    def save_changes(self, selected_item):
        sno_value = self.tree.item(selected_item, "values")[0]
        product_id_value = self.tree.item(selected_item, "values")[2]
        updated_values = {}
        for i, entry in enumerate(self.edit_window_entries):
            if i == 0:
                continue
            elif i == 2:
                updated_values[self.columns[i]] = entry.get()
                continue
            else:
                updated_values[self.columns[i]] = entry.get()
        shop_id = "123"
        modified_values = {}
        for key, value in updated_values.items():
            modified_values[key.replace(" ", "")] = value
        new_values = [sno_value] + list(updated_values.values())
        self.tree.item(selected_item, values=new_values)
        self.edit_window.destroy()
        if self.product_manager.update_product(
            shop_id, product_id_value, modified_values
        ):
            messagebox.showinfo("Success", "Product Updated")
        else:
            messagebox.showerror("Error", "Product Cannot be Updated")

    def remove_product(self, event=None):
        selected_items = self.tree.selection()
        if selected_items:
            selected_product_ids = [
                self.tree.item(item, "values")[2] for item in selected_items
            ]
            confirmation_message = (
                f"Are you sure you want to remove the following products?\n\n"
            )
            confirmation_message += "\n".join(selected_product_ids)
            if messagebox.askyesno("Confirm Removal", confirmation_message):
                for item in selected_items:
                    try:
                        self.tree.delete(item)
                    except tk.TclError:
                        pass
                for product_id in selected_product_ids:
                    self.product_manager.remove_product("123", product_id)
                if not self.tree.get_children():
                    messagebox.showinfo(
                        "All Rows Deleted", "All products have been removed."
                    )
        else:
            messagebox.showinfo("Remove Product", "Please select a product to remove.")


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
    app = ProductManagementApp(root)
    root.mainloop()
