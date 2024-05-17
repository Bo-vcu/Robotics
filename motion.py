import cv2

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Create background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    
    # Apply background subtraction
    fgmask = fgbg.apply(frame)
    
    # Apply thresholding
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw bounding boxes around motion blobs
    for contour in contours:
        if cv2.contourArea(contour) < 500:  # Adjust the threshold area as needed
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the result
    cv2.imshow('Motion Detection', frame)
    
    # Check for 'Esc' key press
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 is the ASCII code for 'Esc'
        break

# Release video capture
cap.release()
cv2.destroyAllWindows()
