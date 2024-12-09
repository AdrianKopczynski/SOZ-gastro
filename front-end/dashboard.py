import tkinter as tk
from tkinter import ttk


class Dashboard(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        self.manager = manager
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        tk.Label(self, text="Dashboard", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        actions = [
            ("New Order", self.create_order),
            ("Edit Order", self.edit_order),
            ("Delete Order", self.delete_order),
            ("Close Order", self.close_order),
        ]

        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(len(actions) + 1, weight=1)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)

        for idx, (label, command) in enumerate(actions):
            tk.Button(buttons_frame, text=label, font=("Arial", 16), bg="gray", fg="white",
                      width=15, height=2, command=command).grid(row=idx + 1, column=1, pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=40)
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

        orders_frame = tk.Frame(self)
        orders_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(orders_frame, text="Active Orders (Tables)", font=("Arial", 18)).pack(pady=10)

        self.orders_list = ttk.Treeview(orders_frame, columns=("Table", "Status", "Created At"), show="headings",
                                        height=15)
        self.orders_list.heading("Table", text="Table")
        self.orders_list.heading("Status", text="Status")
        self.orders_list.heading("Created At", text="Created At")
        self.orders_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_orders()

    def load_orders(self):
        orders_data = [
            (1, "Open", "2024-12-01 12:00"),
            (2, "Open", "2024-12-01 12:30"),
            (3, "Closed", "2024-12-01 13:00"),
        ]
        for order in orders_data:
            self.orders_list.insert("", "end", values=order)

    def create_order(self):
        print("Creating a new order...")

    def edit_order(self):
        print("Editing selected order...")

    def delete_order(self):
        print("Deleting selected order...")

    def close_order(self):
        print("Closing selected order...")
