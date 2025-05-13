import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont


# Klasa zarządzająca bazą danych
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('MASI.sqlite3')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS operations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Name TEXT NOT NULL, 
                            Description TEXT NOT NULL,
                            term_A TEXT NOT NULL, 
                            term_B TEXT NOT NULL,
                            term_P_A TEXT NOT NULL, 
                            term_P_B TEXT NOT NULL,
                            OP_P TEXT NOT NULL,
                            OP TEXT NOT NULL)''')
        self.conn.commit()

    def add_params(self, name, desc, a, b, ap, bp, op, op_p):
        self.c.execute(
            '''INSERT INTO operations 
               (Name, Description, term_A, term_B, term_P_A, term_P_B, OP_P, OP) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, desc, a, b, ap, bp, op_p, op)
        )
        self.conn.commit()

    def del_params(self, name):
        self.c.execute("DELETE FROM operations WHERE Name=?", (name,))
        self.conn.commit()

    def get_params(self):
        self.c.execute("SELECT * FROM operations")
        return self.c.fetchall()

    def get_names(self):
        self.c.execute("SELECT Name, Description FROM operations")
        return self.c.fetchall()

    def get_data(self, name, desc):
        self.c.execute("SELECT term_A, term_B, term_P_A, term_P_B, OP_P, OP FROM operations WHERE name IS ? AND Description IS ?", (name,desc))
        return self.c.fetchall()


# Klasa odpowiedzialna za GUI
class GUI:
    def __init__(self, root):
        self.op_var_p = None
        self.term_a = None
        self.term_b = None
        self.operation = None
        self.db = Database()
        self.op_var = None
        self.root = root
        self.root.title('MASI Project')
        self.root.geometry('1000x500')
        self.root.resizable(False, False)
        self.term_a_var = tk.StringVar()
        self.term_b_var = tk.StringVar()
        self.term_b_var_p = tk.StringVar()
        self.term_a_var_p = tk.StringVar()
        self.name_entry = tk.StringVar()
        self.desc_entry = tk.StringVar()

        # Tworzenie menu
        menu_bar = tk.Menu(self.root)
        bar_file = tk.Menu(menu_bar, tearoff=0)
        bar_file.add_command(label="Change", command=self.changef)
        bar_file.add_command(label='Exit', command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=bar_file)
        self.root.config(menu=menu_bar)

        # Główne okno
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Pole tekstowe
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.canvas = tk.Canvas(text_frame, height=100, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Panel boczny
        side_panel = tk.Frame(main_frame)
        side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        btn_seq = tk.Button(side_panel, text="Sequencing", command=self.sequencing_button)
        btn_seq.pack(pady=5, fill=tk.X)

        btn_parell = tk.Button(side_panel, text="Parallelism", command=self.parallel_button)
        btn_parell.pack(pady=5, fill=tk.X)

        # Label i entry dla Name
        name_label = tk.Label(side_panel, text="Name:")
        name_label.pack(anchor='w', pady=(10, 0))
        self.name_entry = tk.Entry(side_panel)
        self.name_entry.pack(pady=5, fill=tk.X)

        # Label i entry dla Description
        desc_label = tk.Label(side_panel, text="Description:")
        desc_label.pack(anchor='w', pady=(10, 0))
        self.desc_text = tk.Entry(side_panel)
        self.desc_text.pack(pady=5, fill=tk.X)

        btn_clear = tk.Button(side_panel, text="Save", command=self.savef)
        btn_clear.pack(pady=5, fill=tk.X)

        btn_clear = tk.Button(side_panel, text="Clear", command=self.clear_canvas)
        btn_clear.pack(pady=5, fill=tk.X)

        btn_clear = tk.Button(side_panel, text="Load", command=self.loadf)
        btn_clear.pack(pady=5, fill=tk.X)

    # Funkcja zapisująca dane
    def savef(self):
        term_a = self.term_a_var.get().strip()
        term_b = self.term_b_var.get().strip()
        term_ap = self.term_a_var_p.get().strip()
        term_bp = self.term_b_var_p.get().strip()
        operator = self.op_var.get() if self.op_var else ""
        operator_p = self.op_var_p.get() if self.op_var_p else ""

        name = self.name_entry.get().strip()
        description = self.desc_text.get().strip()

        # Walidacja danych
        if not name or not description or not term_a or not term_b or not operator:
            messagebox.showwarning("Missing Data", "Insert terms before saving.")
            return

        self.db.add_params(self.name_entry.get(), self.desc_text.get().strip(), term_a, term_b, term_ap, term_bp,
                           operator, operator_p)

    def loadf(self):
        #print("load")
        names = self.db.get_names()
        #print(names)
        self.load = tk.Toplevel(self.root)
        self.load.title("Change")
        self.load.geometry('300x500')
        self.load.resizable(False, False)

        label = ttk.Label(self.load, text="Load data:", font=("Arial", 12, "bold"))
        label.pack(pady=(15, 10))

        listbox = tk.Listbox(self.load, height=6)
        for name in names:
            listbox.insert(tk.END, str(name))
        listbox.pack()

        def on_select(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                name = names[index]
                data = self.db.get_data(name[0],name[1])
                #print(data)
                self.load.destroy()
                self.draw_alt(data)

        listbox.bind("<<ListboxSelect>>", on_select)

    # Funkcja czyszcząca pole rysunkowe
    def clear_canvas(self):
        self.canvas.delete("all")
        self.term_a_var_p = tk.StringVar()
        self.term_b_var_p = tk.StringVar()
        self.term_a_var = tk.StringVar()
        self.term_b_var = tk.StringVar()

    # Funkcja zmiany (związana z operacjami na termach)
    def changef(self):
        term_a = self.term_a_var.get().strip()
        term_b = self.term_b_var.get().strip()

        if not term_a or not term_b:
            messagebox.showwarning("Missing Data", "Insert terms before clicking 'Change'.")
            return

        self.change = tk.Toplevel(self.root)
        self.change.title("Change")
        self.change.geometry('300x150')
        self.change.resizable(False, False)

        label = ttk.Label(self.change, text="Swap in Term 1 or Term 2", font=("Arial", 12, "bold"))
        label.pack(pady=(15, 10))

        button_frame = tk.Frame(self.change)
        button_frame.pack(pady=10)

        button1 = tk.Button(button_frame, command=self.term1, text="Term 1", width=10)
        button1.pack(side=tk.LEFT, padx=10)

        button2 = tk.Button(button_frame, command=self.term2, text="Term 2", width=10)
        button2.pack(side=tk.LEFT, padx=10)

    # Funkcja rysująca operację równoległą
    def draw(self, term_a, term_b, operator, operator_p, bul):
        self.canvas.delete("all")
        term_a_p = self.term_a_var_p.get()
        term_b_p = self.term_b_var_p.get()
        result = f"  {term_a}  {operator}  {term_b}"

        #print(result)
        font = tkFont.Font(font=("Arial", 12))


        margin = 20
        x1 = 80
        y1 = 20
        y2 = 80

        if bul:
            #print(bul)
            result = f"  {term_a} {operator} {term_b}"
            text_width = font.measure(result)
            x2 = x1 + text_width + margin

            self.canvas.create_arc(x1, y1, x2, y2, start=0, extent=180, style=tk.ARC, width=2, outline="light blue")
            text_x = (x1 + x2) / 2
            self.canvas.create_text(text_x, y2 - 35, text=result, font=("Arial", 12))

            self.canvas.create_text(x1+22, y2 - 15, text=operator_p, anchor="w", font=("Arial", 12))
            self.canvas.create_text(x1+22, y2 + 10, text=term_b_p, anchor="w", font=("Arial", 12))

            self.canvas.create_line(x1 + 15, y1+16, x1 + 15, y2+22, width=2)
            self.canvas.create_line(x1 + 15, y1+16, x1 + 30, y1+16, width=2)
            self.canvas.create_line(x1 + 15, y2+21, x1 + 30, y2+21, width=2)

        else:
            #print(bul)
            result = f"{term_a} {operator}  {term_b}"
            text_width = font.measure(result)
            text_fragment = f"  {term_a} {operator}"
            text_frag_width = font.measure(text_fragment)
            x2 = x1 + text_width + margin

            self.canvas.create_arc(x1, y1, x2, y2, start=0, extent=180, style=tk.ARC, width=2, outline="light blue")
            text_x = (x1 + x2) / 2
            self.canvas.create_text(text_x, y2 - 35, text=result, font=("Arial", 12))

            self.canvas.create_text(x1+text_frag_width+12, y2 - 15, text=operator_p, anchor="w", font=("Arial", 12))
            self.canvas.create_text(x1+text_frag_width+12, y2 + 10, text=term_b_p, anchor="w", font=("Arial", 12))

            self.canvas.create_line(x1+text_frag_width+8, y1+15, x1+text_frag_width+8, y2+22, width=2)
            self.canvas.create_line(x1+text_frag_width+8, y1+16, x1+text_frag_width+16, y1+16, width=2)
            self.canvas.create_line(x1+text_frag_width+8, y2+21, x1+text_frag_width+16, y2+21, width=2)

        x1 = 50
        y1 = 170
        y2 = 250

        self.canvas.create_text(x1 + 10, y1 + 15, text=term_a_p, anchor="w", font=("Arial", 12))
        self.canvas.create_text(x1 + 10, y1 + 40, text=operator_p, anchor="w", font=("Arial", 12))
        self.canvas.create_text(x1 + 10, y1 + 65, text=term_b_p, anchor="w", font=("Arial", 12))

        self.canvas.create_line(x1-10, y1, x1-10, y2, width=2)
        self.canvas.create_line(x1 - 10, y1, x1 + 10, y1, width=2)
        self.canvas.create_line(x1 - 10, y2, x1 + 10, y2, width=2)

    # Funkcje dla Term 1 i Term 2
    def term1(self):
        term_a_p = self.term_a_var_p.get()
        term_b_p = self.term_b_var_p.get()
        term_b = self.term_b_var.get()
        operator = self.op_var.get()
        operator_p = self.op_var_p.get()
        term_a = self.term_a_var.get()

        self.draw(term_a_p, term_b, operator, operator_p, True)
        self.change.destroy()

    def term2(self):
        term_a_p = self.term_a_var_p.get()
        term_b_p = self.term_b_var_p.get()
        term_b = self.term_b_var.get()
        operator = self.op_var.get()
        operator_p = self.op_var_p.get()
        term_a = self.term_a_var.get()

        self.draw(term_a, term_a_p, operator, operator_p, False)
        self.change.destroy()

    # Funkcja dla operacji równoległej
    def parallel_button(self):
        self.operation = tk.Toplevel(self.root)
        self.operation.title("Parallelism")
        self.operation.geometry('150x200')

        self.op_var_p = tk.StringVar(value=";")

        ttk.Label(self.operation, text="Term A").pack(side=tk.TOP, padx=5)
        self.term_a = ttk.Entry(self.operation, width=20, textvariable=self.term_a_var_p)
        self.term_a.pack(side=tk.TOP, padx=5)

        ttk.Label(self.operation, text="Term B").pack(side=tk.TOP, padx=5)
        self.term_b = ttk.Entry(self.operation, width=20, textvariable=self.term_b_var_p)
        self.term_b.pack(side=tk.TOP, padx=5)

        tk.Label(self.operation, text="Operacje:").pack(side=tk.TOP, padx=5)

        radio1 = tk.Radiobutton(self.operation, variable=self.op_var_p, value=";", text=";")
        radio1.pack(side=tk.TOP)
        radio2 = tk.Radiobutton(self.operation, variable=self.op_var_p, value=",", text=",")
        radio2.pack(side=tk.TOP, pady=5)

        add_button = tk.Button(self.operation, command=self.parallel, text="ADD")
        add_button.pack(side=tk.TOP)

    # Funkcja dla operacji sekwencyjnej
    def sequencing_button(self):
        self.operation = tk.Toplevel(self.root)
        self.operation.title("Sequencing")
        self.operation.geometry('150x200')

        self.op_var = tk.StringVar(value=";")

        ttk.Label(self.operation, text="Term A").pack(side=tk.TOP, padx=5)
        self.term_a = ttk.Entry(self.operation, width=20, textvariable=self.term_a_var)
        self.term_a.pack(side=tk.TOP, padx=5)

        ttk.Label(self.operation, text="Term B").pack(side=tk.TOP, padx=5)
        self.term_b = ttk.Entry(self.operation, width=20, textvariable=self.term_b_var)
        self.term_b.pack(side=tk.TOP, padx=5)

        tk.Label(self.operation, text="Operacje:").pack(side=tk.TOP, padx=5)

        radio1 = tk.Radiobutton(self.operation, variable=self.op_var, value=";", text=";")
        radio1.pack(side=tk.TOP)
        radio2 = tk.Radiobutton(self.operation, variable=self.op_var, value=",", text=",")
        radio2.pack(side=tk.TOP, pady=5)

        add_button = tk.Button(self.operation, command=self.sequencing, text="ADD")
        add_button.pack(side=tk.TOP)

    def parallel(self):
        self.canvas.delete("par")
        term_a_p = self.term_a_var_p.get()
        term_b_p = self.term_b_var_p.get()
        operator = self.op_var_p.get()

        x1 = 50
        y1 = 170
        y2 = 250

        self.canvas.create_text(x1 + 10, y1 + 15, text=term_a_p, anchor="w", font=("Arial", 12), tags='par')
        self.canvas.create_text(x1 + 10, y1 + 40, text=operator, anchor="w", font=("Arial", 12), tags='par')
        self.canvas.create_text(x1 + 10, y1 + 65, text=term_b_p, anchor="w", font=("Arial", 12), tags='par')

        self.canvas.create_line(x1-10, y1, x1-10, y2, width=2)
        self.canvas.create_line(x1 - 10, y1, x1 + 10, y1, width=2)
        self.canvas.create_line(x1 - 10, y2, x1 + 10, y2, width=2)

        if self.operation is not None:
            self.operation.destroy()
            self.operation = None

    def sequencing(self):
        self.canvas.delete("seq")
        term_a = self.term_a_var.get()
        term_b = self.term_b_var.get()
        operator = self.op_var.get()

        result = f"{term_a} {operator} {term_b}"

        font = tkFont.Font(font=("Arial", 12))
        text_width = font.measure(result)

        margin = 20
        x1 = 80
        x2 = x1 + text_width + margin
        y1 = 20
        y2 = 80

        self.canvas.create_arc(x1, y1, x2, y2, start=0, extent=180, style=tk.ARC, width=2, outline="light blue",
                               tags='seq')
        text_x = (x1 + x2) / 2
        self.canvas.create_text(text_x, y2 - 35, text=result, font=("Arial", 12), tags='seq')

        if self.operation is not None:
            self.operation.destroy()

    def draw_alt(self, data):
        self.term_a_var=tk.StringVar(self.root, value = data[0][0])
        self.term_b_var=tk.StringVar(self.root, value = data[0][1])
        self.term_a_var_p=tk.StringVar(self.root, value = data[0][2])
        self.term_b_var_p=tk.StringVar(self.root, value = data[0][3])
        self.op_var_p=tk.StringVar(self.root, value = data[0][4])
        self.op_var=tk.StringVar(self.root, value = data[0][5])

        self.sequencing()
        self.parallel()

        #print("data")
        #print(type(data))






