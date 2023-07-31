import tkinter as tk
from tkinter import ttk 
import database


class Page(tk.Frame): 
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self, text=text)
        self.label.pack()
        
    def create_submit_field(self, cmd, input_fields: list[str]):
        input_frame = tk.Frame(self, background="grey", borderwidth=10)
        input_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.text_fields = []  # Initialize the list to store the text_field widgets

        for index, field in enumerate(input_fields):
            frame = tk.Frame(input_frame)
            frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            label = tk.Label(frame, text=field)
            label.pack(side=tk.TOP)

            text_field = tk.Text(frame, wrap="word", height=2)  # Set the initial height to 2 lines
            text_field.pack(side=tk.TOP)
            self.text_fields.append(text_field)  # Add the text_field widget to the list

        button_frame = tk.Frame(input_frame, background="grey", borderwidth=2)
        button_frame.pack(fill=tk.BOTH, expand=True)

        self.submit_button = tk.Button(
            button_frame,
            text="Submit",
            command=lambda: self.submitfield(cmd)
        )
        self.submit_button.pack(pady=10, side=tk.TOP)

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
            user_inputs = tuple(field.get("1.0", tk.END) for field in self.text_fields)
            for field in self.text_fields:
                field.delete("1.0", tk.END)  # Delete all the content from the Text widget
        command(user_inputs)  # Pass the user input as the argument to the command function
        app.change_page(type(app.current_page))

            

    
    def create_list_field(self, lst: list, name: str, cmd=None) -> None:
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

        self.create_submit_field(db.add_resume, ["Resume Content","Language"])

class Skills (Page):
    def __init__(self, parent):
        super().__init__(parent, "This is the skills Page")
        skills=db.skill_list()
        self.create_list_field(skills, "your skills", db.remove_skill)
        self.create_submit_field(db.add_skill, ["add skills"])

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


    

