import tkinter as tk
import tkinter.simpledialog
from tkinter import messagebox

class ListManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("List Manager")
        
        self.x = ["BMW", "Mercedes", "Audi"]
        self.previous_x_value = []

        self.add_prefix = ["+", "1"]
        self.remove_prefix = ["-", "2"]
        
        self.create_widgets()
        
    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.listbox = tk.Listbox(self.frame, width=40, height=10)
        self.listbox.pack(pady=10)
        self.listbox.config(width=40, height=10, exportselection=False)  # Imposta larghezza e altezza minima
        
        self.update_listbox()
        
        self.add_button = tk.Button(self.frame, text="Add", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.remove_button = tk.Button(self.frame, text="Remove", command=self.remove_item)
        self.remove_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(self.frame, text="Quit", command=self.master.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=5)
        
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.x:
            self.listbox.insert(tk.END, item)
            
    def add_item(self):
        item = tkinter.simpledialog.askstring("Add", "Enter item to add:")
        if item:
            self.previous_x_value = self.x[:]
            self.x.append(item)
            self.update_listbox()
            
    def remove_item(self):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            self.previous_x_value = self.x[:]
            for index in selected_indices[::-1]:  # Removing from the end to avoid index shifting
                del self.x[index]
            self.update_listbox()
        else:
            messagebox.showerror("Error", "No item selected.")

def main():
    root = tk.Tk()
    app = ListManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
