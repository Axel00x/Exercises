# Created by Alessandro (Axel00x)
from Snippets.textSnip import *
from datetime import datetime
import os
import sqlite3
import traceback

x = ["BMW", "Mercedes", "Audi"]

previous_x_value = []
previous_y_value = []

add_prefix = ["+", "1"]
remove_prefix = ["-", "2"]
move_prefix = ["->", "3"]
rename_prefix = ["r", "4"]
database_prefix = ["d"]

lineWidth = 27

# Database setup
def setup_database():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS car_lists
                 (id INTEGER PRIMARY KEY, list_name TEXT, name TEXT)''')
    conn.commit()
    conn.close()

def save_to_database():
    list_id = input("Enter the ID to save the list: ")
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('DELETE FROM car_lists WHERE list_name = ?', (list_id,))
    for item in x:
        c.execute('INSERT INTO car_lists (list_name, name) VALUES (?, ?)', (list_id, item))
    conn.commit()
    conn.close()
    print("\033[1;32mData saved to database successfully.\033[0m")
    input("Press Enter to continue...")

def view_saves():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT list_name FROM car_lists')
    rows = c.fetchall()
    conn.close()
    
    if rows:
        print("\033[1;37mSaved lists:\033[0m")
        for row in rows:
            print(f"ID: {row[0]}")
    else:
        print("\033[1;31mNo saved lists found.\033[0m")
    
    input("Press Enter to continue...")

def import_from_database():
    view_saves()
    list_id = input("Enter the ID of the list to import: ")
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('SELECT name FROM car_lists WHERE list_name = ?', (list_id,))
    rows = c.fetchall()
    conn.close()
    
    if rows:
        global x
        x = [row[0] for row in rows]
        print("\033[1;32mData imported from database successfully.\033[0m")
    else:
        print("\033[1;31mNo data found for the given ID.\033[0m")
    
    input("Press Enter to continue...")

def delete_from_database():
    view_saves()
    list_id = input("Enter the ID of the list to delete: ")
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('DELETE FROM car_lists WHERE list_name = ?', (list_id,))
    conn.commit()
    conn.close()
    print("\033[1;32mData deleted from database successfully.\033[0m")
    input("Press Enter to continue...")

def add(y, *args):
    global previous_x_value
    y = y.strip().replace(" ", "")
    previous_x_value = x[:]
    if y:
        try:
            x.insert(int(args[0]), y)
        except:
            x.append(y)

def remove(y, *args):
    global previous_x_value
    previous_x_value = x[:]
    if y in x:
        x.remove(y)
    elif str(y) in map(str, range(len(x))):
        x.pop(int(y))
        
    if args:
        for arg in args:
            if arg.isdigit() and int(arg) in range(len(x)):
                x.pop(int(arg))
            elif arg in x: 
                x.remove(arg)

def move(y, pos=int(len(x)-1)):
    global previous_x_value, previous_y_value
    previous_x_value = x[:]
    
    if str(y) == str(pos):
        print_error(err_types[2])
    
    if y in x:
        previous_y_value = y
        x.pop(x.index(y))
        x.insert(int(pos), y)
    elif str(y) in map(str, range(len(x))):
        previous_y_value = x[int(y)]
        x.pop(int(y))
        x.insert(int(pos), previous_y_value)
    elif str(y) == str(pos):
        print_error(err_types[2])
        
def rename(y, name):
    if y in x:
        x[x.index(y)] = name
    elif str(y) in map(str, range(len(x))):
        x[int(y)] = name

def show_list():
    lineWidth = len("".join(x)) + len(x)*4
    if lineWidth > 160:
        lineWidth = 160
    elif lineWidth < 0:
        lineWidth = 0
        
    def drawLine(x):
        line_width = []
        for i in range(x):
            line_width.append("-")
        print("".join(line_width))
        
    drawLine(lineWidth)
    print(x)
    drawLine(lineWidth)
    
    print(f"\033[1;32m{add_prefix[0]}\033[0m or \033[1;32m{add_prefix[1]}\033[0m to \033[1;37madd\033[0m an item.")
    print(f"\033[1;32m{remove_prefix[0]}\033[0m or \033[1;32m{remove_prefix[1]}\033[0m to \033[1;37mremove\033[0m an item.")
    print(f"\033[1;32m{move_prefix[0]}\033[0m or \033[1;32m{move_prefix[1]}\033[0m to \033[1;37mmove\033[0m an item.")
    print(f"\033[1;32m{rename_prefix[0]}\033[0m or \033[1;32m{rename_prefix[1]}\033[0m to \033[1;37mrename\033[0m an item.")
    print(f"\033[1;32m{database_prefix[0]}\033[0m to \033[1;37maccess database options\033[0m.")
    print("")
    
    response = input()
    if response in add_prefix:
        add_request()
    elif response in remove_prefix:
        remove_request()
    elif response in move_prefix:
        move_request()
    elif response in rename_prefix:
        rename_request()
    elif response in database_prefix:
        database_options()
    else:
        print_error(err_types[1])

def database_options():
    global save_prefix, view_prefix, import_prefix, delete_prefix
    save_prefix = ["s", "5"]
    view_prefix = ["v", "6"]
    import_prefix = ["i", "7"]
    delete_prefix = ["del", "8"]
    
    cls()
    print("\033[1;37mDatabase options:\033[0m")
    print(f"\033[1;32m{save_prefix[0]}\033[0m or \033[1;32m{save_prefix[1]}\033[0m to \033[1;37msave\033[0m the list to the database.")
    print(f"\033[1;32m{view_prefix[0]}\033[0m or \033[1;32m{view_prefix[1]}\033[0m to \033[1;37mview\033[0m saved lists.")
    print(f"\033[1;32m{import_prefix[0]}\033[0m or \033[1;32m{import_prefix[1]}\033[0m to \033[1;37mimport\033[0m a list from the database.")
    print(f"\033[1;32m{delete_prefix[0]}\033[0m or \033[1;32m{delete_prefix[1]}\033[0m to \033[1;37mdelete\033[0m a list from the database.")
    print("")
    
    response = input()
    if response in save_prefix:
        save_to_database()
    elif response in view_prefix:
        view_saves()
    elif response in import_prefix:
        import_from_database()
    elif response in delete_prefix:
        delete_from_database()
    else:
        print_error(err_types[1])

def add_request():
    userInp = input("Which item do you want to add? (write the obj/name) ")
    n = input("Specific position in the list? (insert the index 1,2,3...) \033[1;31m[OPTIONAL]\033[0m ")
    
    add(userInp, n)
    
def remove_request():
    userInp = input("Which item do you want to remove? (write the obj/name/index) ").replace(" ", "").split(",")   
    
    remove(*userInp)
    
def move_request():
    userInp = input('Which item do you want to move? [obj/name/index] to [index] ').split()
    
    move(*userInp)

def rename_request():
    userInp = input('Which item do you want to rename? [obj/name/index] to [obj/name] ').split()
    
    rename(*userInp)

#-------------         S Y S T E M         -------------    

err_types = ["no items added/removed", "invalid syntax", "values must be different", "unknown error"]

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def print_error(type=err_types[len(err_types)-1]):
    print("")
    warn("Error: ", True, True) 
    print(type)
    print("")
    input("Press Enter to continue...")

setup_database()

while True:
    try:
        cls() #clear console
        warn("Press Ctrl + C to end task")
        show_list()
        if previous_x_value[:] == x[:]:
            print_error(err_types[0])
    except Exception as e:
        traceback.print_exc()  # Print the traceback of the error
        print_error()
