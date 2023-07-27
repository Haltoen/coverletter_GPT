import sqlite3 as sql3

class db:
    def __init__(self):
        self.conn=None
        self.cursor=None
        self.init_db()
        
    def init_db (self) -> None:
        self.conn = sql3.connect("database.db") #connect/create db file
        self.cursor = self.conn.cursor() # used to execute SQL queries
        return None

    def execute_query (self, query: str)-> None:
        self.cursor.execute(query)
        self.conn.commit
        return None