import tkinter as tk
from tkinter import ttk 
import database


class Page(tk.Frame): 
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self, text=text)
        self.label.pack()
        
    def create_submit_field(self, cmd, name):
        input_frame = tk.Frame(self, background="grey", borderwidth=10)
        input_frame.pack()

        if name:
            label = tk.Label(input_frame, text=name)
            label.pack(side=tk.TOP)

        self.text_field = tk.Entry(input_frame)
        self.text_field.pack(pady=10, side=tk.LEFT)
        self.submit_button = tk.Button(
            input_frame,
            text="Submit",
            command = lambda: self.submitfield(cmd)
        )
        self.submit_button.pack(side=tk.RIGHT)
        
    def submitfield(self, command):
        user_input = self.text_field.get()
        command(user_input) # Pass the user input as the argument to the command function
        self.text_field.delete(0, tk.END)
        app.change_page(type(app.current_page))
       
    def create_list_field(self, lst: list, name: str) -> None:
        list_field = tk.Frame(self, background="white", borderwidth=10)
        list_field.pack(side="bottom")

        if len(lst) == 0:
            header_text = f"{name} (is Empty)"
        else:
            header_text = name

        header = tk.Label(list_field, text=header_text, background="Grey", border=2, borderwidth=3)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")  # Use grid to span multiple columns

        for index, elm in enumerate(lst):
            label = tk.Label(list_field, text=elm, borderwidth=3)
            label.grid(row=index + 1, column=0, sticky="w")  # Use grid to place elements in separate rows

        # Add separator after the list
        separator = ttk.Separator(list_field, orient="horizontal")
        separator.grid(row=len(lst) + 1, column=0, columnspan=2, sticky="ew", pady=5)

        # Adjust column and row weights to allow header to resize properly
        list_field.grid_columnconfigure(0, weight=1)
        list_field.grid_rowconfigure(len(lst) + 1, weight=1)

## pages

class HomePage(Page):
    def __init__(self, parent):
        super().__init__(parent, "Welcome to the Home Page")
        self.input_field = tk.Entry(self)  # Create the input field
        self.input_field.pack()
        self.button_get_input = tk.Button(self, text="Get Input", command=self.get_input_text)
        self.button_get_input.pack()

    def get_input_text(self):
        user_input = self.input_field.get()
        print("User input:", user_input)

class Resume (Page):
    def __init__(self, parent):
        super().__init__(parent, "This is the Resume Page")

        #self.create_submit_field(db.add_skill, "add Resume")

class Skills (Page):
    def __init__(self, parent):
        super().__init__(parent, "This is the skills Page")
        skills=db.skill_list()
        print("skills:", skills)
        self.create_list_field(skills, "your skills")
        self.create_submit_field(db.add_skill, name="add skills")

class CoverLetter (Page):
    def __init__(self, parent):
        super().__init__(parent, "This is the coverletter Page")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("800x600")
        self.pages = [HomePage, Resume, Skills, CoverLetter]
        self.current_page=HomePage
        self.create_navigation_buttons()
        self.show_current_page()
        self.db=db

    def create_navigation_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM)
        for  page in self.pages:
            name = page.__name__
            print(name)
            new_button = tk.Button(button_frame, text=name, command=lambda p=page: self.change_page(p))
            new_button.pack(side=tk.LEFT)

    def change_page(self, new_page):
        print(self.current_page)
        self.current_page.pack_forget()  # Remove the old page from the window
        self.current_page = new_page
        self.show_current_page()

    def show_current_page(self):
        new_page_class = self.current_page
        self.current_page = new_page_class(self)
        self.current_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    db = database.db()
    app = App()
    app.mainloop()


    

