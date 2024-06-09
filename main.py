import tkinter as tk
import threading
import time
import action_file


def perform_action(root):

    root.title("Loading Indicator Example")

    loading_label = tk.Label(root, text="Loading...", fg="blue")

    loading_label.grid(row=1, column=0)  # Show loading indicator
    threading.Thread(
        target=action_file.long_running_action, args=(loading_label,)
    ).start()
