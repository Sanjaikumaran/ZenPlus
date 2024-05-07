from tkinter import *
from tkinter import messagebox
from database import database
from cryptography.fernet import Fernet


class Login:

    def __init__(self, root, callback):
        self.root = root

        self.callback = callback
        self.root.title("Login")
        self.root.config(bg="#382D72")
        self.root.attributes("-zoomed", True)

        # Title shop name----------------
        self.entries_frame = Frame(self.root, bg="#382D72")
        self.entries_frame.pack(side=TOP, fill=X)
        self.title = Label(
            self.entries_frame,
            text="Welcome To Zen Plus",
            font=("calibri", 45, "bold"),
            bg="#382D72",
            fg="white",
        )
        self.title.pack(pady=100)

        #  login frame start ---------------
        self.login_frame = Frame(self.root, bg="#6A6097")
        self.login_frame.pack()

        self.username = StringVar()
        self.password = StringVar()

        #  username ---------------
        label = Label(
            self.login_frame,
            text="Email Address",
            font=("calibri", 20, "bold"),
            bg="#6A6097",
            fg="white",
        )
        label.grid(row=0, column=0)
        self.textname = Entry(
            self.login_frame, textvariable=self.username, font=("calibri", 15), width=25
        )
        self.textname.grid(row=0, column=1, pady=20, padx=10)

        #  password ---------------
        label = Label(
            self.login_frame,
            text="Password",
            font=("calibri", 20, "bold"),
            bg="#6A6097",
            fg="white",
        )
        label.grid(row=1, column=0)
        self.textpass = Entry(
            self.login_frame,
            textvariable=self.password,
            font=("calibri", 15),
            width=25,
            show="*",
        )
        self.textpass.grid(row=1, column=1, pady=20, padx=10)
        #  button ---------
        btn_signup = Button(
            self.login_frame,
            command=lambda: self.destroy("SignUp"),  # Use lambda to pass arguments
            text="Sign Up",
            bg="#E5CCF4",
            padx=10,
            pady=10,
            font=("calibri", 15, "bold"),
            width=10,
        )
        btn_signup.grid(row=3, column=2, padx=10, pady=20)

        self.btnlog = Button(
            self.login_frame,
            command=self.login,
            text="log in",
            bg="#E5CCF4",
            padx=10,
            pady=10,
            font=("calibri", 15, "bold"),
            width=20,
        )
        self.btnlog.grid(row=3, column=0, columnspan=2, pady=20)

    def login(self):
        # Here you can implement your login logic
        username = self.textname.get()
        password = self.textpass.get()
        if self.root.success_remote:
            query = "SELECT * FROM ShopList WHERE EmailAddress = %s AND Password = %s"
            data = (username, password)
            try:
                # Execute the insert query
                self.root.cursor_remote.execute(query, data)

                row = self.root.cursor_remote.fetchone()
                if row:

                    # Generate a key for encrypsignup_frametion
                    key = self.generate_key()
                    str(row)

                    # Encrypt the configuration file using the key
                    self.encrypt_config(key, str(row))

                    messagebox.showinfo("Success", "Login Successfull")
                    self.destroy("Success")
                else:
                    messagebox.showerror("Error", "Wrong Email Address or Password")
            except Exception as e:
                # Handle any errors that may occur during insertion
                print("Error:", e)
                # self.cnx_remote.rollback()
                messagebox.showerror(
                    "Error", "An error occurred. Please try again later."
                )
        else:
            messagebox.showerror("Internet not connected.")

    # Generate a key for encryption
    def generate_key(self):
        return Fernet.generate_key()

    def encrypt_config(self, key, config_data):
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(config_data.encode())
        with open("configure.enc", "wb") as f:
            # Write the encryption key at the beginning of the file
            f.write(key + b"\n")
            # Write the encrypted data
            f.write(encrypted_data)

    def destroy(self, message):
        # Destroy all the children widgets of the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.callback(message)


if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
