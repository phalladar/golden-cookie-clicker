from pywinauto import Desktop
import numpy as np
import re
from PIL import ImageGrab
from PIL import Image
import cv2

THRESHOLD_VALUE = 127  # Tweak as needed
reference_path = 'C:\\Users\\allocate\\development\\cookies\\reference.png'
cheat_path = 'C:\\Users\\allocate\\development\\cookies\\cheat.jpg'
TESTING = True

def get_cookie_clicker_screenshot():
    if TESTING:
        img = Image.open(cheat_path).convert('L')
        img = np.array(img)
        ret, img = cv2.threshold(
            img, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        return img
    title_pattern = re.compile(r"^.*cookies.*Cookie Clicker.*")
    all_windows = Desktop().windows()
    for window in all_windows:
        if title_pattern.match(window.texts()[0]):
            window.set_focus()
            x, y, width, height = window.rectangle().left, window.rectangle(
            ).top, window.rectangle().width(), window.rectangle().height()
            img = ImageGrab.grab(
                bbox=(x, y, x + width, y + height)).convert('L')
            img = np.array(img)
            ret, img = cv2.threshold(
                img, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
            return img
    else:
        print("Cookie Clicker window not found")
        return None


def prepare_reference_image(image_path):
    # Open the image and convert it to grayscale
    img = Image.open(image_path).convert('L')
    # Convert the image to a numpy array and apply thresholding
    img_array = np.array(img)
    img_array[img_array < THRESHOLD_VALUE] = 0
    img_array[img_array >= THRESHOLD_VALUE] = 255
    # Create an SIFT object
    sift = cv2.SIFT_create()
    # Detect keypoints and compute their descriptors
    keypoints, descriptors = sift.detectAndCompute(img_array, None)
    # Return the keypoints and descriptors
    return keypoints, descriptors, img_array


def find_golden_cookie(screenshot, kp_reference, des_reference, img_reference):
    sift = cv2.SIFT_create()
    # Finding keypoints and descriptor of the screenshot
    kp_screenshot, des_screenshot = sift.detectAndCompute(screenshot, None)
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L2)
    # Match descriptors.
    matches = bf.match(des_reference, des_screenshot)
    # Sort the matches in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    # Draw first 10 matches.
    img_matches = cv2.drawMatches(img_reference, kp_reference, screenshot, kp_screenshot, matches[:15], None)

    cv2.imshow("Matches", img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Obtain the coordinates of the best match
    ratio = matches[0].distance / matches[1].distance
    print("Ratio = ", ratio)
    if len(matches) > 0 and ratio < 0.75:
        x, y = kp_screenshot[matches[0].trainIdx].pt
        print("Match found")
        return x, y
    else:
        print("No match found")
        return None


# ------


screenshot = get_cookie_clicker_screenshot()
kp_reference, des_reference, img_reference = prepare_reference_image(reference_path)
find_golden_cookie(screenshot, kp_reference, des_reference, img_reference)
