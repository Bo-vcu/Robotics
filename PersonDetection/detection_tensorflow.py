import cv2
import os
from ultralytics import YOLO
import math
import numpy as np



print(cv2.getBuildInformation())



class camera:

    def __init__(self, cam_id=None, width=640, height=480):
        self.modelFile  = os.path.join("models", "ssd_mobilenet_v2_coco_2018_03_29", "frozen_inference_graph.pb")
        self.configFile = os.path.join("models", "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")
        self.net = cv2.dnn.readNetFromTensorflow(self.modelFile, self.configFile)
        self.width = 1280
        self.middle = int(self.width*0.5)
        self.cam_id = cam_id
        self.height = 720
        
    def detect_objects(self, im, dim = 300):
        blob = cv2.dnn.blobFromImage(im, 1.0, size=(dim, dim), mean=(0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        objects = self.net.forward()
        return objects

    def get_img(self):

        IpLastSegment = "162"
        cam = self.cam_id
        udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port="
        udpPORT = [9201, 9202, 9203, 9204, 9205]
        udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
        udpSendIntegratedPipe_0 = udpstrPrevData + str(udpPORT[cam - 1]) + udpstrBehindData
        print(udpSendIntegratedPipe_0)

        self.cap = cv2.VideoCapture(udpSendIntegratedPipe_0)

    def get_rotation(self, x1, x2):
        if int((x1 + (x2-x1)*0.5) - self.middle) < -100:
            print("Left")
            return "Left"
        elif int((x1 + (x2-x1)*0.5) - self.middle) > 100:
            print("Right")
            return "Right"
        else:
            print("Center")
            return "Center"
            
    def get_distance(self, y1, y2):
        h = y2 - y1
        focal_length = 615
        KNOWN_HEIGHT = 1.8
        distance = (KNOWN_HEIGHT * focal_length) / h
        return distance
    
    def get_walk(self, y1, y2):
        distance = self.get_distance(y1, y2)
        if distance < 2:
            print("Stop")
        else:
            print("Walk " + str(distance - 2) + "m")

    def demo(self):

        self.get_img()
        # model = YOLO('yolov8n.pt')
        # classNames = model.names
        while True:
            self.ret, self.frame = self.cap.read()
            self.frame = cv2.resize(self.frame, (self.width, self.height))
            self.frame = cv2.flip(self.frame, -1)
            # results = model.predict(self.frame, stream=True, verbose=False)
            results = self.detect_objects(self.frame)
            rows, cols, _ = self.frame.shape
            cv2.line(self.frame, (self.middle, 720), (self.middle, 0), (0, 255, 0), 3)

            for i in range(results.shape[2]):
                selected = results[0, 0, i]
        
                classId = int(selected[1])
                score = float(selected[2])

                x1 = int(selected[3] * cols)
                y1 = int(selected[4] * rows)
                w = int(selected[5] * cols - x1)
                h = int(selected[6] * rows - y1)
                x2 = x1 + w
                y2 = y1 + h

                if score > 0.25 and classId == 1:

                    cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.circle(self.frame,(int(x1 + (x2-x1)*0.5), 
                                           int(y1 + (y2-y1)*0.5)), 5, (0,0,255), -1)
                    
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 0.5
                    color = (255, 0, 0)
                    thickness = 2
                    distance = self.get_distance(y1, y2)

                    # self.get_rotation(x1, x2)
                    # if self.get_rotation(x1, x2) == "Center":
                    #     self.get_walk(y1, y2)

                    cv2.putText(self.frame,

                                f"Person C: {score} D: {distance:.2f}m dmid: {int((x1 + (x2-x1)*0.5) - self.middle)}",

                                org, font, fontScale, color, thickness)

            if self.frame is not None:
                cv2.imshow("video0", self.frame)
                # im = self.frame
                # objects = self.detect_objects(net, im)
                # self.display_objects(im, objects, selection=["person"])
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        self.cap.release()

        cv2.destroyAllWindows()

cam = camera(1)
cam.demo()
