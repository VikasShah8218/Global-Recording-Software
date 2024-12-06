import cv2
import os
import time
import datetime
import math
import subprocess

camera_links = {
    1: 'rtsp://admin:Admin%401234@61.2.240.25:50547/main',
    2: 'rtsp://camera2_ip/stream',
    3: 'rtsp://camera3_ip/stream'
}

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
    
    # Video codec (e.g., XVID)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    # For each segment
    for i in range(segments):
        start_time = time.time()
        segment_file = os.path.join(output_folder, f"segment_{i+1}.avi")
        out = cv2.VideoWriter(segment_file, fourcc, 20.0, (frame_width, frame_height))
        print(f"Recording segment {i+1}/{segments}...")
        
        # Record until the segment duration is reached
        while time.time() - start_time < segment_length:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                print("Error: Failed to grab frame.")
                break
        
        # Release the current segment file
        out.release()
        print(f"Segment {i+1} saved to {segment_file}.")
        
        # Optional: Check for stopping the feed before the segment duration
        if time.time() - start_time >= segment_length:
            print(f"Segment {i+1} finished.")

    # Release the camera and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print(f"Recording finished. All segments saved in {output_folder}.")

# Input from user (or as function arguments)
camera_number = int(input("Enter camera number (1, 2, or 3): "))
duration_minutes = int(input("Enter duration for recording (in minutes): "))
segments = int(input("Enter number of segments to divide the recording into: "))

# Call the function to start recording
record_video(camera_number, duration_minutes, segments)
