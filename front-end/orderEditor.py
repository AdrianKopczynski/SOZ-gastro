import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class OrderEditor(tk.Frame):
    def __init__(self, master, manager, order=None, table_name=None):
        super().__init__(master)
        self.manager = manager
        self.order = order
        self.table_name = table_name
        self.selected_meals = []

        self.meals = self.load_meals()
        self.create_widgets()

        if self.order:
            self.load_order_meals()

    def load_meals(self):
        MEALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meals.json")
        if os.path.exists(MEALS_FILE):
            with open(MEALS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            messagebox.showerror("Błąd", "Plik meals.json nie istnieje!")
            return []

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        title_text = f"Edycja Zamówienia" if self.order else "Nowe Zamówienie"
        tk.Label(self, text=title_text, font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        left_frame = tk.Frame(self)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(left_frame, text="Wyszukaj posiłek:", font=("Arial", 14)).pack(pady=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_meal_list)
        search_entry = tk.Entry(left_frame, textvariable=self.search_var, font=("Arial", 14))
        search_entry.pack(fill="x", padx=5)

        self.meal_listbox = tk.Listbox(left_frame, font=("Arial", 14))
        self.meal_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.meal_listbox.bind('<Double-Button-1>', self.add_selected_meal)

        self.update_meal_list()

        right_frame = tk.Frame(self)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(right_frame, text="Posiłki w zamówieniu:", font=("Arial", 14)).pack(pady=5)

        self.order_meals_listbox = tk.Listbox(right_frame, font=("Arial", 14))
        self.order_meals_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.order_meals_listbox.bind('<Double-Button-1>', self.remove_selected_meal)

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(buttons_frame, text="Zapisz Zamówienie", font=("Arial", 14), bg="green", fg="white",
                  command=self.save_order).pack(side="left", padx=10)

        (tk.Button(buttons_frame, text="Anuluj", font=("Arial", 14), bg="red", fg="white",
                   command=lambda: self.manager.switch_to("TabletopDashboard",
                                                          table_name=self.table_name,
                                                          table_id=self.manager.current_table_id)).pack(side="right",
                                                                                                        padx=10))

    def update_meal_list(self, *args):
        search_term = self.search_var.get().lower()
        search_term = self.search_var.get().lower()
        self.meal_listbox.delete(0, tk.END)
        for meal in self.meals:
            if search_term in meal['name'].lower():
                self.meal_listbox.insert(tk.END, f"{meal['meal_id']}: {meal['name']} - {meal['price']} PLN")

    def add_selected_meal(self, event=None):
        selection = self.meal_listbox.curselection()
        if selection:
            index = selection[0]
            meal_text = self.meal_listbox.get(index)
            meal_id = int(meal_text.split(":")[0])
            meal = next((m for m in self.meals if m['meal_id'] == meal_id), None)
            if meal:
                self.selected_meals.append(meal)
                self.update_order_meals_listbox()

    def remove_selected_meal(self, event=None):
        selection = self.order_meals_listbox.curselection()
        if selection:
            index = selection[0]
            del self.selected_meals[index]
            self.update_order_meals_listbox()

    def update_order_meals_listbox(self):
        self.order_meals_listbox.delete(0, tk.END)
        for meal in self.selected_meals:
            self.order_meals_listbox.insert(tk.END, f"{meal['name']} - {meal['price']} PLN")

    def load_order_meals(self):
        self.selected_meals = self.order.get('meals', [])
        self.update_order_meals_listbox()

    def save_order(self):
        if not self.selected_meals:
            messagebox.showwarning("Uwaga", "Zamówienie nie może być puste.")
            return

        ORDERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.json")
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, "r", encoding="utf-8") as file:
                orders = json.load(file)
        else:
            orders = []

        if self.order:
            for o in orders:
                if o['order_id'] == self.order['order_id']:
                    o['meals'] = self.selected_meals
                    break
            messagebox.showinfo("Sukces", "Zamówienie zaktualizowane.")
        else:
            new_order_id = max([o['order_id'] for o in orders], default=0) + 1
            new_order = {
                "order_id": new_order_id,
                "table_id": self.manager.current_table_id,
                "status": "Open",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "comment": "",
                "meals": self.selected_meals
            }
            orders.append(new_order)
            messagebox.showinfo("Sukces", "Zamówienie utworzone.")

        with open(ORDERS_FILE, "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        self.manager.switch_to("TabletopDashboard",
                               table_id=self.manager.current_table_id,
                               table_name=self.table_name
                               )
