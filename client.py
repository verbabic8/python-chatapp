import socket
import threading
import sys 


def receive_messages(client):
    while True:
        try:
            message = client.recv(2048)
            if not message:
                print("Disconnected from server")
                break
            print(message.decode())
        except:
            break

def send_messages(client):
    while True:
        try:
            message = sys.stdin.readline()
            client.send(message.encode())
            sys.stdout.write("<You>" + message)
            sys.stdout.flush()
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
client.connect((IP_address, Port)) 

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
send_messages(client)