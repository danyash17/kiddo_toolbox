import pyfiglet
import termcolor
import os


def print_portscanner_banner():
    do_print("/banner.txt")

def print_backdoor_banner():
    do_print("/backdoor_banner.txt")

def print_cmok_banner():
    do_print("/cmok_banner.txt")

def print_gorynich_banner():
    do_print("/gorynich_banner.txt")

def do_print(banner_path, trollface_path = "/trollface.txt"):
    with open(str(f"{os.path.dirname(os.path.abspath(__file__))}{banner_path}"), mode="r") as banner:
        print(banner.read())
    with open(str(f"{os.path.dirname(os.path.abspath(__file__))}{trollface_path}"), mode="r") as trollface:
        print(trollface.read())