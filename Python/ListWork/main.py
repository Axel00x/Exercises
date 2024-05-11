#Created by Alessandro (Axel00x)
from Snippets.textSnip import *
from datetime import datetime
import os 

x = ["BMW", "Mercedes", "Audi"]

previous_x_value = []

add_prefix = ["+", "1"]
remove_prefix = ["-", "2"]

lineWidth = 27

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

def show_list():
    lineWidth = len("".join(x)) + len(x)*4
    #print(lineWidth) #Delete this line, its only for debugging
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
    print("")
    
    response = input()
    if response in add_prefix:
        add_request()
    elif response in remove_prefix:
        remove_request()
    else:
        print_error(err_types[1])


def add_request():
    userInp = input("Wich item do you want to add? (write the obj/name) ")
    n = input("Specific position in the list? (insert the index 1,2,3...) \033[1;31m[OPTIONAL]\033[0m ")
    
    add(userInp, n)
    
def remove_request():
    userInp = input("Wich item do you want to remove? (write the obj/name/index) " ).replace(" ", "").split(",")   
    
    remove(*userInp)
    
#-------------         S Y S T E M         -------------    

err_types = ["no items added/removed", "invalid syntax", "unknown error"]

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def print_error(type=err_types[len(err_types)-1]):
        print("")
        print(datetime.now().strftime("%H:%M:%S")+"  ", end="")
        warn("Error: ", True) 
        print(type)
        print("")
        input("Press Enter to continue...")
        
while True:
    try:
        cls() #clear console
        warn("Press Ctrl + C to end task")
        show_list()
        if previous_x_value[:] == x[:]:
            print_error(err_types[0])
    except:
        print_error()


# \033[0m       ---   Default
# \033[1;31m    ---   Rosso
# \033[1;37m    ---   Bianco Grassetto
# \033[1;32m    ---   Verde



# \033 Inizia una sequenza di escape ANSI
# [ Introduce i comandi di formattazione
# 1;37;40 Imposta il colore del testo a bianco brillante (1), il colore del testo a bianco (37) e lo sfondo a nero (40)
# m Termina la sequenza di escape ANSI