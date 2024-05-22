import cv2
import numpy as np
from matplotlib import pyplot as plt
import os


def compare_images(image1_path, image2_path):
    # Load the images
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Initialize the ORB detector
    orb = cv2.ORB_create()

    # Find keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Initialize the brute force matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw the top matches
    img_matches = cv2.drawMatches(
        img1,
        kp1,
        img2,
        kp2,
        matches[:10],
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )

    # Display the matches
    plt.figure(figsize=(20, 10))
    plt.imshow(img_matches)
    plt.title("Top 10 matches")
    plt.show()

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = kp1[match.queryIdx].pt
        points2[i, :] = kp2[match.trainIdx].pt

    # Find the homography matrix
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use the homography matrix to transform the points from img1 to img2
    height, width = img2.shape
    im1_reg = cv2.warpPerspective(img1, h, (width, height))

    # Save the aligned image
    img1_name = os.path.splitext(os.path.basename(image1_path))[0]
    img2_name = os.path.splitext(os.path.basename(image2_path))[0]
    aligned_image_path = f"match_{img1_name}_{img2_name}.jpg"
    cv2.imwrite(aligned_image_path, im1_reg)

    # Display the aligned image
    plt.figure(figsize=(10, 10))
    plt.imshow(im1_reg, cmap="gray")
    plt.title("Aligned Image")
    plt.show()

    # Calculate difference image
    diff = cv2.absdiff(img2, im1_reg)

    # Threshold the difference image
    _, diff_thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

    # Display the difference image
    plt.figure(figsize=(10, 10))
    plt.imshow(diff_thresh, cmap="gray")
    plt.title("Difference Image")
    plt.show()


# Example usage
compare_images("kitty.jpeg", "editedkitty.jpeg")
