import tkinter as tk

def on_button_click():
    user_input = entry.get()
    label.config(text="Hello, " + user_input)

# Create the main application window
app = tk.Tk()
app.title("My App")

# Widgets
label = tk.Label(app, text="Enter your name:")
entry = tk.Entry(app)
button = tk.Button(app, text="Submit", command=on_button_click)

# Layout
label.pack()
entry.pack()
button.pack()

# Start the main event loop
app.mainloop()