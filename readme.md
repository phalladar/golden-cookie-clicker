# Automating Cookie Clicker using AI

## Introduction

This repository contains the code to automate the popular idle game, Cookie Clicker, using AI techniques. With this code, you'll be able to automatically detect and click the golden cookies that appear on the screen, allowing you to progress in the game without having to constantly check for them.

## Requirements

- Python 3.x
- OpenCV
- pywinauto
- Numpy
- PIL
- Re
- Win32api

## Usage

1. Make sure all the required modules are installed
2. Clone this repository to your local machine
3. Run the script `screenshot.py` 
4. Make sure the game window is open and visible on the screen
5. The script will automatically detect and click on the golden cookie every 1 second
6. If the script is unable to detect the game window, adjust the regex in the `get_cookie_clicker_screenshot` function

## Notes

- The vast majority of this code, including this readme, was written using ChatGTP by OpenAI. 
- The script uses the openCV library to detect the golden cookie in the game window. You can adjust the threshold value in the `prepare_reference_image` function to improve detection.
- The script uses pywinauto library to simulate mouse clicks. You can adjust the sleep time between clicks in the main loop.

## Licensing

This code is licensed under the [MIT License](LICENSE). Feel free to use, modify and distribute it as you like.