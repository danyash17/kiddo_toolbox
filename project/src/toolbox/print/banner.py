import pyfiglet
import termcolor
import os


def print_banner(color="green"):
    with open(str(f"{os.path.dirname(os.path.abspath(__file__))}/banner.txt"), mode="r") as banner:
        print(banner.read())
    with open(str(f"{os.path.dirname(os.path.abspath(__file__))}/trollface.txt"), mode="r") as trollface:
        print(trollface.read())
