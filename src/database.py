import sqlite3 as sql3
import os


class db:
    def __init__(self):
        self.setup_complete=False
        self.setup_tables()
        self.csv_h = CSVHandler()
        self.userdata = self.get_userdata()
    
    def get_userdata(self):
        data = self.csv_h.read_dicts_from_csv("userdata.csv")
        return data

    def add_userdata(self, data: tuple):
        userdata = {"full name": data[0], "age": data[1], "country": data[2], "address": data[3]}
        self.csv_h.write_dicts_to_csv("userdata.csv",[userdata])
        
        

    def execute_query (self, inp_conn, inp_cursor, query: str, params):
        try:
            print("Executing query:", query)
            print("Query parameters:", params)
            if params:
                out = inp_cursor.execute(query, params)
            else:
                out = inp_cursor.execute(query)
            inp_conn.commit()
            return out
        except sql3.IntegrityError as e:
            print(f"Error: {e}")

    def single_query(self, query: str, params=None):
        conn = sql3.connect("database.db")  # connect/create db file
        cursor = conn.cursor()  # used to execute SQL queries
        res = self.execute_query(conn, cursor, query, params)
        conn.commit()
        result = res.fetchall()  # Fetch all the data from the cursor
        conn.close()
        return result
    
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
        query = "DELETE FROM Resume WHERE language = ?"
        self.single_query(query, language)
        return None
    
    def get_resume(self, language: tuple):
        query = "SELECT FROM Resume WHERE language = ?"
        res = self.execute_query(query, language)
        return res[0]

    def add_skill(self, skill: tuple) -> None:
        query = "INSERT INTO Skills (skill) VALUES (?)"
        self.single_query(query, (skill[0],))
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
    
    def resume_list(self) -> list[str]:
        query = "SELECT language FROM Resume"
        data = self.single_query(query)
        return [d[0] for d in data]

    def delete_database(self):
        if os.path.exists("database.db"):
            os.remove("database.db")
        return None
    

import csv
class CSVHandler:

    def write_dicts_to_csv(self, file_path, dicts):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=dicts[0].keys())
            writer.writeheader()
            writer.writerows(dicts)

    def read_dicts_from_csv(self, file_path):
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                return [dict(row) for row in reader]
        except: 
            print("no dict")
    