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
                            term_B TEXT NOT NULL,
                            OP TEXT NOT NULL)''')
        self.conn.commit()

    def add_params(self, name, desc, a, b, op):
        self.c.execute("INSERT INTO operations (Name, Description, term_A, term_B, OP) VALUES (?, ?, ?, ?, ?)",
                       (name, desc, a, b, op))
        self.conn.commit()

    def del_params(self, name):
        self.c.execute("DELETE FROM operations WHERE Name=?", (name,))

    def get_params(self):
        self.c.execute("SELECT * FROM operations")
        return self.c.fetchall()



