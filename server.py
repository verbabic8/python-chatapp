# Python program to implement server side of chat room. 
import socket 
import threading
import sys 
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 

IP_address = str(sys.argv[1]) 

Port = int(sys.argv[2]) 

server.bind((IP_address, Port)) 

server.listen(100) 

list_of_clients = [] 

def clientthread(conn, addr): 

    conn.send(("Welcome to this chatroom!").encode()) 

    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
                    decoded_msg = message.decode()
                    print ("<" + addr[0] + "> " + decoded_msg) 

                    message_to_send = "<" + addr[0] + "> " + decoded_msg 
                    broadcast(message_to_send.encode(), conn) 

                else: 
                    remove(conn) 

            except: 
                continue

def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
                remove(clients) 

def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 

def server_input_broadcast():
    while True:
        try:
            message = input()
            if message:
                message_to_send = "<Server> " + message
                broadcast(message_to_send.encode(), None)
        except:
            break

threading.Thread(target=server_input_broadcast, daemon=True).start()

while True: 
    conn, addr = server.accept() 
    list_of_clients.append(conn) 

    print (addr[0] + " connected")

    start_new_thread(clientthread,(conn,addr))     

conn.close() 
server.close()