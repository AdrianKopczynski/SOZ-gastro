import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser
import json
import os
from tabletop import Tabletop

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TABLETOPS_FILE = os.path.join(BASE_DIR, 'tabletops.json')  

class TabletopEditor(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        self.manager = manager
        self.root = master
        self.selected_tabletop = None
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.configure(bg="white")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.canvas = tk.Canvas(self.frame, bg="grey")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.tabletops = []

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=1, sticky="ns", padx=20)

        self.add_button = tk.Button(self.button_frame, text="Add Table", command=self.add_tabletop, width=20, height=3)
        self.add_button.grid(row=0, column=0, pady=20)

        self.toggle_drag_button = tk.Button(self.button_frame, text="Moving OFF", bg="green", command=self.toggle_drag_mode, width=20, height=3)
        self.toggle_drag_button.grid(row=1, column=0, pady=20)

        self.drag_mode_enabled = False
        self.drag_data = {'x': 0, 'y': 0}

        self.load_tabletops()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.show_context_menu)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def add_tabletop(self):
        name = simpledialog.askstring("Tabletop Name", "Name:")
        if name is None or name.strip() == "":
            return

        size = 50
        x = 100
        y = 100
        color = "blue"
        existing_ids = [tabletop.id for tabletop in self.tabletops]
        new_id = max(existing_ids, default=0) + 1
    
        tabletop = Tabletop(self.canvas, x, y, size, color, name, new_id)
        self.tabletops.append(tabletop)

        self.save_tabletops()

    def confirm_remove_tabletop(self):
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete the tabletop '{self.selected_tabletop.name}'?"):
            self.selected_tabletop.delete()
            self.tabletops.remove(self.selected_tabletop)
            self.save_tabletops()

    def toggle_drag_mode(self):
        self.drag_mode_enabled = not self.drag_mode_enabled
        if self.drag_mode_enabled:
            self.toggle_drag_button.config(text="Moving ON ", bg="red")
        else:
            self.toggle_drag_button.config(text="Moving OFF", bg="green")

    def on_click(self, event):
        if not self.drag_mode_enabled:
            for tabletop in self.tabletops:
                x1, y1, x2, y2 = self.canvas.coords(tabletop.id)
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.selected_tabletop = tabletop
                    self.drag_data['x'] = event.x
                    self.drag_data['y'] = event.y
                    self.manager.switch_to("TabletopDashboard", table_name=tabletop.get_name() ,table_id=tabletop.get_id())
                    break
        else:
            for tabletop in self.tabletops:
                x1, y1, x2, y2 = self.canvas.coords(tabletop.id)
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.selected_tabletop = tabletop
                    self.drag_data['x'] = event.x
                    self.drag_data['y'] = event.y
                    break

    def on_drag(self, event):
        if not self.drag_mode_enabled or self.selected_tabletop is None:
            return

        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']

        x1, y1, x2, y2 = self.canvas.coords(self.selected_tabletop.id)

        new_x = x1 + dx
        new_y = y1 + dy
        max_x = self.canvas.winfo_width() - (x2 - x1)
        max_y = self.canvas.winfo_height() - (y2 - y1)

        if new_x < 0:
            new_x = 0
        elif new_x > max_x:
            new_x = max_x

        if new_y < 0:
            new_y = 0
        elif new_y > max_y:
            new_y = max_y

        self.selected_tabletop.move(new_x - x1, new_y - y1)

        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def on_release(self, event):
        if self.selected_tabletop:
            self.save_tabletops()
        self.selected_tabletop = None

    def show_context_menu(self, event):
        for tabletop in self.tabletops:
            x1, y1, x2, y2 = self.canvas.coords(tabletop.id)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selected_tabletop = tabletop
                break
        else:
            return

        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Change Color", command=self.change_color)
        context_menu.add_command(label="Edit Name", command=self.edit_name)
        context_menu.add_command(label="Delete Tabletop", command=self.confirm_remove_tabletop)

        context_menu.post(event.x_root, event.y_root)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.selected_tabletop.change_color(color)
            self.save_tabletops()

    def edit_name(self):
        new_name = simpledialog.askstring("Edit Name", f"Edit the name of the tabletop (current: {self.selected_tabletop.name}):")
        if new_name is not None and new_name.strip() != "":
            self.selected_tabletop.change_name(new_name.strip())
            self.save_tabletops()

    def save_tabletops(self):
        data = []
        for tabletop in self.tabletops:
            x1, y1, x2, y2= self.canvas.coords(tabletop.id)
            data.append({
                "id": tabletop.get_id(),
                "name": tabletop.name,
                "color": tabletop.color,
                "x": x1,
                "y": y1,
                "size": tabletop.size
            })
 
        with open(TABLETOPS_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def load_tabletops(self):
        if os.path.exists(TABLETOPS_FILE):
            with open(TABLETOPS_FILE, "r") as file:
                data = json.load(file)
                for item in data:
                    tabletop = Tabletop(
                    self.canvas,
                    item["x"],
                    item["y"],
                    item["size"],
                    item["color"],
                    item["name"],
                    item["id"]
                )
                    self.tabletops.append(tabletop)

    def get_selected_tabletop_name(self):
        return self.selected_tabletop.get_name()
