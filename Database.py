import sqlite3

class GUI:
    def __init__(self):
        self.conn = sqlite3.connect('MASI.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
        self.conn.commit()