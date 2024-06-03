import cv2
from ultralytics import YOLO
import math
import numpy as np

print(cv2.getBuildInformation())

class camera:
    def __init__(self, cam_id=None, width=640, height=480):
        self.width = width
        self.cam_id = cam_id
        self.height = height

    def get_img(self):
        IpLastSegment = "162"
        cam = self.cam_id
        udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port="
        udpPORT = [9201, 9202, 9203, 9204, 9205]
        udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
        udpSendIntegratedPipe_0 = udpstrPrevData + str(udpPORT[cam - 1]) + udpstrBehindData
        print(udpSendIntegratedPipe_0)

        self.cap = cv2.VideoCapture(udpSendIntegratedPipe_0)

    def demo(self):
        self.get_img()
        model = YOLO('yolov8n.pt')
        classNames = model.names

        # Define the known height of a person in meters (average height)
        KNOWN_HEIGHT = 1.7
        focal_length = 615  # This should be calibrated for your specific camera

        while True:
            self.ret, self.frame = self.cap.read()
            self.frame = cv2.resize(self.frame, (self.width, self.height))
            if self.cam_id == 1:
                self.frame = cv2.flip(self.frame, -1)
                results = model.predict(self.frame, stream=True, verbose=False)

                for r in results:
                    boxes = r.boxes

                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        confidence = math.ceil((box.conf[0] * 100)) / 100
                        cls = int(box.cls[0])
                        if confidence >= 0.3 and cls == 0:  # Only consider the 'person' class
                            cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

                            # Calculate the distance
                            h = y2 - y1
                            distance = (KNOWN_HEIGHT * focal_length) / h

                            cls = int(box.cls[0])
                            org = [x1, y1]
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            fontScale = 1
                            color = (255, 0, 0)
                            thickness = 2

                            cv2.putText(self.frame,
                                        f"{classNames[cls]} {confidence} Distance: {distance:.2f}m",
                                        org, font, fontScale, color, thickness)

            if self.frame is not None:
                cv2.imshow("video0", self.frame)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

cam = camera(1)
cam.demo()
