import cv2
from ultralytics import YOLO
import math 

model = YOLO('best.pt') 
cap = cv2.VideoCapture(0)
cap.set(3, 1600)
cap.set(4, 1200)


while True:
    success, img = cap.read()
    results = model(img, stream=True)

  
    for r in results:
        boxes = r.boxes

        for box in boxes:
           
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

            confidence = math.ceil((box.conf[0]*100))/100

            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, "Person " + str(confidence), org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
   