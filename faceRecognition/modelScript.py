import cv2
import os
import numpy as np

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Train recognizer model for a specific person
def train_model(person_name, images_folder, models_folder):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    images = []
    labels = []
    for image_file in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_file)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        images.append(img)
        labels.append(1)  # Label is always 1 for this person
    recognizer.train(images, np.array(labels))
    os.makedirs(models_folder, exist_ok=True)  # Create models folder if it doesn't exist
    recognizer.save(os.path.join(models_folder, f"{person_name}"))

# Main function
def main():
    data_dir = 'data'  # Directory containing folders of images of known individuals
    models_folder = 'models'  # Folder to save trained models
    
    # Get the name of the person folder
    person_name = input("Enter the name of the person folder: ")
    
    # Ensure the specified folder exists in the 'data' directory
    person_folder = os.path.join(data_dir, person_name)
    if not os.path.isdir(person_folder):
        print("Error: Specified folder does not exist.")
        return
    
    train_model(person_name, person_folder, models_folder)
    print("Model trained successfully!")

if __name__ == "__main__":
    main()
