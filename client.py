import socket
import sys
import threading

def receive_messages(server):
    while True:
        try:
            message = server.recv(2048)
            if not message:
                print("Disconnected from server")
                break
            print(message.decode())
        except:
            break

def send_messages(server):
    while True:
        try:
            message = sys.stdin.readline()
            server.send(message.encode())
            sys.stdout.write("<You>" + message)
            sys.stdout.flush()
        except:
            break

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((IP_address, Port))

threading.Thread(target=receive_messages, args=(server,), daemon=True).start()
send_messages(server)