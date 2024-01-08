import pyfiglet
import termcolor
import os


def print_horizontal_delimiter(len=78):
    print(''.join(["=" for num in range(len)]))


def print_radar():
    with open(str(f"{os.path.dirname(os.path.abspath(__file__))}/radar.txt"), mode="r") as radar:
        print(radar.read())
