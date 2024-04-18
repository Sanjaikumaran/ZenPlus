import tkinter as tk
from tkinter import StringVar, OptionMenu
import datetime
import re  # for regular expressions
from database import (
    operations,
)  # Assuming operations module exists with necessary functionalities


class BasePage:
    def __init__(self, root, title, fields, buttons, on_button_click):
        self.frame = tk.Frame(root, padx=50, pady=100)
        self.frame.pack(padx=50, pady=50)
        self.frame.configure(bg="#3C0753")
        self.fields = {}
        self.buttons = []

        for field_name, field_type, options, grid_options, validate_func in fields:
            label = tk.Label(self.frame, text=f"{field_name}:")
            label.grid(
                row=grid_options["row"],
                column=grid_options["column"],
                padx=10,
                pady=5,
                sticky=tk.E,
            )
            if field_type == "entry":
                entry = tk.Entry(self.frame, **options)
                entry.grid(
                    row=grid_options["row"],
                    column=grid_options["column"] + 1,
                    padx=10,
                    pady=5,
                    ipady=5,
                )
                if validate_func:
                    entry.config(validate="key", validatecommand=(validate_func, "%P"))
                self.fields[field_name] = entry
            elif field_type == "option_menu":
                clicked = StringVar()
                clicked.set(options[0])
                option_menu = OptionMenu(self.frame, clicked, *options)
                option_menu.grid(
                    row=grid_options["row"],
                    column=grid_options["column"] + 1,
                    padx=10,
                    pady=5,
                )
                self.fields[field_name] = clicked

        for button_text, command in buttons:
            button = tk.Button(self.frame, text=button_text, command=command)
            button.grid(
                row=command["grid_options"]["row"],
                column=command["grid_options"]["column"],
                pady=10,
            )
            self.buttons.append(button)

        window_width = root.winfo_reqwidth()
        window_height = root.winfo_reqheight()
        center_x = window_width // 2
        center_y = window_height // 2

        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        additional_label_text, additional_label_command = on_button_click
        self.additional_label = tk.Label(
            self.frame, text=additional_label_text, fg="blue", cursor="hand2"
        )
        self.additional_label.bind("<Button-1>", additional_label_command)
        self.additional_label.grid(
            row=command["grid_options"]["row"],
            column=command["grid_options"]["column"] - 1,
            padx=10,
            pady=5,
        )


def validate_alphabets(new_value):
    return new_value.isalpha() or new_value == ""


def validate_numbers(new_value):
    return new_value.isdigit() or new_value == ""


def validate_email(email):
    # Regular expression pattern for basic email validation
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(EMAIL_REGEX, email) is not None


def validate_mobile_number(new_value):
    return len(new_value) == 10 and new_value.isdigit()


def validate_strong_password(new_value):
    # Check if password has at least 8 characters, contains both uppercase and lowercase letters,
    # and has at least one digit and one special character
    return (
        len(new_value) >= 8
        and any(char.isupper() for char in new_value)
        and any(char.islower() for char in new_value)
        and any(char.isdigit() for char in new_value)
        and any(not char.isalnum() for char in new_value)
    )


def validate_website_url(new_value):
    # You can implement more sophisticated URL validation if needed
    # For simplicity, we're just checking if the input starts with http:// or https://
    return new_value.startswith("http://") or new_value.startswith("https://")


class SignUp(BasePage):
    def __init__(self, root):
        fields = [
            ("Shop Name", "entry", {}, {"row": 0, "column": 0}, validate_alphabets),
            ("Branch", "entry", {}, {"row": 1, "column": 0}, validate_alphabets),
            ("Owner Name", "entry", {}, {"row": 2, "column": 0}, validate_alphabets),
            (
                "Mobile Number",
                "entry",
                {},
                {"row": 3, "column": 0},
                validate_numbers,
            ),  # Corrected validation
            ("Website URL", "entry", {}, {"row": 4, "column": 0}, validate_website_url),
            ("Email Address", "entry", {}, {"row": 5, "column": 0}, validate_email),
            (
                "GST Number",
                "entry",
                {},
                {"row": 6, "column": 0},
                validate_numbers,
            ),  # Corrected validation
            (
                "Password",
                "entry",
                {"show": "*"},
                {"row": 7, "column": 0},
                validate_strong_password,
            ),
            (
                "User Type",
                "option_menu",
                ["Admin", "Manager", "Employee"],
                {"row": 8, "column": 0},
                None,
            ),
        ]
        buttons = [
            (
                "Sign Up",
                {"command": self.on_signup, "grid_options": {"row": 9, "column": 1}},
            )
        ]
        additional_label_text = "Already have user?, Login!"
        additional_label_command = lambda event: LoginPage(event.widget.master.master)
        super().__init__(
            root,
            "Sign Up",
            fields,
            buttons,
            (additional_label_text, additional_label_command),
        )

    def on_signup(self):
        username = self.fields["Username"].get()
        password = self.fields["Password"].get()
        usertype = self.fields["User Type"].get()

        if "Admin" in usertype:
            usetype = "ADN"
        elif "Manager" in usertype:
            usetype = "MNG"
        else:
            usetype = "EMP"

        current_time = datetime.datetime.now()
        userId = f"{current_time.strftime('%Y')}{usetype}{current_time.strftime('%m%d%H%M%S')}{len(username)}"
        operations.AdminControlls().AddUser(username, userId, password, usertype)


class LoginPage(BasePage):
    def __init__(self, root):
        fields = [
            ("Username", "entry", {}, {"row": 0, "column": 0}),
            ("Password", "entry", {"show": "*"}, {"row": 1, "column": 0}),
        ]
        buttons = [
            (
                "Login",
                {"command": self.on_login, "grid_options": {"row": 2, "column": 1}},
            )
        ]
        additional_label_text = "Don't have user?, Sign Up!"
        additional_label_command = lambda event: SignUp(event.widget.master.master)
        super().__init__(
            root,
            "Login",
            fields,
            buttons,
            (additional_label_text, additional_label_command),
        )

    def on_login(self):
        username = self.fields["Username"].get()
        password = self.fields["Password"].get()
        try:
            operations.AdminControlls().login(username, password)
        except Exception as e:
            # Handle the exception here, such as showing an error message
            print("An error occurred during login:", str(e))


# Example usage
root = tk.Tk()
LoginPage(root)
root.mainloop()
