'''
Author: Eashan Maurya
Date: 09/08/2024
'''

import cv2
import os
import time


directory = os.getcwd()
TimeS = 0
comcheck = 0

config_file = open(f"{directory}/config.txt", "r")
setting = config_file.readlines()
cameranum = setting[9].replace("camera_num = ", "")

def takePhoto():
    # Initialize the camera
    camera = cv2.VideoCapture(int(cameranum))
    # Capture an image
    ret, frame = camera.read()

    # Save the image to a file
    name = NameSet()
    cv2.imwrite(name, frame)

    # Release the camera
    camera.release()

def check_files_exist(directory_path, file_name):
    """
    Checks if the specified files exist in the given directory.

    :param directory_path: Path to the directory to search in.
    :param file_names: List of file names to check for.
    :return: Dictionary with file names as keys and boolean values indicating their existence.
    """
    existing_files = os.listdir(directory_path)
    
    if file_name in existing_files:
        return True
    else:
        return False

def NameSet():
    result = check_files_exist(directory_path= directory, file_name= "test.png")
    if result == True:
        return "check.png"
    else:
        return "test.png"

def Comparision():
    # Load the two RGB images in grayscale
    image1 = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread('check.png', cv2.IMREAD_GRAYSCALE)

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Find keypoints and descriptors with ORB
    keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2, None)

    # Create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(descriptors1, descriptors2)

    # Sort matches by distance
    matches = sorted(matches, key = lambda x:x.distance)

    print(f"Number of good matches: {len(matches)}")
    if len(matches) > 200:
        print("There is no change...")
    elif len(matches) > 0 and len(matches) < 200:
        print("There is change...")

while True:
    time.sleep(1)
    TimeS += 1
    comcheck += 1
    if TimeS == 10:
        takePhoto()
        print("Image taken!!!")
        TimeS = 0
        if comcheck == 20:
            Comparision()
            os.remove("check.png")
            os.remove("test.png")
            comcheck = 0
