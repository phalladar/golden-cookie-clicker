from pywinauto import Desktop
import numpy as np
import re
from PIL import ImageGrab
from PIL import Image
import cv2
from skimage.feature import SIFT
from skimage.io import imread

THRESHOLD_VALUE = 127  # Tweak as needed


def get_cookie_clicker_screenshot():
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
            # cv2.imshow("Cookie Clicker screenshot", img)
            # cv2.waitKey(0)
            return img
    else:
        print("Cookie Clicker window not found")
        return None


def prepare_reference_image(image_path):
    img = Image.open(image_path)
    # convert the image to grayscale
    gray = img.convert('L')
    # Applying threshold to the image
    img_array = np.array(gray)
    img_array[img_array < THRESHOLD_VALUE] = 0
    img_array[img_array >= THRESHOLD_VALUE] = 255
    # Applying SIFT on the processed image
    sift = cv2.SIFT_create()
    kp, des = sift.detectAndCompute(img_array, None)
    return kp, des


def find_golden_cookie(screenshot, kp_reference, des_reference):
    sift = cv2.SIFT_create()
    # Finding keypoints and descriptor of the screenshot
    kp_screenshot, des_screenshot = sift.detectAndCompute(screenshot, None)
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L2)
    # Match descriptors.
    matches = bf.match(des_reference, des_screenshot)
    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    # cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
    plt.imshow(img3)
    plt.show()

# ------


reference_path = 'C:\\Users\\allocate\\development\\cookies\\reference.jpg'
screenshot = get_cookie_clicker_screenshot()
kp_reference, des_reference = prepare_reference_image(reference_path)
find_golden_cookie(screenshot, kp_reference, des_reference)
