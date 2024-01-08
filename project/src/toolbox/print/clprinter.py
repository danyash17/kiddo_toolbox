import pyfiglet
import termcolor
import os


def print_horizontal_delimiter(len=78):
    print(''.join(["=" for num in range(len)]))


def print_radar():
    with open(str(f"{os.path.dirname(os.path.abspath(__file__))}/radar.txt"), mode="r") as radar:
        print(radar.read())


def print_hose_is_down(target):
    print(f"# Host {target} is down, aborting")


def print_scan_target(target):
    print(f"# Scanning target {target}")


def print_detected_opened_port(target, port):
    print(f"# [+] Port {port} is opened on {target}")
