# -*- coding: utf-8 -*-
import base64
import os
import random
import time
import shutil
import stat
import tkinter
from tkinter import filedialog
# Assuming 'img' variable is defined elsewhere or you have an alternative approach for the icon.

USB = 'F:'  # Initial USB directory, set to F: for testing
SAVE = 'C:/usbCopy'  # Default save directory
OLD = []  # To store file directory for detecting changes in USB files
drive_status = {chr(65 + i): 0 for i in range(26)}  # Using dictionary comprehension for A-Z drives

# Function to copy USB contents
def usb_walker():
    global SAVE, USB
    if os.path.exists(SAVE):
        print('Deleting existing file!')
        try:
            os.chmod(SAVE, stat.S_IREAD | stat.S_IWRITE)
            shutil.rmtree(SAVE)
        except Exception as e:
            print(e)
            SAVE += 'NewFile' + str(random.random() * 10)

    print('FileName ' + SAVE)
    print('Copying...')

    shutil.copytree(USB, SAVE)  # "Life is short, use Python"

# Check if USB content has changed
def get_usb():
    global OLD
    NEW = os.listdir(USB)
    if len(NEW) == len(OLD):
        print("USB content has not changed")
        return 0
    else:
        OLD = NEW
        return 1

# Check if USB is present and copy its contents
def usb_copy():
    global USB
    for i in range(26):
        name = chr(i + ord('A')) + ':'
        print(name)
        if os.path.exists(name):
            drive_status[chr(i + ord('A'))] = 1
            print('Drive ' + chr(i + ord('A')) + ' exists')

    while True:
        for i in range(26):
            name = chr(i + ord('A')) + ':'
            if not os.path.exists(name):
                drive_status[chr(i + ord('A'))] = 0
            if os.path.exists(name) and drive_status[chr(i + ord('A'))] == 0:
                USB = name
                print("USB detected")
                if get_usb():
                    try:
                        usb_walker()
                    except Exception as e:
                        print(e)

        print("No USB detected, sleeping")
        time.sleep(1)
        print("Waking up")

# GUI to change save directory
def choose_dir():
    global SAVE
    SAVE = filedialog.askdirectory(initialdir="/", title='Pick a directory') + '/usbCopy'
    print('Save in ' + SAVE)

# Start button action
def click_button():
    root.withdraw()  # Hide the main window
    usb_copy()

if __name__ == '__main__':
    root = tkinter.Tk()
    usb_copy()