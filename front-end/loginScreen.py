import tkinter as tk
from tkinter import *
#import tkinter.ttk as ttk

VALUE = ""

class MyFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Grid.rowconfigure(master, 0, weight=1)
        tk.Grid.columnconfigure(master, 0, weight=1)
        self.create_widgets()

    

    def create_widgets(self):

        for rows in range(4):
            tk.Grid.rowconfigure(self, rows, weight=1)
        for columns in range(3):
            tk.Grid.columnconfigure(self, columns, weight=1)

        def display_pin():
            global VALUE
            VALUE += "*"
            pin.config(text=f"{VALUE}")

        def clear_pin():
            global VALUE
            VALUE = ""
            pin.config(text=f"{VALUE}")

        tk.Label(root, font=("Arial", 45), fg="black", text="ZALOGUJ",pady=100).grid(row=0, column=0,sticky="n")
        pin = tk.Label(root, font=("Arial", 30), fg="black", text="",pady=100)
        pin.grid(row=1, column=0,sticky="n")

        submit = tk.Button(self,
                text="SUBMIT",
                fg="white",
                bg="green",
                activebackground="white",
                activeforeground="lightgreen",
                font=("Arial", 15),
                cursor="hand2",
                width=10,
                height=5
                )
        clear = tk.Button(self,
                text="CLEAR",
                fg="white",
                bg="red",
                activebackground="white",
                activeforeground="lightgreen",
                font=("Arial", 15),
                cursor="hand2",
                width=10,
                height=5,
                command=clear_pin
                )
        clear.grid(row=4, column=2, sticky="s")
        submit.grid(row=4, column=1, sticky="s")

        row=3
        column=0
        counter=0
        buttons = {}
        for x in range(1,10):
            buttons[f"button_{x}"] = tk.Button(self,
                text=f"{x}",
                fg="white",
                bg="gray",
                activebackground="gray",
                activeforeground="white",
                font=("Arial", 15),
                cursor="hand2",
                width=10,
                height=5,
                command=display_pin
                )
            root.bind(str(x), lambda event: buttons[f"button_{x}"].invoke())
            buttons[f"button_{x}"].grid(row=row, column=column, sticky="nwes")
            if(counter==2):
                column=0
                row -= 1
                counter = 0
            else:
                column += 1
                counter += 1

        self.place(anchor="c", relx=.5, rely=.5)

if (__name__ == "__main__"):

    root = tk.Tk()
    var = tk.IntVar()

    root.geometry('600x400')
    root.title('SOZ-Gastro')
    root.attributes("-fullscreen", True)

    keyboard = MyFrame(root)

    tk.Label(root, font=("Arial", 15), fg="black", text="SOZ-Gastro").place(x=0, y=0)
    exit_button = tk.Button(root,
                            text="Exit", 
                            command=root.destroy,
                            fg="white",
                            bg="red",
                            activebackground="white",
                            activeforeground="white",
                            font=("Arial", 15),
                            cursor="hand2",
                            width=13,
                            height=3,)
    root.bind("<Escape>", lambda event: exit_button.invoke())
    exit_button.place(relx=1, rely=0, anchor='ne')

    root.mainloop()

