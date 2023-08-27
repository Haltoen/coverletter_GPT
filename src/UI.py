import tkinter as tk
from tkinter import ttk, messagebox 


import database
import GPT_gen
import deepTranslator

class Page(tk.Frame): 
    """
    This class represents a page with basic functionalities as forms.
    """
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self, text=text)
        self.label.pack()
        self.forms = []
        self.text_fields = []  # Initialize the list to store the text_field widgets

    def create_submit_field(self, cmd, input_fields: list, name=None):
        """
        Creates a form (submission_field) on a page
        
        Parameters:
        cmd (func -> None): The function executed on form submission, which handles the forms output.
        input_fields: (list[str | dict | ])
        name: The name of the form, displayed at the top.
        """

        
        input_frame = tk.Frame(self, background="White", borderwidth=10)
        input_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        out_fields = []
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
                    out_field = ("combo", text_field)
                elif "state" in field.keys():
                    var = tk.BooleanVar()
                    var.set(field["state"])
                    text_field = tk.Checkbutton(frame, variable=var, onvalue=1, offvalue=0)
                    out_field = ("check",var)
                elif "content" in field.keys():      
                    input_txt = field["content"]
                    text_field = tk.Text(frame, wrap="word", height=1, width=30)  # Set the initial height to 1 line
                    text_field.insert("1.0", input_txt)
                    out_field = ("text", text_field)
                    self.text_fields.append(text_field)  # Add the text_field widget to the list
                text_field.pack(padx=10, side=tk.RIGHT, fill=tk.X, expand=True)  # Make text fields expand horizontally
                out_fields.append(out_field)
                label = tk.Label(frame, text=txt, width=20)  # Set a fixed width for the labels
                label.pack(side=tk.LEFT, padx=5)  # Align labels to the left
            else:
                return
            
        self.forms.append(out_fields)
        length = len(self.forms)-1
        self.submit_button = tk.Button(
            input_frame,
            text="Submit",
            command=lambda: self.submitfield(cmd, None, length)
        )
        self.submit_button.pack(padx=10)

        # Allow input_frame to expand vertically
        input_frame.pack_propagate(False)

        # Bind the <Key> event to adjust the height of the Text widget based on the content
        for text_field in self.text_fields:
            text_field.bind("<Key>", self.adjust_text_field_height)

    def adjust_text_field_height(self, event=None):
        for text_field in self.text_fields:
            content = text_field.get("1.0", "end-1c")  # Get the content of the Text widget
            if content.strip():  # Check if the content is not empty or just whitespace
                num_lines = int(text_field.index("end-1c").split(".")[0])
                text_field.configure(height=min(num_lines, 10))

    def submitfield(self, command, input=None, form_index=None):
        if input:
            user_inputs = input
        else:
            user_inputs = tuple(
                field[1].get("1.0", tk.END) if field[0] == "text" else
                field[1].get() if field[0] == "combo" else
                field[1].get() if field[0] == "check" else
                None
                for field in self.forms[form_index]
            )
            print(self.forms)
            print("form index", form_index)
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
            label = tk.Label(list_frame, text=elm, borderwidth=3, width=10)
            label.grid(row=index + 1, column=0, sticky="w")  # Use grid to place elements in separate rows
            if cmd:
                submit_button = tk.Button(
                    list_frame, 
                    text="X",
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

class popup(tk.Toplevel):
    def __init__(self, parent, field_names=[], title="no title", text=None):
        super().__init__(parent)
        self.geometry("600x800")
        self.title("Popup Window")
        self.label = tk.Label(self, text="This is a popup window!")
        self.label.pack(pady=20)
        self.field_vars = []
        self.text = text
        self.text_field = None
        self.create_title(title)

        if field_names:
            self.create_true_false_fields(field_names)
        if text:
            self.create_text_field()
       
        self.create_submit_button()

    def create_title(self, title):
        title_label = tk.Label(self, text=title, font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

    def create_text_field(self):
        # Create the text field
        self.text_field = tk.Text(self, wrap="word", height=5, width=40)
        self.text_field.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_field.insert("1.0", self.text)

    def create_true_false_fields(self, field_names):
        for field_name in field_names:
            var = tk.BooleanVar()
            check_button = tk.Checkbutton(self, text=field_name, variable=var, onvalue=True, offvalue=False)
            check_button.pack(anchor="w", padx=10)
            self.field_vars.append((field_name, var))

    def create_submit_button(self):
        submit_button = tk.Button(self, text="Submit", command=self.submit_values)
        submit_button.pack(pady=20)

    def submit_values(self):
        Selected_values = [(field_name, var.get()) for field_name, var in self.field_vars]
        self.destroy()  # Close the popup window after submitting the values
        print (Selected_values)
        return Selected_values


## pages
class HomePage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, "Welcome to the Home Page")

        if not db.userdata:
            self.create_submit_field(db.add_userdata, ["Full name", "Age", "Country", "Address"], "basic user information")
        elif not gpt.has_api_key:
            self.create_submit_field(gpt.add_API_KEY, ["API key"], "Setup OpenAI API key")
        else:
            return None


class Resume (Page):
    def __init__(self, parent, app):
        super().__init__(parent, "This is the Resume Page")
        resumes = db.resume_list()
        self.create_list_field(
            resumes,
            "your resume'",
              db.remove_resume
              )
        self.create_submit_field(
            db.add_resume, 
            [{"txt": "Resume Language", "lst": trans.language_lst()},
            {"txt": "Resume Content", "content": ""}], "add resume"
            )
        self.create_submit_field(
            trans.translate_resume, 
            [{"txt": "from",
            "lst": db.resume_list()},
            {"txt": "to", "lst": trans.language_lst()}],
            "Translate resume"
            )

class Skills (Page):
    def __init__(self, parent, app):
        super().__init__(parent, "This is the skills Page")
        skills=db.skill_list()
        self.create_list_field(skills, "your skills", db.remove_skill)
        self.create_submit_field(db.add_skill, [{"txt": "add skills", "content": ""}])


class CoverLetter (Page):
    def __init__(self, parent, app):
        super().__init__(parent, "This is the coverletter Page")
        self.create_submit_field(gpt.make_coverletter, [{"txt": "Language","lst": db.resume_list()},
                                                         {"txt": "Employer", "content": ""},
                                                           {"txt": "Job description","content": ""},
                                                             {"txt": "ask for additional info", "state": False}],
                                                               "Coverletter Generator")


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
        gpt.ref_app(self)

    def create_navigation_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM)
        for  page in self.pages:
            name = page.__name__
            print(name)
            new_button = tk.Button(button_frame, text=name, command=lambda p=page: self.change_page(p))
            new_button.pack(side=tk.LEFT)

    def change_page(self, new_page):
        self.current_page.pack_forget()
        self.current_page = new_page
        self.show_current_page()

    def show_current_page(self):
        new_page_class = self.current_page
        self.current_page = new_page_class(self, self)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_popup(self, title, field_names=None, text_field=None):
        pop = popup(self, field_names=field_names, title=title, text=text_field)
        self.wait_window(pop)  # Wait for the popup window to be closed
        sub = pop.submit_values()  # Retrieve the submitted values after the popup is closed
        print(sub)
        return sub

    def skill_popup(self, skill_list):
        selected_skills = self.show_popup("Checkmark the skills you have", skill_list)
        #print("Selected skills:", selected_skills)
        for name, b in selected_skills:
            if b:
                self.db.add_skill((name,))
                print(name)

if __name__ == "__main__":
    db = database.db()
    gpt = GPT_gen.GPT_Handler()
    app = App()
    trans = deepTranslator.DeepTrans()
    print("run app")
    app.mainloop()