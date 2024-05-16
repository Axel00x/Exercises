from datetime import datetime

def warn(message, end=False, t=False):
    if end==True and t==True:
        print(datetime.now().strftime("%H:%M:%S")+"  "+"\033[1;31m"+message+"\033[0m", end="")
    elif end==True and t==False:
        print("\033[1;31m"+message+"\033[0m", end="")
    elif end==False and t==True:
        print(datetime.now().strftime("%H:%M:%S")+"  "+"\033[1;31m"+message+"\033[0m")
    else:
        print("\033[1;31m"+message+"\033[0m")
