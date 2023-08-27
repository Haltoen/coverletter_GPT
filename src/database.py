import sqlite3 as sql3
import os


class db:
    """
    This class handles a database containing skills and resume'. 
    """
    def __init__(self):
        self.setup_complete=False
        self.setup_tables()
        self.csv_h = CSVHandler()
        self.userdata = self.get_userdata()
    
    def get_userdata(self):
        """
        Reads userdata from userdata.csv.

        Returns:
        dict: Contains userdata, might be empty.
        """
        data = self.csv_h.read_dicts_from_csv("userdata.csv")
        return data

    def add_userdata(self, data: tuple) -> None:
        """
        Writes userdata to userdata.csv.

        Parameters:
        data (tuple): (full name, age, country, adress)
        """
        userdata = {
            "full name": data[0],
            "age": data[1],
            "country": data[2],
            "address": data[3]
        }
        self.csv_h.write_dicts_to_csv("userdata.csv",[userdata])
        return None
        
    def execute_query (self, inp_conn, inp_cursor, query: str, params: tuple | None):
        """
        Attempts to execute a query.

        Parameters:
        inp_conn (): Sql3 connection to db.
        inp_cursur (): Sql3 cursor object.
        query (str):
        params (tuple, optional): 

        Returns:
        Query output object
        """
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
        """
        activates execute_query, and reads result.

        Parameters:
        query (str):
        params (tuple, optional): 

        Returns:
        tuple: result of query.
        """
        conn = sql3.connect("database.db")  # connect/create db file
        cursor = conn.cursor()  # used to execute SQL queries
        res = self.execute_query(conn, cursor, query, params)
        conn.commit()
        try:
            result = res.fetchall()  # Fetch all the data from the cursor
            conn.close()
            return result
        except:
            return None
    
    def setup_tables (self) -> None:
        """
        Creates the resume and skills tables. 
        """
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

    def add_resume(self, resume_data: tuple) -> None:
        """
        Adds a new resume to the resume table. 

        Parameters:
        resume_data (tuple): Expects (language, content)       
        """
        query = "INSERT INTO Resume (content, language) VALUES (?, ?)"
        params = resume_data[1], resume_data[0]
        self.single_query(query, params)
        return None
    
    def remove_resume(self, language: tuple):
        """
        Removes a resume of a given language from the database.

        Parameters:
        language (tuple): Expects (language,)
        """
        query = "DELETE FROM Resume WHERE language = ?"
        self.single_query(query, language)
        return None
    
    def get_resume(self, language: str):
        """
        Fetches a resumes content, given it's language.

        Parameters:
        language (str):

        Returns 
        str: Which contains the resume content
        """
        print("lan:", language)
        query = f"SELECT content FROM Resume WHERE language = ?"
        res = self.single_query(query, (language,))
        print(res)
        return res[0][0]

    def add_skill(self, skill: tuple) -> None:
        """
        Adds a skill to the skills table
        
        Parameters:
        skill (tuple): Expects (skill: str,)
        """
        query = "INSERT INTO Skills (skill) VALUES (?)"
        self.single_query(query, skill)
        return None 
    
    def remove_skill(self, skill: tuple) -> None:
        """
        Removes a skill from the skills table
        
        Parameters:
        skill (tuple): Expects (skill: str,)
        """
        print("remove", skill)
        query = "DELETE FROM Skills WHERE skill = ?"
        try:
            self.single_query(query, (skill[0],))
        except sql3.IntegrityError as e:
            print(f"Error: {e}")
            # Here, you can display an error message to the user or take other actions
        return None
        
    def skill_list(self) -> list[str]:
        """
        Fetches a list of all the users skills.

        Returns:
        list[str]: Contains all skills from the skill table
        """
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
        """
        Fetches a list of all existing resume languages.

        Returns:
        list[str]: Contains all resume' from the resume table.
        """
        query = "SELECT language FROM Resume"
        data = self.single_query(query)
        return [d[0] for d in data]

    def delete_database(self):
        """
        Deletes database.db, used to reset database.
        """
        if os.path.exists("database.db"):
            os.remove("database.db")
        return None
    

import csv
class CSVHandler:
    """
    Contains functions to read and write to csv files
    """
    def write_dicts_to_csv(self, file_path: str, dicts: list[dict]) -> None:
        """
        Writes multiple dictionaries to a csv file. 

        Parameters:
        file_path (str): File to write to, should be csv.
        dicts (list[dicts]): List of dictionaries written to file.
        """
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=dicts[0].keys())
            writer.writeheader()
            writer.writerows(dicts)

    def read_dicts_from_csv(self, file_path) -> list[dict]:
        """
        Reads multiple dictionaries from a csv file

        Parameters:
        file_path (str): File to read from, should be csv.

        Returns:
        list[dict]: List of the dictionaries in the file. 
        """
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                return [dict(row) for row in reader]
        except: 
            print("no dict")
    