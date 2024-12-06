import cv2
import os
import time
import datetime
import socket
import json
import threading

server_ip = "192.168.29.213"
camera_links = {
    1: 'rtsp://admin:Admin%401234@61.2.240.25:50547/main',
    2: 'rtsp://camera2_ip/stream',
    3: 'rtsp://camera3_ip/stream'
}


def handle_client(clientsocket, address):
    print(f"Connection from {address} has been established.")
    clientsocket.send(bytes("Welcome to Shah World", "utf-8"))
    while True:
        msg = clientsocket.recv(1024)
        print("*"*50)
        print(msg)
        print("*"*50)
        if not msg:
            print(f"Connection from {address} has been closed.")
            break
        else:
            mssg = msg.decode('utf-8')
            print("*"*50)
            print(mssg)
            print("*"*50)
            try:
                mssg = json.loads(mssg)
                # print(f"Received from {address}: {msg.decode('utf-8')}")
                print(f"Received from {address}: {mssg}")

                if mssg["type"] == "rec":
                    record_video(camera_number=mssg["camera"],duration_minutes=mssg["time"],segments=mssg["segment"])
                    video_recording = threading.Thread(target=record_video, args=(mssg["camera"],mssg["time"],mssg["segment"]))
                    video_recording.start()
                    clientsocket.send(bytes(f"Video thread is started : camera-{mssg["camera"]} {mssg["time"]}min {mssg["segment"]} segment", "utf-8"))
            except Exception as e:
                print("Error",str(e)) 
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

def record_video(camera_number, duration_minutes, segments):
    if camera_number not in camera_links:
        print("Invalid camera number.")
        return
    rtsp_link = camera_links[camera_number]
    
    now = datetime.datetime.now()
    folder_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = f"recordings/{folder_name}"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    duration_seconds = duration_minutes * 60
    
    segment_length = int(duration_seconds / segments)
    print(f"Recording {duration_minutes} minutes from camera {camera_number} into {segments} segments.")
    
    cap = cv2.VideoCapture(rtsp_link)
    if not cap.isOpened():
        print(f"Error: Unable to open camera stream {camera_number}.")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    for i in range(segments):
        start_time = time.time()
        segment_file = os.path.join(output_folder, f"segment_{i+1}.avi")
        out = cv2.VideoWriter(segment_file, fourcc, 20.0, (frame_width, frame_height))
        print(f"Recording segment {i+1}/{segments}...")
        
        while time.time() - start_time < segment_length:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                print("Error: Failed to grab frame.")
                break
        
        out.release()
        print(f"Segment {i+1} saved to {segment_file}.")
        
        if time.time() - start_time >= segment_length:
            print(f"Segment {i+1} finished.")

    cap.release()
    cv2.destroyAllWindows()
    print(f"Recording finished. All segments saved in {output_folder}.")

start_server()