import cv2
import time
# rtsp_url = "rtsp://admin:Admin%401234@61.2.240.25:50547/main"
rtsp_url = "rtsp://admin:Admin%401234@61.2.240.25:50547/main"

# rtsp_url = "rtsp://admin:Admin@1234@61.2.240.25:50547/main"
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Could not open RTSP stream")
else:
    ret, frame = cap.read()
    if ret:
        image_path = f"test_capture/{str(int(time.time()))}.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image saved at {image_path}")
    else:
        print("Error: Could not read frame from the RTSP stream")
cap.release()
