import tkinter as tk
from tkinter import ttk
from database import database
import time


class BillBookApp:
    success_remote, cnx_remote, cursor_remote, error_remote = (
        database.connect_to_remote_db()
    )

    def __init__(self, root):

        self.root = root
        self.root.title("Bill Book")
        self.root.config(bg="#382D72")
        self.root.attributes("-zoomed", True)
        current_time = time.time()
        self.current_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(current_time)
        )

        self.create_widgets()

    def create_widgets(self):
        self.create_title()
        self.create_signup_frame()

    def create_title(self):
        title_frame = tk.Frame(self.root, bg="#382D72")
        title_frame.pack(side=tk.TOP, fill=tk.X)
        title = tk.Label(
            title_frame,
            text="Welcome To Bill Sheet",
            font=("calibri", 45, "bold"),
            bg="#382D72",
            fg="white",
        )
        title.pack(pady=40)

    def create_signup_frame(self):
        signup_frame = tk.Frame(self.root, bg="#6A6097")
        signup_frame.pack()

        labels = [
            "Email Address",
            "Password",
            "GST No.",
            "Mobile Number",
            "Shop Name",
            "Owner Name",
            "Branch",
            "Website URL",
            "Greetings Message",
        ]
        self.entries = [
            tk.StringVar() for _ in range(len(labels))
        ]  # Assign to self.entries

        for i, label_text in enumerate(labels):
            label = tk.Label(
                signup_frame,
                text=label_text,
                font=("calibri", 18, "bold"),
                bg="#6A6097",
                fg="white",
            )
            label.grid(row=i, column=0, padx=10, sticky="w")

            entry = tk.Entry(
                signup_frame,
                textvariable=self.entries[i],
                font=("calibri", 15),
                width=25,
            )
            entry.grid(row=i, column=1, pady=20, padx=15, sticky="w")

        btn_signup = tk.Button(
            signup_frame,
            command=self.signup,
            text="Sign Up",
            bg="#E5CCF4",
            padx=10,
            pady=10,
            font=("calibri", 15, "bold"),
            width=10,
        )
        btn_signup.grid(row=len(labels), column=0, padx=10, pady=10)

        btn_exit = tk.Button(
            signup_frame,
            command=self.exit,
            text="Exit",
            bg="#E5CCF4",
            padx=10,
            pady=10,
            font=("calibri", 15, "bold"),
            width=10,
        )
        btn_exit.grid(row=len(labels), column=1, padx=10, pady=10)

    def signup(self):
        # Retrieve data from entry fields
        email = self.entries[0].get()
        password = self.entries[1].get()
        gst_no = self.entries[2].get()
        mobile_number = self.entries[3].get()
        shop_name = self.entries[4].get()
        owner_name = self.entries[5].get()
        branch = self.entries[6].get()
        website_url = self.entries[7].get()
        greetings_message = self.entries[8].get()
        shopId = (
            shop_name.replace(" ", "")[:3]
            + gst_no[:3]
            + owner_name.replace(" ", "")[:3]
            + mobile_number[:3]
        )
        shopId = shopId.upper()

        # Connect to remote database

        # If connection is successful, proceed with inserting data
        if self.success_remote:
            # Define the SQL query to insert data into the table
            insert_query = """
            INSERT INTO ShopList (TimeStamp, ShopId, EmailAddress, Password, GSTNo, MobileNumber, ShopName, OwnerName, Branch, WebsiteURL, GreetingsMessage)
            VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Data to be inserted into the table
            data = (
                self.current_time,
                shopId,
                email,
                password,
                gst_no,
                mobile_number,
                shop_name,
                owner_name,
                branch,
                website_url,
                greetings_message,
            )

            try:
                # Execute the insert query
                self.cursor_remote.execute(insert_query, data)

                # Commit changes to the database
                self.cnx_remote.commit()

                print("Data inserted successfully.")
            except Exception as e:
                # Handle any errors that may occur during insertion
                print("Error:", e)
                self.cnx_remote.rollback()
        else:
            print("Failed to connect to remote database.")

        # Close the database connection
        self.cursor_remote.close()
        self.cnx_remote.close()

    def exit(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BillBookApp(root)
    root.mainloop()
