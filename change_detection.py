import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
ret, frame = cap.read()

# Initialize the average frame with the same type and size as the first frame
average1 = np.float32(frame)

# Define a threshold for detecting significant changes
change_threshold = 10000000

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam")
        break

    cv.accumulateWeighted(frame, average1, 0.01)
    frameDelta = cv.absdiff(frame, cv.convertScaleAbs(average1))

    change_sum = np.sum(frameDelta)

    if change_sum > change_threshold:
        print("Significant change detected!")

    cv.imshow('Main video frame', cv.resize(frame, (600, 500)))
    cv.imshow('Change in foreground', cv.resize(frameDelta, (600, 500)))

    # Break the loop if the 'ESC' key is pressed
    if cv.waitKey(33) == 27:
        break

# Release the capture and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
