# Wordle Combos
# version : 1.0

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import json
import string

button_states_file = "button_states.json"

def save_button_states():
    with open(button_states_file, 'w') as file:
        json.dump(button_states, file)

def load_button_states():
    try:
        with open(button_states_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def close_program():
    root.destroy()

def clear_output():
    output_text.delete(1.0, tk.END)

def generate_combinations(combination, index=0, current="", excluded_letters=None):
    combinations = []

    if index == len(combination):
        if len(current) == 5:
            combinations.append(current.lower())
        return combinations

    if combination[index] == '_':
        for char in (excluded_letters or string.ascii_lowercase):
            combinations.extend(generate_combinations(combination, index + 1, current + char, excluded_letters))
    else:
        combinations.extend(generate_combinations(combination, index + 1, current + combination[index], excluded_letters))

    return combinations

def generate_button_clicked():
    global button_states

    if 'button_states' not in globals():
        button_states = load_button_states()

    combination = entry.get().strip()
    if len(combination) < 5 or '_' not in combination:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Error: Input 5 characters, use '_' for unknown characters.")
    else:
        excluded_letters = [letter.lower() for letter, state in button_states.items() if not state]

        output_text.delete(1.0, tk.END)
        combinations = generate_combinations(combination, excluded_letters=set(excluded_letters))
        combinations.sort()

        for i, combination in enumerate(combinations, start=1):
            output_text.insert(tk.END, f"{i}. {combination}\n")

def save_output():
    text_content = output_text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        initialfile="wordle_combinations.txt" 
    )
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_content)


def letters_window():
    global button_states

    def on_drag_start(event):
        nonlocal x, y
        x = event.x
        y = event.y

    def on_drag_motion(event):
        nonlocal x, y
        deltax = event.x - x
        deltay = event.y - y
        new_x = window.winfo_x() + deltax
        new_y = window.winfo_y() + deltay
        window.geometry(f"+{new_x}+{new_y}")

    def letter_button_clicked(button, letter):
        button_state = button_states.get(letter, False)
        new_state = not button_state
        button_states[letter] = new_state
        if new_state:
            button.config(bg='#201c1c', fg='white')
        else:
            button.config(bg='white', fg='black')

    def clear_button_clicked():
        for button in letter_buttons:
            letter = button.cget("text")
            button.config(bg='white', fg='black')
            button_states[letter] = False

    def close_letters_window():
        save_button_states()
        window.destroy()

    button_states = load_button_states()

    window = tk.Toplevel(root)
    window.title("Letters Window")
    window.configure(bg='#201c1c', highlightbackground='#c0c0c0', highlightthickness=1)
    window_width = 600
    window_height = 200
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    window.overrideredirect(True)
    x = 0
    y = 0
    window.bind("<ButtonPress-1>", on_drag_start)
    window.bind("<B1-Motion>", on_drag_motion)

    letters = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M"]
    ]

    letter_buttons = [] 

    for row_index, letter_row in enumerate(letters):
            for col_index, letter in enumerate(letter_row):
                button = tk.Button(window, text=letter)
                button.config(command=lambda b=button, l=letter: letter_button_clicked(b, l),
                            width=3, height=2)
                button.grid(row=row_index, column=col_index, padx=5, pady=5, sticky='nsew')
                letter_buttons.append(button)

                if button_states.get(letter, False):
                    button.config(bg='#201c1c', fg='white')
                else:
                    button.config(bg='white', fg='black')

            window.grid_rowconfigure(row_index, weight=1, minsize=50)

            clear_button = tk.Button(window, text="Clear", command=clear_button_clicked, bg='#201c1c', fg='white')
            clear_button.grid(row=3, column=4, padx=10, pady=10, sticky='ew')

            close_button = tk.Button(window, text="Close", command=close_letters_window, bg='#201c1c', fg='white')
            close_button.grid(row=3, column=5, padx=10, pady=10, sticky='ew')

            for i in range(len(letters)):
                window.grid_rowconfigure(i, weight=1)
            window.grid_rowconfigure(len(letters), weight=1)
            for j in range(len(letters[0])):
                window.grid_columnconfigure(j, weight=1, uniform="equal")

    window.mainloop()

def open_settings_window():
    def on_drag_start(event):
        nonlocal x, y
        x = event.x
        y = event.y

    def on_drag_motion(event):
        nonlocal x, y
        deltax = event.x - x
        deltay = event.y - y
        new_x = window.winfo_x() + deltax
        new_y = window.winfo_y() + deltay
        window.geometry(f"+{new_x}+{new_y}")

    def close_settings_window():
        window.destroy()
    window = tk.Toplevel(root)
    window.title("Settings Window")
    window.configure(bg='#201c1c', highlightbackground='#c0c0c0', highlightthickness=1)
    window_width = 500
    window_height = 250
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    window.overrideredirect(True)
    x = 0
    y = 0
    window.bind("<ButtonPress-1>", on_drag_start)
    window.bind("<B1-Motion>", on_drag_motion)
    
    theme_label = tk.Label(window, text="Theme", bg='#201c1c', fg='white')
    theme_label.pack(pady=10)
    
    button_frame = tk.Frame(window, bg='#201c1c')
    button_frame.pack()
    
    light_button = tk.Button(button_frame, text="Light", bg='#201c1c', fg='white')
    light_button.pack(side=tk.LEFT, padx=5)
    
    dark_button = tk.Button(button_frame, text="Dark", bg='#201c1c', fg='white')
    dark_button.pack(side=tk.LEFT, padx=5)
    
    close_button = tk.Button(window, text="Close", command=close_settings_window, bg='#201c1c', fg='white')
    close_button.place(relx=0.5, rely=0.95, anchor=tk.S)

# Main
root = tk.Tk()
root.title("Wordle Combos 1.0")

icon_path = "Wordle_Combos_logo.ico"
root.iconbitmap(icon_path)

root.configure(bg='#201c1c')
window_width = 400
window_height = 1040
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

root.resizable(False, False)

frame = tk.Frame(root, bg='#201c1c')
frame.pack(padx=20, pady=20)

entry_label = tk.Label(frame, text="Enter your Wordle guess:", bg='#201c1c', fg='white')
entry_label.grid(row=0, column=0, sticky='w', pady=10, padx=10)

entry = tk.Entry(frame)
entry.grid(row=0, column=1, sticky='w', pady=10, padx=10)

generate_button = tk.Button(frame, text="Generate", command=generate_button_clicked, bg='#201c1c', fg='white')
generate_button.grid(row=1, column=0, columnspan=1, pady=10, padx=10, sticky='ew')

exclude_letters_button = tk.Button(frame, text="Exclude letters", command=letters_window, bg='#201c1c', fg='white')
exclude_letters_button.grid(row=1, column=1, columnspan=1, pady=10, padx=10, sticky='ew')

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)

output_text = tk.Text(frame, wrap=tk.WORD, height=50, width=15, yscrollcommand=scrollbar.set, bg='#201c1c', fg='white')
output_text.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

scrollbar.config(command=output_text.yview)
scrollbar.grid(row=2, column=2, sticky='ns')

clear_button = tk.Button(frame, text="Clear", command=clear_output, bg='#201c1c', fg='white')
clear_button.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='ew')

save_button = tk.Button(frame, text="Save", command=save_output, bg='#201c1c', fg='white')
save_button.grid(row=3, column=1, padx=5, pady=10, sticky='ew')

exit_button = tk.Button(frame, text="Exit", command=close_program, bg='#201c1c', fg='white')
exit_button.grid(row=3, column=2, padx=(5, 10), pady=10, sticky='ew')

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

settings_icon = ImageTk.PhotoImage(Image.open("settings_icon.png").resize((25, 25)))
settings_button = tk.Button(root, image=settings_icon, bg='#201c1c', bd=0, command=open_settings_window)

program_name_label = tk.Label(root, text="Wordle Combos 1.0", bg='#201c1c', fg='white')
program_name_label.pack(side=tk.BOTTOM, padx=10, pady=10, anchor=tk.SW)

settings_button.pack(side=tk.BOTTOM, padx=10, pady=10, anchor=tk.SE)

root.update_idletasks()
center_window(root)

root.mainloop()
