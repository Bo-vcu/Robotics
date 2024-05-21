import cv2
from skimage.metrics import structural_similarity as ssim
import os


def compare_images(imageA_path, imageB_path):
    # Load the two images
    imageA = cv2.imread(imageA_path)
    imageB = cv2.imread(imageB_path)

    # Extract base names of the files (without directories and extensions)
    baseA = os.path.basename(imageA_path)
    baseB = os.path.basename(imageB_path)
    nameA = os.path.splitext(baseA)[0]
    nameB = os.path.splitext(baseB)[0]

    # Convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # Compute the Structural Similarity Index (SSI) between the two images
    (score, diff) = ssim(grayA, grayB, full=True)
    print(f"SSIM: {score}")

    # The diff image contains the actual differences between the two images.
    # Convert the diff image to uint8 format for further processing
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image to find regions that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Find contours (regions of differences)
    contours, _ = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw bounding boxes around the differing regions on the original images
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Save the difference image
    diff_filename = f"diff_{nameA}_{nameB}.png"
    cv2.imwrite(diff_filename, diff)
    print(f"Difference image saved as: {diff_filename}")

    # Display the images with differences highlighted
    cv2.imshow("Original Image A", imageA)
    cv2.imshow("Original Image B", imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Paths to the two images to be compared
imageA_path = "kitty.jpeg"
imageB_path = "editedkitty.jpeg"

# Compare the images
compare_images(imageA_path, imageB_path)
