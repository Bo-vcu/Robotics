import sys
import cv2
import numpy
from ultralytics import YOLO
import math 

def get_feed(*cameras, model = YOLO('yolov8n.pt')):
    classNames = model.names    
    while True:
        camera_images = []
        for camera in cameras:
            
            success, img = camera.read()
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
                                    classNames[0] + " " + str(confidence)
                                    , org, font, fontScale, color, thickness)
            camera_images.append(img)
            feed = numpy.concatenate(camera_images, axis=0)
            cv2.imshow('feed', feed)
        if cv2.waitKey(10) & 0xFF == 27:
            break
    for camera in cameras:
        camera.release()
    cv2.destroyAllWindows()

def get_image_from_unitree():
    IpLastSegment = "123"
    cam = 1
    if len(sys.argv) >= 2:
        cam = int(sys.argv[1])
    udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port="
    udpPORT = [9201, 9202, 9203, 9204, 9205]
    udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    udpSendIntegratedPipe = udpstrPrevData + str(udpPORT[cam - 1]) + udpstrBehindData
    print("udpSendIntegratedPipe:", udpSendIntegratedPipe)
    cap3 = cv2.VideoCapture( udpSendIntegratedPipe ,cv2.CAP_GSTREAMER)
    cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    return cap3



cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

# cap2 = cv2.VideoCapture(1)
# cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
# cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)


get_feed(cap)
# get_feed(cap2)
# get_feed(get_image_from_unitree())

   