import socket
import os
import sys
import threading
from time import sleep
import base64
from colorama import Fore, Back, Style

loop = True
data = ""
clients = []
wfr = False #waiting_for_data
ip_list = []

def p_command(text=""):
    print(f"{Fore.WHITE}>> {Style.RESET_ALL}{text}")



def connect():
    global clients, loop, data
    while loop:
        ip = "192.168.0.208"

        if len(clients) <= 0: p_command(f"{Fore.CYAN}waiting for connection\n")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, 80))
        server.listen(5)


        connection , address = server.accept()
        clients.append({"connection":connection,"address":address})

        if address[0] not in ip_list:
            ip_list.append(address[0])
        else:
            connection.close()

        if len(clients) == 1 : p_command(f"{Fore.GREEN}new connection : {address}  (connections:{len(clients)}){Style.RESET_ALL}\n")
        else: 
            p_command(f"{Fore.GREEN}new connection : {address}  (connections:{len(clients)}){Style.RESET_ALL}\n")
 



def send_data():
    global data, wfr, loop
    while loop:
        if wfr == False and len(clients) > 0:
            wfr = True
            
            data = bytes(input(f""), "utf-8")

            if len(data) > 0:
                if data.decode("utf-8") == "exit": #exit server
                    loop = False

                for index, client in enumerate(clients): 
                    try:
                        client["connection"].send(data)
                    except:
                        p_command(f"{client['address']} disconnected\n")
                        clients.pop(index)



def recv_data():
    global client, wfr, loop
    while loop:
        if len(clients) > 0:
            for index, client in enumerate(clients):
                try:
                    data = client["connection"].recv(1024).decode("ISO-8859-1")
                    data = data.replace("ÿ", " ")
                    if len(data) > 0:
                        p_command(f"{Fore.CYAN}{client['address'][0]}{Style.RESET_ALL} : {data}")
                except:
                    print(f"{Fore.CYAN}{client['address'][0]} disconnected \n")
                    p_command()
                    clients.pop(index)

            try:
                if len(data) > 0:
                    wfr = False
            except:pass



thread_connect = threading.Thread(target=connect)
thread_send = threading.Thread(target=send_data)
thread_recv = threading.Thread(target=recv_data)

thread_connect.start()
thread_send.start()
thread_recv.start()

thread_connect.join()
thread_send.join()
thread_recv.join()


