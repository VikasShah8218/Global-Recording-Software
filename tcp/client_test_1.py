import socket

server_ip = "192.168.29.81"

def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, 3001))

    msg = s.recv(1024)
    print(msg.decode("utf-8"))

    while True:
        a = input("--> ")
        s.send(bytes(a, "utf-8"))
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

start_client()
