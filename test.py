from tkinter import *
from tkinter import ttk, messagebox
from database import database  # Import your database module
from employee import EmployeeManagement

# Import your employee management module


class EmployeeManagementApp:
    columns = (
        "Employee ID",
        "Shop ID",
        "First Name",
        "Last Name",
        "Department",
        "Position",
        "Salary",
        "Hire Date",
    )

    def __init__(self, master):
        self.master = master
        self.master.title("Employee Management")
        self.master.config(bg="#382D72")
        self.master.attributes("-zoomed", True)
        self.employee_manager = (
            EmployeeManagement()
        )  # Initialize the employee management instance
        self.create_search_frame()
        self.create_table_frame()
        self.master.bind("<Alt-s>", lambda event: self.search_entry.focus())
        self.master.bind("<Alt-n>", lambda event: self.add_new_employee())
        self.master.bind("<Delete>", lambda event: self.remove_employee())
        self.master.bind("<Alt-e>", lambda event: self.edit_employee())
        self.master.bind("<Escape>", lambda event: self.close_windows_except_master())

    def close_windows_except_master(self):
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
        self.search_entry.bind("<KeyRelease>", self.search_employee)

        self.add_button = Button(
            self.search_frame, text="Add New", command=self.add_new_employee
        )
        self.edit_button = Button(
            self.search_frame, text="Edit ", command=self.edit_employee
        )
        self.remove_button = Button(
            self.search_frame, text="Remove ", command=self.remove_employee
        )

        self.remove_button.pack(side=RIGHT, padx=(5, 0))
        self.edit_button.pack(side=RIGHT, padx=(5, 0))
        self.add_button.pack(side=RIGHT, padx=(5, 0))

    def create_table_frame(self):
        self.table_frame = Frame(self.master)
        self.table_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.tree = ttk.Treeview(
            self.table_frame, columns=self.columns, show="headings"
        )

        for col in self.columns:
            self.tree.heading(col, text=col)

        self.original_data = (
            self.employee_manager.list_employees()
        )  # Get the initial employee data
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
            self.tree.insert("", "end", values=row)

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

    def search_employee(self, event=None):
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

    def add_new_employee(self, event=None):
        self.add_window = Toplevel(self.master)
        self.add_window.title("Add New Employee")
        self.add_window.bind("<Control-s>", lambda event: self.save_new_employee())
        self.add_window.bind("<Return>", lambda event: self.save_new_employee())

        self.labels = self.columns[2:]  # Exclude Employee ID and Shop ID
        self.entries = []
        for i, label in enumerate(self.labels):
            Label(self.add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(self.add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        save_button = Button(
            self.add_window, text="Save", command=self.save_new_employee
        )
        save_button.grid(row=len(self.labels), columnspan=2, padx=10, pady=10)

    def save_new_employee(self):
        employee_data = [entry.get() for entry in self.entries]
        columns = [
            "EmployeeID",
            "FirstName",
            "LastName",
            "Department",
            "Position",
            "Salary",
            "HireDate",
        ]
        employee_dict = dict(zip(columns, employee_data))
        print(employee_data)
        if self.employee_manager.add_employee(employee_dict):
            self.tree.delete(*self.tree.get_children())
            self.original_data = self.employee_manager.list_employees()
            self.insert_data_into_treeview(self.original_data)
            self.add_window.destroy()
            messagebox.showinfo("Success", "Employee Added")
        else:
            messagebox.showerror("Error", "Employee cannot be added.")

    def edit_employee(self, event=None):
        selected_items = self.tree.selection()
        if len(selected_items) != 1:
            messagebox.showinfo(
                "Edit Employee", "Please select exactly one employee to edit."
            )
            return
        selected_item = selected_items[0]
        if selected_item:
            selected_item_values = self.tree.item(selected_item, "values")
            self.edit_window = Toplevel(self.master)
            self.edit_window.title("Edit Employee")
            self.edit_window.bind(
                "<Control-s>", lambda event: self.save_changes(selected_item)
            )
            self.edit_window.bind(
                "<Return>", lambda event: self.save_changes(selected_item)
            )

            self.edit_window_entries = []
            for i, column in enumerate(
                self.columns[2:], start=2
            ):  # Exclude Employee ID and Shop ID
                Label(self.edit_window, text=f"{column}:").grid(
                    row=i - 2, column=0, padx=10, pady=5, sticky="e"
                )
                entry = Entry(self.edit_window)
                entry.insert(0, selected_item_values[i])
                entry.grid(row=i - 2, column=1, padx=10, pady=5)
                self.edit_window_entries.append(entry)

            save_button = Button(
                self.edit_window,
                text="Save Changes",
                command=lambda: self.save_changes(selected_item),
            )
            save_button.grid(row=len(self.columns) - 2, columnspan=2, padx=10, pady=10)
        else:
            messagebox.showinfo("Edit Employee", "Please select an employee to edit.")

    def save_changes(self, selected_item):
        employee_id_value = self.tree.item(selected_item, "values")[0]
        updated_values = [entry.get() for entry in self.edit_window_entries]
        if self.employee_manager.update_employee(employee_id_value, updated_values):
            self.tree.item(selected_item, values=updated_values)
            self.edit_window.destroy()
            messagebox.showinfo("Success", "Employee Updated")
        else:
            messagebox.showerror("Error", "Employee Cannot be Updated")

    def remove_employee(self, event=None):
        selected_items = self.tree.selection()
        if selected_items:
            confirmation_message = (
                "Are you sure you want to remove the selected employee(s)?"
            )
            if messagebox.askyesno("Confirm Removal", confirmation_message):
                for item in selected_items:
                    employee_id = self.tree.item(item, "values")[0]
                    self.tree.delete(item)
                    self.employee_manager.remove_employee(employee_id)
                if not self.tree.get_children():
                    messagebox.showinfo(
                        "All Rows Deleted", "All employees have been removed."
                    )
        else:
            messagebox.showinfo(
                "Remove Employee", "Please select an employee to remove."
            )


if __name__ == "__main__":
    root = Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
