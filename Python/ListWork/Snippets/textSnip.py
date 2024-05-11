def warn(message, end=False):
    if end==True:
        print("\033[1;31m"+message+"\033[0m", end="")
    else:
        print("\033[1;31m"+message+"\033[0m")
