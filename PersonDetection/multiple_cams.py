from itertools import count
import sys
import cv2
import numpy
from ultralytics import YOLO
import math 

def get_feed(*cameras, model = YOLO('yolov8n.pt')):
    classNames = model.names   
    out1 = cv2.VideoWriter('output_camera_1.avi', cv2.VideoWriter_fourcc(*'MJPG'), 5, (1280, 720))
    out2 = cv2.VideoWriter('output_camera_2.avi', cv2.VideoWriter_fourcc(*'MJPG'), 5, (1280, 720))
    out3 = cv2.VideoWriter('output_camera_3.avi', cv2.VideoWriter_fourcc(*'MJPG'), 5, (1280, 720))

    
    while True:
        camera_images = []
        i = 1
        img = None
        for camera in cameras:
            success, img = camera.read()
            if i == 1:
                # if count%(1*camera.get(cv2.CAP_PROP_FPS)) == 0:
                    out1.write(img)
            elif i == 2:
                # if count%(1*camera.get(cv2.CAP_PROP_FPS)) == 0:
                    out2.write(img)
            elif i == 3:
                # if count%(1*camera.get(cv2.CAP_PROP_FPS)) == 0:
                    out3.write(img)
            results = model.predict(img, stream=True, verbose=False)
        
            for r in results:
                boxes = r.boxes

                for box in boxes:
                
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 
                    confidence = math.ceil((box.conf[0]*100))/100
                    if confidence >= 0.3:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

                        cls = int(box.cls[0])
                        org = [x1, y1]
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        color = (255, 0, 0)
                        thickness = 2

                        cv2.putText(img,
                                    classNames[cls] + " " + str(confidence)
                                    , org, font, fontScale, color, thickness)
            camera_images.append(img)
            i += 1   
        feed = numpy.concatenate(camera_images, axis=1)
        
        #hieronder kan feed veranderd worden naar img om output in aparte vensters te tonen
        cv2.imshow('feed', feed)
        if cv2.waitKey(10) & 0xFF == 27:
            break
    out1.release()
    out2.release()
    out3.release()
    for camera in cameras:
        camera.release()
    cv2.destroyAllWindows()
   

def get_image_from_unitree(index_camera = 1):
    IpLastSegment = "123"
    udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port="
    udpPORT = [9201, 9202, 9203, 9204, 9205]
    udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    udpSendIntegratedPipe = udpstrPrevData + str(udpPORT[index_camera - 1]) + udpstrBehindData
    # print("udpSendIntegratedPipe:", udpSendIntegratedPipe)
    cap = cv2.VideoCapture( udpSendIntegratedPipe ,cv2.CAP_GSTREAMER)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    return cap



cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cap2 = cv2.VideoCapture(1)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# cap3 = cv2.VideoCapture(2)
# cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


get_feed(cap, cap2)
# get_feed(cap, cap2, cap3)
# get_feed((get_image_from_unitree(1), get_image_from_unitree(2), get_image_from_unitree(3)))

   