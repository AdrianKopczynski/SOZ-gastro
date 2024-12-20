from tkinter import Tk
import tkinter as tk
from loginScreen import LoginScreen
from tabletopDashboard import TabletopDashboard
from tabletopEditor import TabletopEditor
from orderEditor import OrderEditor
from adminPanel import AdminPanel
from requestHandler import RequestHandler 


class WindowManager:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.username = ""
        self.current_table_id = None
        self.request_handler = RequestHandler(base_url="http://localhost:10000")
        self.root.bind("<Escape>", self.exit_application)

        self.header_frame = tk.Frame(self.root, bg="lightgray")
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=0)

        tk.Label(self.header_frame, text="SOZ-Gastro", font=("Arial", 15),
                 fg="black", bg="lightgray").grid(row=0, column=0, sticky="w", padx=10)

        self.greeting_label = tk.Label(self.header_frame, text="", font=("Arial", 15), fg="black", bg="lightgray")
        self.greeting_label.grid(row=0, column=1, sticky="e", padx=10)

        self.admin_button = tk.Button(self.header_frame, text="Panel Admina", command=lambda: self.switch_to("AdminPanel"),
                                      fg="white", bg="blue", font=("Arial", 15), width=15)
        self.admin_button.grid(row=0, column=1, sticky="e", padx=10)
        self.admin_button.grid_remove()

        self.logout_button = tk.Button(self.header_frame, text="Wyloguj", command=lambda: self.switch_to("LoginScreen"),
                                       fg="white", bg="red", font=("Arial", 15), width=10)
        self.logout_button.grid(row=0, column=2, sticky="e", padx=10)

        self.exit_button = tk.Button(self.header_frame, text="Exit", command=self.exit_application,
                                      fg="white", bg="red", font=("Arial", 15), width=10)
        self.exit_button.grid(row=0, column=3, sticky="e", padx=10)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.root.grid_rowconfigure(2, weight=10, minsize=500)
        self.root.grid_columnconfigure(0, weight=1)

    def set_username(self, username):
        self.username = username
        self.update_greeting()

        # if username == "admin":  # TODO: zastąpić sprawdzanie na podstawie bazy danych
        self.admin_button.grid()
        # else:
        # self.admin_button.grid_remove()

    def update_admin_button(self, in_admin_panel):
        if in_admin_panel:
            self.admin_button.config(text="Powrót", command=lambda: self.switch_to("TabletopEditor"))
        else:
            self.admin_button.config(text="Panel Admina", command=lambda: self.switch_to("AdminPanel"))


    def update_greeting(self):
        if self.username and self.current_frame != "LoginScreen":
            self.greeting_label.config(text=f"Witaj, {self.username}!")
        else:
            self.greeting_label.config(text="")

    def exit_application(self, event=None):
        self.root.destroy()

    def switch_to(self, frame_name, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()
            self.update_admin_button(False)


        if frame_name == "LoginScreen":
            self.current_frame = LoginScreen(self.root, self)
            self.logout_button.grid_remove()
            self.exit_button.grid()
            self.username = ""
            self.admin_button.grid_remove()

        elif frame_name == "TabletopDashboard":
            table_name = kwargs.get("table_name",)
            table_id = kwargs.get("table_id", self.current_table_id)
            self.current_frame = TabletopDashboard(self.root, self, table_name=table_name, table_id=table_id)
            self.logout_button.grid()
            self.exit_button.grid_remove()

        elif frame_name == "TabletopEditor":
            self.current_frame = TabletopEditor(self.root, self)
            self.logout_button.grid()
            self.exit_button.grid_remove()

        elif frame_name == "OrderEditor":
            order = kwargs.get("order", None)
            table_name = kwargs.get("table_name")
            self.current_frame = OrderEditor(self.root, self, order=order, table_name=table_name)
            self.logout_button.grid()
            self.exit_button.grid_remove()

        elif frame_name == "AdminPanel":
            self.current_frame = AdminPanel(self.root, self, self.request_handler)
            self.logout_button.grid()
            self.exit_button.grid_remove()
            self.update_admin_button(True)

        
        self.update_greeting()
        self.current_frame.grid(row=2, column=0, sticky="nsew")



if __name__ == "__main__":
    root = Tk()
    root.geometry('600x400')
    root.title("SOZ-Gastro")
    root.attributes("-fullscreen", True)

    manager = WindowManager(root)
    manager.switch_to("LoginScreen")

    root.mainloop()
