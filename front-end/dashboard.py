import tkinter as tk
from loginScreen import LoginScreen


class Dashboard(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        self.manager = manager
        self.create_widgets()

    def create_widgets(self):
        """Tworzenie interfejsu Dashboard."""
        tk.Label(self, text="Dashboard", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Wyloguj", font=("Arial", 16),
                command=lambda: self.manager.switch_to("LoginScreen")).pack(pady=20)
        """
        - Panel do zarządzania zamówieniami.
        - Sekcja szybkich akcji (np. tworzenie nowych zamówień).
        - Podgląd aktualnych zamówień.
        """