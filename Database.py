import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('MASI.sqlite3')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS operations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Name TEXT NOT NULL, 
                            Description TEXT NOT NULL,
                            term_A TEXT NOT NULL, 
                            term_B TEXT NOT NULL)''')
        self.conn.commit()

    def add_params(self, name, desc, a, b):
        self.c.execute("INSERT INTO operations (Name, Description, term_A, term_B) VALUES (?, ?, ?, ?)",
                       (name, desc, a, b))
        self.conn.commit()



