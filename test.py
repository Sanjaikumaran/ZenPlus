import tkinter as tk


class Application:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # Creating the first frame (bottom frame)
        bottom_frame = tk.Frame(self.root, width=200, height=200, bg="blue")
        bottom_frame.place(x=50, y=50)

        # Creating the second frame (top frame)
        top_frame = tk.Frame(self.root, width=150, height=150, bg="red")
        top_frame.place(x=50, y=50)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
