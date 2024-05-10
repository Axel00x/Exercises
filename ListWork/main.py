#Created by Alessandro (Axel00x)

x = ["BMW", "Mercedes", "Audi"]


add_prefix = ["+", "1"]
remove_prefix = ["-", "2"]

lineWidth = 27

def add(y, *args):
    y = y.strip().replace(" ", "")
    if y:
        try:
            x.insert(int(args[0]), y)
        except:
            x.append(y)
    

def remove(y, *args):
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
    if lineWidth > 170:
        lineWidth = 170
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


def add_request():
    userInp = input("Wich item do you want to add? (write the obj/name) ")
    n = input("Specific position in the list? (insert the index 1,2,3...) \033[1;31m[OPTIONAL]\033[0m ")
    
    add(userInp, n)
    
def remove_request():
    userInp = input("Wich item do you want to remove? (write the obj/name/index) " ).replace(" ", "").split(",")
    
    remove(*userInp)

print("\033[1;31mPress Ctrl + C to end task\033[0m")
while True:
    show_list()

# \033[0m       ---   Default
# \033[1;31m    ---   Rosso
# \033[1;37m    ---   Bianco Grassetto
# \033[1;32m    ---   Verde



# \033 Inizia una sequenza di escape ANSI
# [ Introduce i comandi di formattazione
# 1;37;40 Imposta il colore del testo a bianco brillante (1), il colore del testo a bianco (37) e lo sfondo a nero (40)
# m Termina la sequenza di escape ANSI