import tkinter as tk
from tkinter import messagebox
import json
import os

class LoginScreen(tk.Frame):
    def __init__(self, master, manager):
        tk.Frame.__init__(self, master)
        self.manager = manager
        self.value = ""
        self.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.create_widgets()

    def create_widgets(self):
        for i in range(3):  
            self.grid_rowconfigure(i, weight=1)
        for j in range(3):  
            self.grid_columnconfigure(j, weight=1)

        center_frame = tk.Frame(self, relief="solid")
        center_frame.grid(row=1, column=1, sticky="nsew", padx=50, pady=50)

        for i in range(6):
            center_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            center_frame.grid_columnconfigure(j, weight=1)

        tk.Label(center_frame, text="ZALOGUJ", font=("Arial", 45), fg="black").grid(row=0, column=0, columnspan=3, pady=20)

        def display_pin(number):
            self.value += str(number)
            self.pin_label.config(text="*" * len(self.value))

        def clear_pin():
            self.value = ""
            self.pin_label.config(text="")

        row, column = 1, 0
        for x in range(1, 10):
            tk.Button(center_frame, text=f"{x}", fg="white", bg="gray", activebackground="gray",
                    activeforeground="white", font=("Arial", 15), width=10, height=4,
                    command=lambda x=x: display_pin(x)).grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
            column += 1
            if column == 3:
                column = 0
                row += 1

        self.pin_label = tk.Label(center_frame, font=("Arial", 30), fg="black", text="", bg="lightgray", relief="solid")
        self.pin_label.grid(row=4, column=0, columnspan=3, pady=20, sticky="ew")

        def submit_pin():
            username = self.check_pin(self.value)
            if username:
                self.manager.set_username(username)
                self.manager.switch_to("TabletopEditor")
            else:
                self.value = ""
                self.pin_label.config(text="Błędny PIN")

        tk.Button(center_frame, 
                  text="SUBMIT", 
                  fg="white", bg="green", 
                  font=("Arial", 15), 
                  width=10, height=2,
                  activebackground="white", activeforeground="lightgreen",
                  command=submit_pin).grid(row=5, column=1, pady=10)
        tk.Button(center_frame, 
                  text="CLEAR", 
                  fg="white", bg="red", 
                  font=("Arial", 15), 
                  width=10, height=2,
                  activebackground="white", activeforeground="lightgreen",
                  command=clear_pin).grid(row=5, column=2, pady=10)

    def check_pin(self, pin):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, 'users.json')
            
            with open(file_path, 'r', encoding='utf-8') as f:
                users = json.load(f)
            for username, stored_pin in users.items():
                if stored_pin == pin:
                    return username
            return None
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Plik z użytkownikami nie istnieje!")
            return None
        except json.JSONDecodeError:
            messagebox.showerror("Błąd", "Niepoprawny format pliku użytkowników!")
            return None
