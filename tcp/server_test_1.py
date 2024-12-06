import socket
import threading

server_ip = "192.168.29.81"

def handle_client(clientsocket, address):
    print(f"Connection from {address} has been established.")
    clientsocket.send(bytes("Welcome to Shah World", "utf-8"))
    while True:
        msg = clientsocket.recv(1024)
        if not msg:
            print(f"Connection from {address} has been closed.")
            break
        print(f"Received from {address}: {msg.decode('utf-8')}")
        clientsocket.send(bytes("So what is going on", "utf-8"))
    clientsocket.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_ip, 3001))
    s.listen(5)
    print("Server is listening...")

    while True:
        clientsocket, address = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(clientsocket, address))
        client_thread.start()

start_server()
