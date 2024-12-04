from tkinter import Tk
import tkinter as tk
from loginScreen import LoginScreen
from dashboard import Dashboard
from create_table import CreateTableWindow


class WindowManager:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.root.bind("<Escape>", self.exit_application)

        header_frame = tk.Frame(self.root, bg="lightgray")
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        tk.Label(header_frame, text="SOZ-Gastro", font=("Arial", 15),
                 fg="black", bg="lightgray").grid(row=0, column=0, sticky="w", padx=10)

        tk.Button(header_frame, text="Exit", command=self.exit_application,
                  fg="white", bg="red", font=("Arial", 15),
                  width=10).grid(row=0, column=1, sticky="e", padx=10)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def exit_application(self, event=None):
        self.root.destroy()

    def switch_to(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()

        if frame_name == "LoginScreen":
            self.current_frame = LoginScreen(self.root, self)
        elif frame_name == "Dashboard":
            self.current_frame = Dashboard(self.root, self)
        elif frame_name == "CreateTable":
            self.current_frame = CreateTableWindow(self.root)

        self.current_frame.grid(row=1, column=0, sticky="nsew")  


if __name__ == "__main__":
    root = Tk()
    root.geometry('600x400')
    root.title("SOZ-Gastro")
    root.attributes("-fullscreen", True)

    manager = WindowManager(root)
    manager.switch_to("LoginScreen")

    root.mainloop()
