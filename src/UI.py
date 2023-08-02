import tkinter as tk
from tkinter import ttk 

import database
import GPT_gen
import functions


class Page(tk.Frame): 
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self, text=text)
        self.label.pack()
        
    def create_submit_field(self, cmd, input_fields: list[str], name=None):
        input_frame = tk.Frame(self, background="White", borderwidth=10)
        input_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.text_fields = []  # Initialize the list to store the text_field widgets
        self.out_fields = []
        if name:
            header = tk.Label(input_frame, text=name)
            header.pack(pady=3, side=tk.TOP)

        for field in input_fields:
            frame = tk.Frame(input_frame, borderwidth=10)
            frame.pack()
            if type(field) is dict:
                txt = field["txt"]
                if "lst" in field.keys():
                    text_field = ttk.Combobox(frame, values=field["lst"], width=37)
                    out_field = ("combo",text_field)
                elif "state" in field.keys():
                    var = tk.BooleanVar()
                    text_field = tk.Checkbutton(frame, variable=var, onvalue=1, offvalue=0)
                    out_field = ("check",var)       
            else:
                txt = field
                print(txt)
                text_field = tk.Text(frame, wrap="word", height=1, width=30)  # Set the initial height to 1 line
                out_field = ("text", text_field)
                self.text_fields.append(text_field)  # Add the text_field widget to the list
            text_field.pack(padx=10, side=tk.RIGHT, fill=tk.X, expand=True)  # Make text fields expand horizontally
            self.out_fields.append(out_field)
            label = tk.Label(frame, text=txt, width=20)  # Set a fixed width for the labels
            label.pack(side=tk.LEFT, padx=5)  # Align labels to the left

        self.submit_button = tk.Button(
            input_frame,
            text="Submit",
            command=lambda: self.submitfield(cmd)
        )
        self.submit_button.pack(padx=10)


        # Allow input_frame to expand vertically
        input_frame.pack_propagate(False)

        # Bind the <Key> event to adjust the height of the Text widget based on the content
        for text_field in self.text_fields:
            text_field.bind("<Key>", self.adjust_text_field_height)

    def adjust_text_field_height(self, event):
        for text_field in self.text_fields:
            num_lines = int(text_field.index("end-1c").split(".")[0])  # Get the number of lines of text
            text_field.configure(height=min(num_lines, 10))  # Update the height based on the number of lines

    def submitfield(self, command, input=None):
        print(input)
        if input:
            user_inputs = input
        else:
            user_inputs = tuple(
                field[1].get("1.0", tk.END) if field[0] == "text" else field[1].get() if field[0]== "combo" else field[1]
                for field in self.out_fields
            )
        print(user_inputs)
        command(user_inputs)  # Pass the user input as the argument to the command function
        app.change_page(type(app.current_page))


    def create_list_field(self, lst: list[str], name: str, cmd=None) -> None:
        print("lst:", lst)
        list_frame = tk.Frame(self, background="white", borderwidth=10)
        list_frame.pack(side="bottom")

        if len(lst) == 0:
            header_text = f"{name} (is Empty)"
        else:
            header_text = name

        header = tk.Label(list_frame, text=header_text, background="Grey", border=2, borderwidth=3)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")  # Use grid to span multiple columns

        for index, elm in enumerate(lst):
            print(elm)
            label = tk.Label(list_frame, text=elm, borderwidth=3)
            label.grid(row=index + 1, column=0, sticky="w")  # Use grid to place elements in separate rows
            if cmd:
                submit_button = tk.Button(
                    list_frame, 
                    text="del",
                    command= lambda elm=elm: self.submitfield(cmd, [elm])
                )
                submit_button.grid(row=index + 1, column=1, sticky="w")

        # Add separator after the list
        separator = ttk.Separator(list_frame, orient="horizontal")
        separator.grid(row=len(lst) + 1, column=0, columnspan=2, sticky="ew", pady=5)

        # Adjust row weight to allow header to resize properly
        list_frame.grid_rowconfigure(len(lst) + 1, weight=1)

        # Move the list_frame to the right using pack
        list_frame.pack(side="right", padx=10)

## pages
class HomePage(Page):
    def __init__(self, parent):
        super().__init__(parent, "Welcome to the Home Page")
        self.create_submit_field(db.add_userdata, ["Full name", "Age", "Country", "Address"], "basic user information")
        #self.create_submit_field(gpt.setup_API_KEY, ["API key"], "Setup OpenAI API key")
            #self.create_submit_field(gpt.setup_API_KEY, ["API key"], "Setup OpenAI API key")
    def get_input_text(self):
        user_input = self.input_field.get()
        print("User input:", user_input)

class Resume (Page):
    def __init__(self, parent):
        super().__init__(parent, "This is the Resume Page")
        resumes = db.resume_list()
        self.create_list_field(resumes, "your resume'", db.remove_resume)
        self.create_submit_field(db.add_resume, [{"txt": "Resume Language", "lst": trans.language_lst()},"Resume Content"], "add resume")
        self.create_submit_field(trans.translate_resume, [{"txt": "from", "lst": db.resume_list()},{"txt": "to", "lst": trans.language_lst()}], "Translate resume")

class Skills (Page):
    def __init__(self, parent):
        super().__init__(parent, "This is the skills Page")
        skills=db.skill_list()
        self.create_list_field(skills, "your skills", db.remove_skill)
        self.create_submit_field(db.add_skill, ["add skills"])
    
class CoverLetter (Page):
    def __init__(self, parent):
        super().__init__(parent, "This is the coverletter Page")
        self.create_submit_field(db.add_resume, ["Employer", {"txt": "Language","lst": db.resume_list()}, "Job description", {"txt": "ask for additional info", "state": True}], "Coverletter Generator")

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
    gpt = GPT_gen.GPT_Handler()
    trans = functions.Trans()
    app = App()
    print("run app")
    app.mainloop()