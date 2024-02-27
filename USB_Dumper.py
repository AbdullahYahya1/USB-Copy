import os
import shutil
import time
import win32api
import win32file

SAVE_DIR = 'C:/usbCopy'  # Directory where USB contents will be saved

def is_removable_drive(drive):
    try:
        drive_type = win32file.GetDriveType(drive)
        # DRIVE_REMOVABLE refers to removable drives (e.g., USB flash drives)
        return drive_type == win32file.DRIVE_REMOVABLE
    except Exception as e:
        print(f"Error checking drive type for {drive}: {e}")
        return False
def find_removable_drives():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]  # Split the string and remove the last empty item
    return [drive for drive in drives if is_removable_drive(drive)]

def copy_usb_contents(usb_drive, save_dir):
    target_dir = os.path.join(save_dir, os.path.basename(usb_drive.strip(":/")))
    if os.path.exists(target_dir):
        print(f"Deleting existing directory: {target_dir}")
        shutil.rmtree(target_dir)
    print(f"Copying contents from {usb_drive} to {target_dir}...")
    shutil.copytree(usb_drive, target_dir)
    print("Copy completed.")

def monitor_usb_drives():
    known_drives = set()
    while True:
        current_drives = set(find_removable_drives())
        new_drives = current_drives - known_drives
        if new_drives:
            for drive in new_drives:
                print(f"New USB drive detected: {drive}")
                try:
                    copy_usb_contents(drive, SAVE_DIR)
                except Exception as e:
                    print(f"Error copying contents from {drive}: {e}")
            known_drives = current_drives
        else:
            print("No new USB detected, sleeping...")
        time.sleep(5)  # Check every 5 seconds
if __name__ == '__main__':
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    monitor_usb_drives()
