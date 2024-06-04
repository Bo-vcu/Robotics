import cv2
import os
from ultralytics import YOLO
import math
import numpy as np

print(cv2.getBuildInformation())

class output:
    def __init__(self):
        pass
    def send(self, action):
        pass
class output_cmd(output):
    def __init__(self):
        pass
    def send(self, action):
        print(action)
class output_mqtt(output):
    def __init__(self):
        pass
    def send(self, action):
        pass
    

class model:
    def __init__(self):
        pass
    def detect_objects(self, frame):
        pass
    def get_results(self, frame):
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
    
    def get_results(self, frame):
        objects = self.detect_objects(frame)
        rows, cols, _ = frame.shape
        results = []
        for i in range(objects.shape[2]):
                selected = objects[0, 0, i]
        
                classId = int(selected[1])
                score = float(selected[2])

                x1 = int(selected[3] * cols)
                y1 = int(selected[4] * rows)
                w = int(selected[5] * cols - x1)
                h = int(selected[6] * rows - y1)
                x2 = x1 + w
                y2 = y1 + h
                if score > 0.25 and classId == 1:
                    results.append([x1, x2, y1, y2])
        return results
   
class model_ultralytics(model):
    def __init__(self):
        self.model_ultralytics = YOLO('yolov8n.pt')
        self.classNames = self.model_ultralytics.names

    def detect_objects(self, frame):
        return self.model_ultralytics.predict(frame, stream=True, verbose=False)
    
    def get_results(self, frame):
        objects = self.detect_objects(frame)
        results = []
        for r in objects:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                confidence = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])

                if confidence >= 0.3 and cls == 0:
                    results.append([x1, x2, y1, y2])
        return results
   

class camera:
    def __init__(self, cam_id=0):
        self.width = 1280
        self.middle = int(self.width*0.5)
        self.cam_id = cam_id
        self.height = 720
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 0.5
        self.color = (255, 0, 0)
        self.thickness = 2
        self.get_img()
        
    def get_frame(self):
        self.ret, self.frame = self.cap.read()
        self.frame = cv2.resize(self.frame, (self.width, self.height))
        self.frame = cv2.flip(self.frame, -1)
        return self.frame

    def get_img(self):
        self.cap = cv2.VideoCapture(self.cam_id)

    def release(self):
        self.cap.release()

class unitree_camera(camera):
    def __init__(self, cam_id=1):
        super().__init__(cam_id)
        self.width = 1280
        self.height = 720
        self.cam_id = cam_id
        self.get_img()

    def get_img(self):
        IpLastSegment = "162"
        udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port="
        udpPORT = [9201, 9202, 9203, 9204, 9205]
        udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
        udpSendIntegratedPipe_0 = udpstrPrevData + str(udpPORT[self.cam_id - 1]) + udpstrBehindData
        print(udpSendIntegratedPipe_0)
        self.cap = cv2.VideoCapture(udpSendIntegratedPipe_0)

class algorithm:
    def __init__(self, model, camera, output):
        self.model = model
        self.camera = camera
        self.output = output

    def get_distance(self, y1, y2):
        h = y2 - y1
        focal_length = 615
        KNOWN_HEIGHT = 1.8
        distance = (KNOWN_HEIGHT * focal_length) / h
        return distance
    
    def get_action(self, x1, x2, distance, middle=640):
        if int((x1 + (x2-x1)*0.5) - middle) < -100*middle/640:
            return "Left"
        elif int((x1 + (x2-x1)*0.5) - middle) > 100*middle/640:
            return "Right"
        else:
            return self.get_walk(distance)         
    
    def get_walk(self, distance):
        if distance < 3:
            return "Stop"
        else:
            return "Walk "

    def demo(self):
        while True:
            frame = self.camera.get_frame()
            results = self.model.get_results(frame)
            cv2.line(frame, (self.camera.middle, 720), (self.camera.middle, 0), (0, 255, 0), 3)

            for result in results:
                x1, x2, y1, y2 = result
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.circle(frame,(int(x1 + (x2-x1)*0.5), 
                                        int(y1 + (y2-y1)*0.5)), 5, (0,0,255), -1)
                
                org = [x1, y1]
                distance = self.get_distance(y1, y2)
                self.output.send(self.get_action(x1, x2, distance))

                cv2.putText(frame,
                            f"D: {distance:.2f}m dmid: {int((x1 + (x2-x1)*0.5) - self.camera.middle)}",
                            org, self.camera.font, self.camera.fontScale, self.camera.color, self.camera.thickness)

            if frame is not None:
                cv2.imshow("video0", frame)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        self.camera.release()
        cv2.destroyAllWindows()

cam = unitree_camera(1)
mod = model_tensorflow()
out = output_cmd()
alg = algorithm(mod, cam, out)
alg.demo()
