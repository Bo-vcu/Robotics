import cv2
import numpy as np

# Load pre-trained person detection model
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Initialize optical flow parameters
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Initialize variables for optical flow
old_frame = None
old_gray = None
p0 = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect people in the frame
    rects, _ = hog.detectMultiScale(gray, winStride=(4, 4), padding=(8, 8), scale=1.05)
    
    # Draw bounding boxes around detected people
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Use optical flow to track movement
        if old_gray is not None:
            p1, status, err = cv2.calcOpticalFlowPyrLK(old_gray, gray, p0, None, **lk_params)
            if p1 is not None:
                # Compute vector of movement
                movement_vector = np.mean(p1 - p0, axis=0)
                print("Movement Vector:", movement_vector)
        
        # Update previous frame and points for optical flow
        old_gray = gray.copy()
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7))

    # Display the result
    cv2.imshow('Person Detection and Movement Tracking', frame)
    
    # Exit if 'Esc' key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

# Release video capture
cap.release()
cv2.destroyAllWindows()
