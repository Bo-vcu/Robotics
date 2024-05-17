import cv2
import os
import numpy as np

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load pre-trained face recognition models
recognizer_models = {}

def load_recognizer_models(models_dir):
    for model_file in os.listdir(models_dir):
        person_name = model_file.split('.')[0]
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(os.path.join(models_dir, model_file))
        recognizer_models[person_name] = recognizer

# Function to recognize faces
def recognize_faces(frame, gray_frame):
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y+h, x:x+w]
        label, confidence = predict_person(roi_gray)
        print(confidence)
        if confidence < 100:  # Recognized face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        else:  # Unknown face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, 'Unknown', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

# Function to predict person using all recognizer models
def predict_person(face):
    min_confidence = float('inf')
    min_label = "Unknown"
    for person_name, recognizer in recognizer_models.items():
        label, confidence = recognizer.predict(face)
        if confidence < min_confidence:
            min_confidence = confidence
            min_label = person_name
    return min_label, min_confidence

# Main function
def main():
    models_dir = 'models'  # Directory containing models for each person
    
    load_recognizer_models(models_dir)  # Load recognizer models
    
    cap = cv2.VideoCapture(0)  # Access the webcam
    while True:
        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        recognize_faces(frame, gray_frame)
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
