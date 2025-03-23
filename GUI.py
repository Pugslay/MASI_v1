import tkinter as tk
from tkinter import ttk
from Database import *
import Database as DB

class GUI:
    def __init__(self, root):
        self.operation = None
        self.db = DB.Database()
        self.op_var = None
        self.root = root
        self.root.title('MASI Project')
        self.root.geometry('1000x500')
        self.root.resizable(False, False)

        #creating menu_bar
        menu_bar = tk.Menu(self.root)

        #creating bar_file
        bar_file = tk.Menu(menu_bar, tearoff=0)
        bar_file.add_command(label="New", command=self.newf)
        bar_file.add_command(label="Change", command=self.changef)
        bar_file.add_command(label="Save", command=self.savef)
        bar_file.add_command(label='Exit', command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=bar_file)

        self.root.config(menu=menu_bar)

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        #Left field
        left_panel = tk.Frame(main_frame, width=600, relief=tk.SUNKEN, borderwidth=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=True)
        tk.Label(left_panel, text="Operations").pack(anchor="w", pady=2)

        #Middle field
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=False, side=tk.LEFT)

        text_area = tk.Text(text_frame, wrap="word", font=("Arial",12))
        scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)

        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        #Right field
        side_panel = tk.Frame(main_frame, width=200, height=500)
        side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        btn_seq = tk.Button(side_panel, text="Sequencing", command=self.sequencing_button)
        btn_seq.pack(fill=tk.X, pady=2)

        tk.Label(side_panel, text="Font").pack(anchor="w", pady=2)
        font_box = ttk.Combobox(side_panel, values=["Arial", "Courier", "Times New Roman"], state="readonly")
        font_box.current(0)
        font_box.pack(fill=tk.X, pady=2)

        tk.Label(side_panel, text="Size").pack(anchor="w", pady=2)
        size_box = ttk.Combobox(side_panel, values=[10, 12, 14, 16, 18, 20], state="readonly")
        size_box.current(1)
        size_box.pack(fill=tk.X, pady=2)

        btn_redraw = ttk.Button(side_panel, text="Draw", command=self.draw)
        btn_redraw.pack(fill=tk.X, pady=2)

        btn_clear = ttk.Button(side_panel, text="Clear", command=lambda: text_area.delete("1.0", tk.END))
        btn_clear.pack(fill=tk.X, pady=2)

        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(bottom_frame, text="Name").pack(side=tk.LEFT, padx=5)
        entry_name = ttk.Entry(bottom_frame, width=20)
        entry_name.pack(side=tk.LEFT, padx=5)

        ttk.Label(bottom_frame, text="Description").pack(side=tk.LEFT, padx=5)
        entry_desc = ttk.Entry(bottom_frame, width=100)
        entry_desc.pack(side=tk.LEFT, padx=5)




    def savef(self):
        op_var = " "
        db = DB.Database()
        db.add_params("name","desc","zmAa","zmBb",op_var)

    def changef(self):
        print("change")

    def newf(self):
        print("newf")

    def draw(self):
        print("draw")

    def sequencing_button(self):
        self.operation= tk.Toplevel(self.root)
        self.operation.title("Sequencing")
        self.operation.geometry('300x200')

        self.op_var = tk.StringVar()

        ttk.Label(self.operation, text="Term A").pack(side=tk.TOP, padx=5)
        self.term_a = ttk.Entry(self.operation, width=20)
        self.term_a.pack(side=tk.TOP, padx=5)

        ttk.Label(self.operation, text="Term B").pack(side=tk.TOP, padx=5)
        self.term_b = ttk.Entry(self.operation, width=20)
        self.term_b.pack(side=tk.TOP, padx=5)

        tk.Label(self.operation,text="Operacje:").pack(side=tk.TOP, padx=5)

        radio1 = tk.Radiobutton(self.operation, variable=self.op_var, value=";", text=";")
        radio1.pack(side=tk.TOP)
        radio2 = tk.Radiobutton(self.operation, variable=self.op_var, value=",", text=",")
        radio2.pack(side=tk.TOP)

        add_button = tk.Button(self.operation,command=self.sequencing, text="ADD")
        add_button.pack(side=tk.RIGHT)

    def sequencing(self):
        print(self.op_var.get())
        print(self.term_a.get())
        print(self.term_b.get())

        #operacja do wprowadzenia

        self.operation.destroy()


