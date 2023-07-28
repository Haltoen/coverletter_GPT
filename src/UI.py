import tkinter as tk

class Page(tk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent

        label = tk.Label(self, text=text)
        label.pack()

class Page(tk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent

        self.label = tk.Label(self, text=text)
        self.label.pack()

class HomePage(Page):
    def __init__(self, parent):
        super().__init__(parent, "Welcome to the Home Page")

        self.button_change_text = tk.Button(self, text="Change Text", command=self.change_text)
        self.button_change_text.pack()

    def change_text(self):
        new_text = "New text on the Home Page"
        self.label.config(text=new_text)

class AboutPage(Page):
    def __init__(self, parent):
        super().__init__(parent, "This is the About Page")

        self.button_change_text = tk.Button(self, text="Change Text", command=self.change_text)
        self.button_change_text.pack()

    def change_text(self):
        new_text = "New text on the About Page"
        self.label.config(text=new_text)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("800x600")

        self.pages = [HomePage, AboutPage]
        self.current_page_index = 0

        self.create_navigation_buttons()
        self.show_current_page()

    def create_navigation_buttons(self):
        prev_button = tk.Button(self, text="Previous", command=self.show_previous_page)
        prev_button.pack(side=tk.LEFT)

        next_button = tk.Button(self, text="Next", command=self.show_next_page)
        next_button.pack(side=tk.RIGHT)

    def show_previous_page(self):
        self.current_page_index -= 1
        if self.current_page_index < 0:
            self.current_page_index = len(self.pages) - 1
        self.show_current_page()

    def show_next_page(self):
        self.current_page_index += 1
        if self.current_page_index >= len(self.pages):
            self.current_page_index = 0
        self.show_current_page()

    def show_current_page(self):
        new_page_class = self.pages[self.current_page_index]

        if hasattr(self, "current_page"):
            self.current_page.pack_forget()  # Remove the old page from the window

        self.current_page = new_page_class(self)
        self.current_page.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()


    

