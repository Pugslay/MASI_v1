import tkinter as tk
import sqlite3

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('MASI Project')
        self.root.geometry('700x600')
        self.root.resizable(False, False)

        self.zm_1=tk.Entry(self.root)
        self.zm_2=tk.Entry(self.root)

        self.add_button = tk.Button(self.root, text='Add')
        self.add_button.pack()

        #creating menu_bar
        menu_bar = tk.Menu(self.root)

        #creating bar_file
        bar_file = tk.Menu(menu_bar, tearoff=0)
        bar_file.add_command(label="New")
        bar_file.add_command(label='Exit', command=self.root.destroy)

        operation

        menu_bar.add_cascade(label="Plik", menu=bar_file)
        menu_bar.add_cascade(label="Pomoc", menu=help_menu)

        self.root.config(menu=menu_bar)

        #self.operation_window = tk.Toplevel(self.root)
        #self.operation_window.pack()
