import tkinter as tk
from tkinter import ttk

def add_item():
    item = entry_item.get().strip().replace(" ", "")
    if item:
        position = entry_position.get()
        if position:
            try:
                position = int(position)
                x.insert(position, item)
            except ValueError:
                x.append(item)
        else:
            x.append(item)
        update_list()

def remove_item():
    items = entry_remove.get().strip().replace(" ", "").split(",")
    for item in items:
        if item.isdigit() and int(item) in range(len(x)):
            x.pop(int(item))
        elif item in x:
            x.remove(item)
    update_list()

def update_list():
    listbox.delete(0, tk.END)
    for item in x:
        listbox.insert(tk.END, item)

root = tk.Tk()
root.title("List Manager")
root.geometry("400x300")
root.configure(bg="white")

x = ["BMW", "Mercedes", "Audi"]

label_add = tk.Label(root, text="Add Item:", bg="white")
label_add.pack()

entry_item = tk.Entry(root)
entry_item.pack()

label_position = tk.Label(root, text="Position (optional):", bg="white")
label_position.pack()

entry_position = tk.Entry(root)
entry_position.pack()

button_add = ttk.Button(root, text="Add", command=add_item)
button_add.pack()

label_remove = tk.Label(root, text="Remove Item(s):", bg="white")
label_remove.pack()

entry_remove = tk.Entry(root)
entry_remove.pack()

button_remove = ttk.Button(root, text="Remove", command=remove_item)
button_remove.pack()

listbox = tk.Listbox(root, bg="white")
listbox.pack(fill=tk.BOTH, expand=True)

update_list()

root.mainloop()
