import os
import cv2
from ultralytics import YOLO
import math 

model = YOLO('yolov8n.pt') 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

classNames = model.names


while True:
    success, img = cap.read()
    results = model(img, stream=True)
  
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

    cv2.imshow('feed', img)
    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
   