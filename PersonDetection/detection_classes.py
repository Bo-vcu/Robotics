import cv2
import os
from ultralytics import YOLO
import math
import numpy as np

print(cv2.getBuildInformation())

class output:
    def get_rotation_cmd(x1, x2, middle=640):
        if int((x1 + (x2-x1)*0.5) - middle) < -100:
            print("Left")
            return "Left"
        elif int((x1 + (x2-x1)*0.5) - middle) > 100:
            print("Right")
            return "Right"
        else:
            print("Center")
            return "Center"
            
    def get_distance(y1, y2):
        h = y2 - y1
        focal_length = 615
        KNOWN_HEIGHT = 1.8
        distance = (KNOWN_HEIGHT * focal_length) / h
        return distance
    
    def get_walk_cmd(y1, y2):
        distance = output.get_distance(y1, y2)
        if distance < 2:
            print("Stop")
        else:
            print("Walk " + str(distance - 2) + "m")

class model:
    def __init__(self):
        pass
    def detect_objects(self, frame):
        pass

class model_tensorflow(model):
    def __init__(self):
        self.modelFile  = os.path.join("models", "ssd_mobilenet_v2_coco_2018_03_29", "frozen_inference_graph.pb")
        self.configFile = os.path.join("models", "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")
        self.model_tensorflow = cv2.dnn.readNetFromTensorflow(self.modelFile, self.configFile)

    def detect_objects(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1.0, size=(300, 300), mean=(0, 0, 0), swapRB=True, crop=False)
        self.model_tensorflow.setInput(blob)
        objects = self.model_tensorflow.forward()
        return objects
   
class model_ultralytics(model):
    def __init__(self):
        self.model_ultralytics = YOLO('yolov8n.pt')
        self.classNames = self.model_ultralytics.names

    def detect_objects(self, frame):
        return self.model_ultralytics.predict(frame, stream=True, verbose=False)
   

class camera:
    def __init__(self, cam_id=None, model=None):
        self.width = 1280
        self.middle = int(self.width*0.5)
        self.cam_id = cam_id
        self.height = 720
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 0.5
        self.color = (255, 0, 0)
        self.thickness = 2
        self.model = model
        
    def format_frame(self):
        self.ret, self.frame = self.cap.read()
        self.frame = cv2.resize(self.frame, (self.width, self.height))
        self.frame = cv2.flip(self.frame, -1)

    def get_img(self):
        IpLastSegment = "162"
        cam = self.cam_id
        udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port="
        udpPORT = [9201, 9202, 9203, 9204, 9205]
        udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
        udpSendIntegratedPipe_0 = udpstrPrevData + str(udpPORT[cam - 1]) + udpstrBehindData
        print(udpSendIntegratedPipe_0)
        self.cap = cv2.VideoCapture(udpSendIntegratedPipe_0)


    def read_cam(self):
        self.ret, self.frame = self.cap.read()
        self.frame = cv2.resize(self.frame, (self.width, self.height))
        self.frame = cv2.flip(self.frame, -1)
        

    def demo_tensorflow(self):
        self.get_img()
        while True:
            self.format_frame()
            results = self.model.detect_objects(self.frame)
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
                    distance = output.get_distance(y1, y2)

                    
                    if output.get_rotation_cmd(x1, x2) == "Center":
                        output.get_walk_cmd(y1, y2)

                    cv2.putText(self.frame,
                                f"Person C: {score} D: {distance:.2f}m dmid: {int((x1 + (x2-x1)*0.5) - self.middle)}",
                                org, self.font, self.fontScale, self.color, self.thickness)

            if self.frame is not None:
                cv2.imshow("video0", self.frame)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    # def demo_ultralytics(self):
    #         self.get_img()
    #         --model = YOLO('yolov8n.pt')
    #         --classNames = model.names

    #         while True:
    #             self.format_frame()
    #             --results = model.predict(self.frame, stream=True, verbose=False)
    #             cv2.line(self.frame, (self.middle, 720), (self.middle, 0), (0, 255, 0), 3)

    #             for r in results:
    #                 boxes = r.boxes

    #                 for box in boxes:
    #                     x1, y1, x2, y2 = box.xyxy[0]
    #                     x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    #                     confidence = math.ceil((box.conf[0] * 100)) / 100
    #                     cls = int(box.cls[0])

    #                     if confidence >= 0.3 and cls == 0:

    #                         cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
    #                         cv2.circle(self.frame,(int(x1 + (x2-x1)*0.5), int(y1 + (y2-y1)*0.5)), 5, (0,0,255), -1)
                            
    #                         cls = int(box.cls[0])
    #                         org = [x1, y1]
    #                         distance = self.get_distance(y1, y2)
    #                         self.get_rotation(x1, x2)
    #                         if self.get_rotation(x1, x2) == "Center":
    #                             self.get_walk(y1, y2)

    #                         cv2.putText(self.frame,
    #                                     f"{--classNames[cls]} C: {confidence} D: {distance:.2f}m dmid: {int((x1 + (x2-x1)*0.5) - self.middle)}",
    #                                     org, self.font, self.fontScale, self.color, self.thickness)

    #             if self.frame is not None:
    #                 cv2.imshow("video0", self.frame)
    #             if cv2.waitKey(2) & 0xFF == ord('q'):
    #                 break
    #         self.cap.release()
    #         cv2.destroyAllWindows()

cam = camera(1, model_tensorflow())
cam.demo_tensorflow()
