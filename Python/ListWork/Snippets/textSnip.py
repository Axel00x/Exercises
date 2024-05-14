from datetime import datetime

def warn(message, end=False):
    if end==True:
        print(datetime.now().strftime("%H:%M:%S")+"  "+"\033[1;31m"+message+"\033[0m", end="")
    else:
        print(datetime.now().strftime("%H:%M:%S")+"  "+"\033[1;31m"+message+"\033[0m")
