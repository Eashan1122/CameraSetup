'''
Author: Eashan Maurya
Date: 09/08/2024
'''

from cv2 import VideoCapture, imwrite, imread, IMREAD_GRAYSCALE, ORB_create, BFMatcher, NORM_HAMMING
from os import getcwd, listdir, remove
from time import sleep


directory = getcwd()
seconds = 0
compared = None

config_file = open(f"{directory}/config.txt", "r")
camera = config_file.readlines()[9]
config_file.close()
camera_num = camera.replace("camera_num = ", "")

def take_photo():
    # Initialize the camera
    camera = VideoCapture(int(camera_num))
    # Capture an image
    ret, frame = camera.read()

    # Save the image to a file
    name = choose_name()
    imwrite(name, frame)

    # Release the camera
    camera.release()

def check_files_exist(directory_path: str, file_names: list):
    """
    Checks if the specified files exist in the given directory.

    :param directory_path: Path to the directory to search in.
    :param file_names: List of file names to check for.
    :return: Dictionary with file names as keys and boolean values indicating their existence.
    """
    existing_files = listdir(directory_path)
    results = {}
    for file_name in file_names:
        if file_name in existing_files:
            results[file_name] = True
        else:
            results[file_name] = False
    return results

def choose_name():
    result = check_files_exist(directory_path = directory, file_names = ["test.png"])
    if result["test.png"] == True:
        return "check.png"
    else:
        return "test.png"

def comparision():
    # Load the two RGB images in grayscale
    image1 = imread('test.png', IMREAD_GRAYSCALE)
    image2 = imread('check.png', IMREAD_GRAYSCALE)

    # Initialize ORB detector
    orb = ORB_create()

    # Find keypoints and descriptors with ORB
    _, descriptors1 = orb.detectAndCompute(image1, None)
    _, descriptors2 = orb.detectAndCompute(image2, None)

    # Create BFMatcher object
    bf = BFMatcher(NORM_HAMMING, crossCheck=True)

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
    seconds += 1
    if seconds == 10:
        compared = False if compared == True or compared == None else True
        take_photo()
        print("Image taken!!!")
        seconds = 0
        if compared:
            comparison()
            remove("check.png")
            remove("test.png")
            
