from itertools import count
import cv2
import numpy
# from ultralytics import YOLO
import math 

def get_feed(*cameras):
    
    while True:
        camera_images = []

        img = None
        for camera in cameras:
            success, img = camera.read()
            img = cv2.flip(img, 0)
            
        
           
            camera_images.append(img)
        feed = numpy.concatenate(camera_images, axis=1)
        
        cv2.imshow('feed', feed)
        if cv2.waitKey(10) & 0xFF == 27:
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
    # print("udpSendIntegratedPipe:", udpSendIntegratedPipe)
    cap = cv2.VideoCapture( udpSendIntegratedPipe , cv2.CAP_GSTREAMER)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cap



# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# cap2 = cv2.VideoCapture(1)
# cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# cap3 = cv2.VideoCapture(2)
# cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# get_feed(cap)
# get_feed(cap, cap2, cap3)
get_feed(get_image_from_unitree(1)
        #   , get_image_from_unitree(2), get_image_from_unitree(3)
          )

   