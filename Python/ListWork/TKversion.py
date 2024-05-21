import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Setup database
def setup_database():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS car_lists
                 (id INTEGER PRIMARY KEY, list_name TEXT, name TEXT)''')
    conn.commit()
    conn.close()

# Functions to interact with the database
def save_to_database():
    list_id = simpledialog.askstring("Save List", "Enter the ID to save the list:")
    if list_id:
        conn = sqlite3.connect('cars.db')
        c = conn.cursor()
        c.execute('DELETE FROM car_lists WHERE list_name = ?', (list_id,))
        for item in x:
            c.execute('INSERT INTO car_lists (list_name, name) VALUES (?, ?)', (list_id, item))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data saved to database successfully.")

def view_saves():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT list_name FROM car_lists')
    rows = c.fetchall()
    conn.close()
    
    if rows:
        saved_lists = "\n".join([f"ID: {row[0]}" for row in rows])
        messagebox.showinfo("Saved Lists", saved_lists)
    else:
        messagebox.showinfo("No Saved Lists", "No saved lists found.")

def import_from_database():
    view_saves()
    list_id = simpledialog.askstring("Import List", "Enter the ID of the list to import:")
    if list_id:
        conn = sqlite3.connect('cars.db')
        c = conn.cursor()
        c.execute('SELECT name FROM car_lists WHERE list_name = ?', (list_id,))
        rows = c.fetchall()
        conn.close()
        
        if rows:
            global x
            x = [row[0] for row in rows]
            refresh_listbox()
            messagebox.showinfo("Success", "Data imported from database successfully.")
        else:
            messagebox.showerror("Error", "No data found for the given ID.")

def delete_from_database():
    view_saves()
    list_id = simpledialog.askstring("Delete List", "Enter the ID of the list to delete:")
    if list_id:
        conn = sqlite3.connect('cars.db')
        c = conn.cursor()
        c.execute('DELETE FROM car_lists WHERE list_name = ?', (list_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data deleted from database successfully.")

# List operations
def add_item():
    item = simpledialog.askstring("Add Item", "Enter the item to add:")
    if item:
        x.append(item.strip())
        refresh_listbox()

def remove_item():
    selected_items = listbox.curselection()
    for index in reversed(selected_items):
        x.pop(index)
    refresh_listbox()

def move_item():
    selected_item = listbox.curselection()
    if selected_item:
        item = x.pop(selected_item[0])
        new_position = simpledialog.askinteger("Move Item", "Enter new position (0-based index):")
        if new_position is not None:
            x.insert(new_position, item)
            refresh_listbox()

def rename_item():
    selected_item = listbox.curselection()
    if selected_item:
        new_name = simpledialog.askstring("Rename Item", "Enter new name:")
        if new_name:
            x[selected_item[0]] = new_name.strip()
            refresh_listbox()

def refresh_listbox():
    listbox.delete(0, tk.END)
    for item in x:
        listbox.insert(tk.END, item)

# Main GUI setup
root = tk.Tk()
root.title("Car List Manager")

x = ["BMW", "Mercedes", "Audi"]

# Setup listbox and scrollbar
frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.MULTIPLE, width=50, height=15)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Initial population of listbox
refresh_listbox()

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Item", command=add_item)
remove_button = tk.Button(button_frame, text="Remove Item", command=remove_item)
move_button = tk.Button(button_frame, text="Move Item", command=move_item)
rename_button = tk.Button(button_frame, text="Rename Item", command=rename_item)

add_button.grid(row=0, column=0, padx=5)
remove_button.grid(row=0, column=1, padx=5)
move_button.grid(row=0, column=2, padx=5)
rename_button.grid(row=0, column=3, padx=5)

database_button_frame = tk.Frame(root)
database_button_frame.pack(pady=10)

save_button = tk.Button(database_button_frame, text="Save to Database", command=save_to_database)
view_button = tk.Button(database_button_frame, text="View Saved Lists", command=view_saves)
import_button = tk.Button(database_button_frame, text="Import from Database", command=import_from_database)
delete_button = tk.Button(database_button_frame, text="Delete from Database", command=delete_from_database)

save_button.grid(row=0, column=0, padx=5)
view_button.grid(row=0, column=1, padx=5)
import_button.grid(row=0, column=2, padx=5)
delete_button.grid(row=0, column=3, padx=5)

setup_database()
root.mainloop()
