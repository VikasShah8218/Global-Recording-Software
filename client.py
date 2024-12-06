import socket
import json

server_ip = "192.168.29.213"

def get_valid_input(prompt, validation_func, error_message):
    while True:
        try:
            value = input(prompt)
            return value if validation_func(value) else print(error_message)
        except ValueError:
            print("Invalid input! Please try again.")

def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, 3001))

    msg = s.recv(1024)
    print(msg.decode("utf-8"))

    while True:

        print("Please select your \n 1. Camera \n 2. Time in min \n 3. Segments")
        print("Enter: OK for recording")

        camera = int(get_valid_input( "Camera No. (1-100): ", lambda x: x.isdigit() and 1 <= int(x) <= 100,"Must be a number between 1 and 100."))
        time = int(get_valid_input("Time min (1-600): ",lambda x: x.isdigit() and 1 <= int(x) <= 600,"Must be a number between 1 and 600."))
        segment = int(get_valid_input("Segments (0-10): ",lambda x: x.isdigit() and 0 <= int(x) <= 10,"Must be a number between 0 and 10."))
        ack = get_valid_input("Start Recording ? (must be 'ok'): ",lambda x: x.strip().lower() == "ok", "Must be 'ok'.")

        if ack == "ok":
            print("ack run")
            data = json.dumps({"type":"rec","camera":camera,"time":time,"segment":segment})
        else:
            data=json.dumps({})
        print(data)
        s.send(bytes(data, "utf-8"))
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

start_client()
