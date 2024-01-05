import pyfiglet
import termcolor
import os
from pathlib import Path

'''
    General Util for printing print
'''

def print_banner(text = "KIDDO TOOLBOX", font = "doom", color = "green"):
    print(termcolor.colored(pyfiglet.figlet_format(text, font), color))
    with open(str(f"{os.path.dirname(os.path.abspath(__file__))}/trollface.txt"), mode="r") as trollface:
        print(trollface.read())
