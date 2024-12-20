import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from requestHandler import RequestHandler

class AdminPanel(tk.Frame):
    def __init__(self, master, manager, request_handler):
        super().__init__(master)
        self.manager = manager
        self.request_handler = request_handler
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        self.create_navbar()
        self.create_layout()

    def create_navbar(self):
        self.navbar_frame = tk.Frame(self, bg="lightgray")
        self.navbar_frame.grid(row=0, column=0, sticky="ew")
        self.navbar_frame.grid_columnconfigure(0, weight=1)  # Rozciągnięcie na całą szerokość

        style = ttk.Style()
        style.configure("TButton", background="lightgray", foreground="black", font=("Arial", 15), padding=5)
        style.map("TButton", background=[("active", "darkgray")])

        self.main_tab_button = ttk.Button(self.navbar_frame, text="Główna", command=lambda: self.switch_tab("main"))
        self.main_tab_button.grid(row=0, column=0, sticky="w", padx=5)

        self.user_tab_button = ttk.Button(self.navbar_frame, text="Edycja użytkowników", command=lambda: self.switch_tab("user"))
        self.user_tab_button.grid(row=0, column=1, sticky="w", padx=5)

    def create_layout(self):

        self.main_tab = tk.Frame(self)
        self.user_tab = tk.Frame(self)

        self.tabs = {
            "main": self.main_tab,
            "user": self.user_tab
        }

        self.create_main_tab()
        self.create_user_tab()

        self.switch_tab("user")

    def switch_tab(self, tab_name):
        for tab in self.tabs.values():
            tab.grid_forget()
        self.tabs[tab_name].grid(row=1, column=0, sticky="nsew")

    def create_main_tab(self):
        self.user_tab.grid_rowconfigure(0, weight=1)
        self.user_tab.grid_columnconfigure(0, weight=1)
        tk.Label(self.main_tab, text="Panel Admina - Główna", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.main_tab, text="Witaj w panelu administracyjnym!", font=("Arial", 14)).pack(pady=10)

    def create_user_tab(self):
        self.create_user_tab_view(self.user_tab)

    def create_user_tab_view(self, frame):
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)
        frame.grid_columnconfigure(2, weight=1, minsize=300)
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=1)
        
        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        actions = [
            ("Dodaj użytkownika", lambda: self.show_add_user_form(frame)),
            ("Usuń użytkownika", self.delete_user),
        ]

        for idx, (label, command) in enumerate(actions):
            tk.Button(buttons_frame, text=label, font=("Arial", 16), bg="gray", fg="white",
                    width=15, height=2, command=command).pack(pady=10)

        users_frame = tk.Frame(frame)
        users_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(users_frame, text="Lista użytkowników", font=("Arial", 18)).pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=40) 
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

        self.users_listbox = ttk.Treeview(users_frame, columns=("ID", "Nazwa", "Typ", "Aktywny"), show="headings")
        self.users_listbox.heading("ID", text="ID")
        self.users_listbox.heading("Nazwa", text="Nazwa")
        self.users_listbox.heading("Typ", text="Typ")
        self.users_listbox.heading("Aktywny", text="Aktywny")

        self.users_listbox.column("ID", anchor="center", width=10)
        self.users_listbox.column("Nazwa", anchor="w", width=160)
        self.users_listbox.column("Typ", anchor="center", width=100)
        self.users_listbox.column("Aktywny", anchor="center", width=70)
        self.users_listbox.pack(fill="both", expand=True)


        self.load_users()

        self.dynamic_frame = tk.Frame(frame, bg="white", relief="sunken", bd=2, width=300)
        self.dynamic_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        buttons_frame.grid_propagate(False)
        users_frame.grid_propagate(False)  
        
    def load_users(self):
        test_users = [
            {"user_id": 1, "user_name": "kasjer1", "user_type": "Kasjer", "enabled": True},
            {"user_id": 2, "user_name": "magazynier1", "user_type": "Magazynier", "enabled": True},
        ]

        self.users_listbox.delete(*self.users_listbox.get_children())
        for user in test_users:
            self.users_listbox.insert(
                "", "end", values=(user['user_id'], user['user_name'], user['user_type'], "Tak" if user['enabled'] else "Nie")
            )

    def show_add_user_form(self, parent_frame):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        tk.Label(self.dynamic_frame, text="Dodaj użytkownika", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.dynamic_frame, text="Nazwa użytkownika:", font=("Arial", 14)).pack(pady=5)
        username_entry = tk.Entry(self.dynamic_frame, font=("Arial", 14))
        username_entry.pack(pady=5)
    
        tk.Label(self.dynamic_frame, text="PIN (4 cyfry):", font=("Arial", 14)).pack(pady=5)
        pin_entry = tk.Entry(self.dynamic_frame, show="*", font=("Arial", 14))
        pin_entry.pack(pady=5)

        tk.Label(self.dynamic_frame, text="Typ użytkownika:", font=("Arial", 14)).pack(pady=5)
        user_type_combo = ttk.Combobox(self.dynamic_frame, values=["Kasjer", "Magazynier"], font=("Arial", 14))
        user_type_combo.pack(pady=5)

        def submit():
            user_name = username_entry.get().strip()
            login_pin = pin_entry.get().strip()
            user_type = user_type_combo.get()

            if not user_name or not login_pin or not user_type:
                tk.Label(self.dynamic_frame, text="Wszystkie pola są wymagane!", fg="red", font=("Arial", 12)).pack(pady=5)
                return

            if len(login_pin) != 4 or not login_pin.isdigit():
                tk.Label(self.dynamic_frame, text="PIN musi składać się z 4 cyfr!", fg="red", font=("Arial", 12)).pack(pady=5)
                return

            if self.request_handler.check_user_exists(user_name):
                tk.Label(self.dynamic_frame, text="Użytkownik o tej nazwie już istnieje!", fg="red", font=("Arial", 12)).pack(pady=5)
                return

            success = self.request_handler.create_user({
                "user_name": user_name,
                "login_pin": login_pin,
                "user_type": user_type,
            })
            if success:
                self.load_users()
                tk.Label(self.dynamic_frame, text="Użytkownik dodany!", fg="green", font=("Arial", 12)).pack(pady=5)
            else:
                tk.Label(self.dynamic_frame, text="Nie udało się dodać użytkownika.", fg="red", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.dynamic_frame, text="Dodaj", font=("Arial", 14), bg="green", fg="white", command=submit).pack(pady=10)

    def delete_user(self):
        selected_item = self.users_listbox.selection()
        if selected_item:
            user_id = self.users_listbox.item(selected_item, "values")[0]

            for widget in self.dynamic_frame.winfo_children():
                widget.destroy()

            tk.Label(self.dynamic_frame, text=f"Czy na pewno chcesz usunąć użytkownika o ID {user_id}?",
                    font=("Arial", 14)).pack(pady=10)

            def confirm_delete():
                success = self.request_handler.delete_user_by_id(user_id)
                for widget in self.dynamic_frame.winfo_children():
                    widget.destroy()
                if success:
                    self.load_users()
                    tk.Label(self.dynamic_frame, text=f"Użytkownik o ID {user_id} został usunięty.",
                            fg="green", font=("Arial", 12)).pack(pady=5)
                else:
                    tk.Label(self.dynamic_frame, text=f"Nie udało się usunąć użytkownika o ID {user_id}.",
                            fg="red", font=("Arial", 12)).pack(pady=5)

            tk.Button(self.dynamic_frame, text="Tak", font=("Arial", 14), bg="green", fg="white",
                    command=confirm_delete).pack(padx=10, pady=10)
            tk.Button(self.dynamic_frame, text="Nie", font=("Arial", 14), bg="red", fg="white",
                    command=lambda: self.clear_dynamic_frame()).pack(padx=10, pady=10)

        else:
            for widget in self.dynamic_frame.winfo_children():
                widget.destroy()
            tk.Label(self.dynamic_frame, text="Proszę wybrać użytkownika do usunięcia.",
                    fg="red", font=("Arial", 12)).pack(pady=5)

            
    def clear_dynamic_frame(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

    def check_user_exists(self, user_name):
        users = self.get_all_users() # Trzeba dodac pozniej jak funkcje z requestHandlera!!!
        for user in users:
            if user["user_name"] == user_name:
                return True
        return False
