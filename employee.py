from database import operations
import time


class EmployeeManagement:
    def __init__(self):
        # Initialize database operations instance
        self.ops = operations.Operations()

        # Get current timestamp
        self.current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Method to add a new employee
    def add_employee(self, employee_data):
        # Call insert_row method to add employee record
        self.ops.insert_row("Employees", employee_data)

    # Method to update an employee record
    def update_employee(self, employee_id, updated_values):
        # Define where conditions to identify the row to be updated
        where_conditions = {"EmployeeID": employee_id}

        # Call update_row method to update employee record
        self.ops.update_row("Employees", updated_values, where_conditions)

    # Method to remove an employee record
    def remove_employee(self, employee_id):
        # Define where conditions to identify the row to be removed
        where_conditions = {"EmployeeID": employee_id}

        # Call remove_row method to remove employee record
        self.ops.remove_row("Employees", where_conditions)

    # Additional methods for employee-related operations can be defined here


if __name__ == "__main__":
    # Create an instance of the ShopManagement class
    employee_management = EmployeeManagement()

    # Add a new employee
    employee_data = {
        "EmployeeID": 3,
        "ShopId": "123",
        "FirstName": "John",
        "LastName": "Doe",
        "Department": "Sales",
        "Position": "Sales Associate",
        "Salary": 50000.00,
        "HireDate": "2024-04-20",
    }
    employee_management.add_employee(employee_data)

    ## Update an existing employee
    # updated_values = {"Salary": 55000.00}
    # employee_management.update_employee(1, updated_values)

    ## Remove an employee
    # employee_management.remove_employee(1)
