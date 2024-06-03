import cv2
import numpy
from ultralytics import YOLO
import math 

def get_feed(*cameras, model = YOLO('yolov8n.pt')):
    classNames = model.names   
    while True:
        camera_images = []
        image = None
        for camera in cameras:
            success, img = camera.read()
            image = cv2.resize(img, (640, 480))
            image = cv2.flip(img, -1)
            results = model.predict(image, stream=True, verbose=False)
        
            for r in results:
                boxes = r.boxes

                for box in boxes:
                
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 
                    confidence = math.ceil((box.conf[0]*100))/100
                    cls = int(box.cls[0])
                    if confidence >= 0.3 and cls == 0:
                            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 3)

                            cls = int(box.cls[0])
                            org = [x1, y1]
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            fontScale = 1
                            color = (255, 0, 0)
                            thickness = 2

                            cv2.putText(image,
                                        classNames[cls] + " " + str(confidence)
                                        , org, font, fontScale, color, thickness)
            camera_images.append(image)
        feed = numpy.concatenate(camera_images, axis=1)
        
        cv2.imshow('feed', feed)
        if cv2.waitKey(2) & 0xFF == 27:
            break

    for camera in cameras:
        camera.release()
    cv2.destroyAllWindows()

def get_image_from_unitree(index_camera = 1):
    IpLastSegment = "162"
    udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port="
    udpPORT = [9201, 9202, 9203, 9204, 9205]
    udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    udpSendIntegratedPipe = udpstrPrevData + str(udpPORT[index_camera - 1]) + udpstrBehindData
    print("udpSendIntegratedPipe:", udpSendIntegratedPipe)
    cap = cv2.VideoCapture( udpSendIntegratedPipe , cv2.CAP_GSTREAMER)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cap

def get_img(index_camera = 1):
        IpLastSegment = "162"
        udpstrPrevData = "udpsrc address=192.168.123."+ IpLastSegment + " port="
        udpPORT = [9201,9202,9203,9204,9205]
        udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
        udpSendIntegratedPipe_0 = udpstrPrevData +  str(udpPORT[index_camera-1]) + udpstrBehindData
        print(udpSendIntegratedPipe_0)
        return cv2.VideoCapture(udpSendIntegratedPipe_0)

get_feed(get_img(1))
# get_feed(get_img(1), get_img(2), get_img(3))   