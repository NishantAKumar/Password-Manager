from sqlite3 import *

class Database:
    def __init__(self, db) -> None:
        self.connection = connect(db)
        self.cur = self.connection.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS sensitive(id INTEGER PRIMARY KEY, password TEXT, username TEXT, location TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS admin(id INTEGER PRIMARY KEY, username TEXT, password TEXT, logged_in BOOLEAN)")
        self.connection.commit()

    def read_sensitive_data(self):
        self.cur.execute("SELECT * FROM sensitive")
        rows = self.cur.fetchall()
        return rows

    def read_admin_data(self):
        self.cur.execute("SELECT * FROM admin")
        rows = self.cur.fetchall()
        return rows

    def insert_sensitive_data(self, password, username, location):
        self.cur.execute("INSERT INTO sensitive VALUES (NULL, ?, ?, ?)", (password, username, location))
        self.connection.commit()

    def insert_admin_data(self, username, password):
        self.cur.execute("INSERT INTO admin VALUES (NULL, ?, ?, 0)", (username, password))
        self.connection.commit()

    def remove_sensitive_data(self, id):
        self.cur.execute("DELETE FROM sensitive where id=?", (id,))
        self.connection.commit()

    def update_sensitive_data(self, id, password, username, location):
        self.cur.execute("UPDATE sensitive_data SET password=?, username=?, location=? where id=?", (password, username, location, id))
        self.connection.commit()
    
    def update_admin_data(self, id, password, username):
        self.cur.execute("UPDATE sensitive_data SET password=?, username=?, location=? where id=?", (password, username, id))
        self.connection.commit()

    def admin_logged_in_setter(self, id, value):
        self.cur.execute("UPDATE admin SET logged_in=? where id=?", (value, id))
        self.connection.commit()

    def delete_all_sensitive_data(self):
        self.cur.execute("DELETE FROM sensitive")
        self.cur.execute("DELETE FROM admin")
        self.connection.commit()

    def __del__(self):
        self.connection.close()