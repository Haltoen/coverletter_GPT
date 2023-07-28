import sqlite3 as sql3
import os


class db:
    def __init__(self):
        self.setup_complete=False
        
    def execute_query (self, inp_conn, inp_cursor, query: str, params=None)-> None:
        if params:
            inp_cursor.execute(query, params)
        else:
            inp_cursor.execute(query)
        inp_conn.commit()
        return None
    
    def single_query (self, query: str, params) -> None:
        conn = sql3.connect("database.db") #connect/create db file
        cursor = conn.cursor() # used to execute SQL queries
        self.execute_query(conn, cursor, query, params)
        conn.commit()
        conn.close()
        return None
    """
    def multi_query (self, query_lst: list) -> None: 
        conn = sql3.connect("database.db") #connect/create db file
        cursor = conn.cursor() # used to execute SQL queries
        for query in query_lst:
            self.execute_query(conn, cursor, query)
        conn.commit()
        conn.close()
        return None
    """    
    def setup_tables (self) -> None:
        query1 = """
            CREATE TABLE IF NOT EXISTS Resume(
                content TEXT,
                language TEXT,
                PRIMARY KEY (content, language)
            )
        """
        query2 = """
            CREATE TABLE IF NOT EXISTS Skills(
                skill TEXT PRIMARY KEY
            )
        """
        self.multi_query([query1, query2]) 
        return None

    def add_resume(self, content: str, language: str) -> None:
        query = "INSERT INTO Resume (content, language) VALUES (?, ?)"
        self.single_query(query, (content, language))
        return None

    def add_skills(self, skill: str) -> None:
        query = "INSERT INTO Skills (skill) VALUES (?)"
        self.single_query(query, (skill,))  
        return None   
    
    def delete_database(self):
        if os.path.exists("database.db"):
            os.remove("database.db")
        return None
    


   

    
def simple_test():
    # Create a new instance of the db class
    my_db = db()

    # Setup the tables
    my_db.delete_database()
    my_db.setup_tables()

    # Add some resumes and skills
    my_db.add_resume("Resume 1 content", "English")
    my_db.add_resume("Resume 2 content", "French")

    my_db.add_skills("Python")
    my_db.add_skills("JavaScript")

    # Retrieve and print the data
    with sql3.connect("database.db") as conn:
        cursor = conn.cursor()

        # Retrieve data from the Resume table
        cursor.execute("SELECT * FROM Resume")
        resume_data = cursor.fetchall()
        print("Resume Data:")
        print(resume_data)

        # Retrieve data from the Skills table
        cursor.execute("SELECT * FROM Skills")
        skills_data = cursor.fetchall()
        print("\nSkills Data:")
        print(skills_data)

simple_test()
    