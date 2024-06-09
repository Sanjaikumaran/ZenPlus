import time


def long_running_action(loading_label):
    # Simulate a long-running action
    time.sleep(5)
    print("Action completed")
    # Hide loading indicator after action is completed
    loading_label.grid_forget()  # Hide the loading label
