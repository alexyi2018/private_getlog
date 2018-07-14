import sys

#--->Keep the terminal in the window to see the result<---
def EXIT():
    try:
        INPUT = input("Press the <Enter> key on the keyboard to exit.")
    except SyntaxError:     #Aviod display SyntaxError in python shell
        sys.exit()          #End the routine
        pass   #Do nothing

if __name__ == "__main__":
    EXIT()
