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
        # meals = self.manager.request_handler.get_meals()
        # return meals if meals else []

        MEALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meals.json")
        if os.path.exists(MEALS_FILE):
            with open(MEALS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            messagebox.showerror("Błąd", "Plik meals.json nie istnieje!")
            return []

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        title_text = f"Edycja Zamówienia" if self.order else "Nowe Zamówienie"
        tk.Label(self, text=title_text, font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        comment_frame = tk.Frame(self)
        comment_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        tk.Label(comment_frame, text="Komentarz do zamówienia:", font=("Arial", 14)).pack(anchor="w", padx=5)
        self.comment_text = tk.Text(comment_frame, font=("Arial", 14), height=5, width=80, wrap="word")
        self.comment_text.pack(fill="x", padx=5)

        if self.order and "comment" in self.order:
            self.comment_text.delete("1.0", tk.END)
            self.comment_text.insert("1.0", self.order["comment"])

        def limit_comment(event):
            max_chars = 250
            current_text = self.comment_text.get("1.0", tk.END)
            if len(current_text) > max_chars:
                self.comment_text.delete("1.0", f"1.{max_chars}")
        self.comment_text.bind("<KeyRelease>", limit_comment)

        left_frame = tk.Frame(self)
        left_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(left_frame, text="Dostępne posiłki:", font=("Arial", 14)).pack(pady=5)

        self.meal_table = ttk.Treeview(left_frame, columns=("ID", "Nazwa", "Cena"), show="headings")
        self.meal_table.heading("ID", text="ID")
        self.meal_table.heading("Nazwa", text="Nazwa")
        self.meal_table.heading("Cena", text="Cena")
        self.meal_table.column("ID", width=50, anchor="center")
        self.meal_table.column("Nazwa", width=200, anchor="w")
        self.meal_table.column("Cena", width=100, anchor="center")
        self.meal_table.pack(fill="both", expand=True, padx=5, pady=5)
        self.update_meal_table()

        right_frame = tk.Frame(self)
        right_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(right_frame, text="Posiłki w zamówieniu:", font=("Arial", 14)).pack(pady=5)

        self.order_table = ttk.Treeview(right_frame, columns=("Nazwa", "Cena", "Ilość"), show="headings")
        self.order_table.heading("Nazwa", text="Nazwa")
        self.order_table.heading("Cena", text="Cena")
        self.order_table.heading("Ilość", text="Ilość")
        self.order_table.column("Nazwa", width=200, anchor="w")
        self.order_table.column("Cena", width=100, anchor="center")
        self.order_table.column("Ilość", width=50, anchor="center")
        self.order_table.pack(fill="both", expand=True, padx=5, pady=5)

        self.update_order_table()

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(buttons_frame, text="Zapisz Zamówienie", font=("Arial", 14), bg="green", fg="white",
                command=self.save_order).pack(side="left", padx=10)

        tk.Button(buttons_frame, text="Anuluj", font=("Arial", 14), bg="red", fg="white",
                command=lambda: self.manager.switch_to("TabletopDashboard",
                                                        table_name=self.table_name,
                                                        table_id=self.manager.current_table_id)).pack(side="right", padx=10)
        self.order_table.bind("<ButtonRelease-1>", self.on_order_click)


    def on_order_click(self, event):
        selected_item = self.order_table.focus()
        if selected_item:
            meal_name = self.order_table.item(selected_item, "values")[0]
            self.remove_meal_from_order_by_name(meal_name)


    def update_meal_table(self):
        self.meal_table.delete(*self.meal_table.get_children())
        for meal in self.meals:
            row_id = self.meal_table.insert("", "end", values=(meal["meal_id"], meal["name"], f"{meal['price']} PLN", "+"))
            self.meal_table.item(row_id, tags=row_id)
            self.meal_table.tag_bind(row_id, "<Button-1>", lambda event, meal_id=meal["meal_id"]: self.add_meal_to_order(meal_id))

    def add_meal_to_order(self, meal_id):
        meal = next((m for m in self.meals if m["meal_id"] == meal_id), None)
        if meal:
            for selected in self.selected_meals:
                if selected["meal_id"] == meal_id:
                    selected["quantity"] += 1
                    self.update_order_table()
                    return
            self.selected_meals.append({
                "meal_id": meal["meal_id"],
                "name": meal["name"],
                "price": meal["price"],
                "quantity": 1
            })
            self.update_order_table()

    def remove_meal_from_order_by_name(self, meal_name):
        for selected in self.selected_meals:
            if selected["name"] == meal_name:
                if selected["quantity"] > 1:
                    selected["quantity"] -= 1
                else:
                    self.selected_meals.remove(selected)
                self.update_order_table()
                return


    def update_order_table(self):
        self.order_table.delete(*self.order_table.get_children())
        for meal in self.selected_meals:
            self.order_table.insert("", "end", values=(
                meal["name"], f"{meal['price']} PLN", meal["quantity"]
            ))

    def load_order_meals(self):
        self.selected_meals = []
        if self.order and "meals" in self.order:
            for meal in self.order["meals"]:
                self.selected_meals.append({
                    "meal_id": meal["meal_id"],
                    "name": meal["name"],
                    "price": meal["price"],
                    "quantity": meal.get("quantity", 1)
                })
        if self.order and "comment" in self.order:
            self.comment_text.delete("1.0", tk.END)
            self.comment_text.insert("1.0", self.order["comment"])
        self.update_order_table()



    def save_order(self):
        if not self.selected_meals:
            messagebox.showwarning("Uwaga", "Zamówienie nie może być puste.")
            return

        new_comment = self.comment_text.get("1.0", tk.END).strip()
        comment = self.order["comment"] if self.order and "comment" in self.order and self.order["comment"] == new_comment else new_comment

        # Na pozniej do zapisu zamówienia do backendu
        # order_data = {
        #     "table_id": self.manager.current_table_id,
        #     "status": "Open",
        #     "comment": comment,
        #     "meals": self.selected_meals
        # }
        # if self.order:
        #     self.manager.request_handler.edit_order(self.order["order_id"], order_data)
        # else:
        #     self.manager.request_handler.create_order(order_data)

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
                    o['comment'] = comment
                    break
            messagebox.showinfo("Sukces", "Zamówienie zaktualizowane.")
        else:
            new_order_id = max([o['order_id'] for o in orders], default=0) + 1
            new_order = {
                "order_id": new_order_id,
                "table_id": self.manager.current_table_id,
                "status": "Open",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "comment": comment,
                "meals": self.selected_meals
            }
            orders.append(new_order)
            messagebox.showinfo("Sukces", "Zamówienie utworzone.")

        with open(ORDERS_FILE, "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        self.manager.switch_to("TabletopDashboard",
                            table_id=self.manager.current_table_id,
                            table_name=self.table_name)
