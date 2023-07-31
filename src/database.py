import sqlite3 as sql3
import os


class db:
    def __init__(self):
        self.setup_complete=False
        self.setup_tables()
        
    def execute_query (self, inp_conn, inp_cursor, query: str, params):
        if params:
            out = inp_cursor.execute(query, params)
        else:
            out = inp_cursor.execute(query)
        inp_conn.commit()
        return out
    
    def single_query (self, query: str, params):
        conn = sql3.connect("database.db") #connect/create db file
        cursor = conn.cursor() # used to execute SQL queries
        res = self.execute_query(conn, cursor, query, params)
        conn.commit()
        conn.close()
        print ("res:",res)
        return res
    
 
    def setup_tables (self) -> None:
        query1 = """
            CREATE TABLE IF NOT EXISTS Resume(
                content TEXT,
                language TEXT PRIMARY KEY
            )
        """
        query2 = """
            CREATE TABLE IF NOT EXISTS Skills(
                skill TEXT PRIMARY KEY
            )
        """
        self.single_query(query1, None)
        self.single_query(query2, None)
        return None


    def add_resume(self, res: tuple) -> None:
        query = "INSERT INTO Resume (content, language) VALUES (?, ?)"
        self.single_query(query, res)
        return None

    def remove_resume(self, language: tuple):
        return None

    def add_skill(self, skill: tuple) -> None:
        query = "INSERT INTO Skills (skill) VALUES (?)"
        try:
            self.single_query(query, (skill[0],))
        except sql3.IntegrityError as e:
            print(f"Error: {e}")
            # Here, you can display an error message to the user or take other actions
        return None 
    
    def remove_skill(self, skill: tuple) -> None:
        print("remove", skill)
        query = "DELETE FROM Skills WHERE skill = ?"
        try:
            self.single_query(query, (skill[0],))
        except sql3.IntegrityError as e:
            print(f"Error: {e}")
            # Here, you can display an error message to the user or take other actions
        return None
        
    def skill_list(self) -> list[str]:
        query = "SELECT skill FROM Skills"
        conn = sql3.connect("database.db")  # Create the connection
        cursor = conn.cursor()  # Create the cursor

        cursor.execute(query)  # Execute the query
        skills = cursor.fetchall()  # Fetch the data from the cursor
        skill_list = [skill[0] for skill in skills]  # Extract the skills from the fetched rows

        cursor.close()  # Close the cursor
        conn.close()  # Close the connection
        return skill_list

    def delete_database(self):
        if os.path.exists("database.db"):
            os.remove("database.db")
        return None
    

