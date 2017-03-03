""" Angell Owen 
    Last Update - Mar 2017
    Photography Backup Device
    backup.py - main app used to control program 
"""

import time
import sys
import lcd_d
import button
import usb
import os #used to check if path exists
import fnmatch #file name match
import threading
import message_thread
import subprocess
import random
import string 

# define storage devices and mount points
STORAGE_DEV = "/dev/sda1"
STORAGE_MOUNT_POINT= "/media/storage"
CARD_DEV = "/dev/sdb1"
CARD_MOUNT_POINT = "/media/card"
BUTTON_YES = 1
BUTTON_NO = 2

def id_generator(size=6, char=string.ascii_uppercase + string.digits):
    """ generate a random character ID string """
    return ''.join(random.choice(char) for _ in range(size))

def checkFile(device):
    """ check if file exists """
    while not os.path.exists(device):
        time.sleep(1)
    return True
    
def shutdownDev():
    print("Device is shutting down")
    subprocess.call(["shutdown","-h","now"])
    time.sleep(5)
    sys.exit()
    
def confirmStorage(device, message):
    """ confirm storage from user, prompts to LCD screen"""
    
    usbName = usb.get_vendor(device) + " " + usb.get_model_name(device)
    
    lcd_d.lcd_string(" ",lcd_d.LCD_LINE_1)
    lcd_d.lcd_string(">yes         >no",lcd_d.LCD_LINE_2)
    
    scroll = message_thread.scrollThread(message, usbName)
    scroll.start()
    if (button.get_press() == BUTTON_NO):
        scroll.stopit()
        lcd_d.lcd_string("             >NO",lcd_d.LCD_LINE_2)
        scroll.join()
        lcd_d.lcd_string("",lcd_d.LCD_LINE_1)
        return False
    else:
        scroll.stopit()
        lcd_d.lcd_string(">YES",lcd_d.LCD_LINE_2)
        scroll.join()
        lcd_d.lcd_string("",lcd_d.LCD_LINE_1)
        return True
        
def storageError():
    lcd_d.lcd_string("Error, please",lcd_d.LCD_LINE_1)
    lcd_d.lcd_string("restart device",lcd_d.LCD_LINE_2)
    shutdownDev()
    

def main():
    #welcome user on lcd screen
    lcd_d.lcd_init()
    
    #check if storage is plugged in
    lcd_d.lcd_string("Plug in usb",lcd_d.LCD_LINE_1)
    lcd_d.lcd_string("backup device",lcd_d.LCD_LINE_2)
    time.sleep(1)
    
    #wait until device is inserted
    checkFile(STORAGE_DEV)
    
    #get user conf for usb
    message = "Backup to device: "
    if not confirmStorage(STORAGE_DEV, message):
        storageError()

    #mount storage
    backupMountPoint = usb.mount_partition(STORAGE_DEV)
    
    #check if card in inserted
    lcd_d.lcd_string("Plug in sd card",lcd_d.LCD_LINE_1)
    lcd_d.lcd_string("to back up",lcd_d.LCD_LINE_2)
    time.sleep(1)
    
    #wait until device is inserted
    checkFile(CARD_DEV)
    
    #get user conf for card
    message = "Copy from device: "
    if not confirmStorage(CARD_DEV, message):
        storageError()
    
    #mount storage
    cardMountPoint = usb.mount_partition(CARD_DEV)
    
    #get card info to use as directory name
    uid_path = cardMountPoint + "/" + "CARD_ID"
    card_id = None
    
    #check for CARD_ID file
    if os.path.exists(uid_path):
        with open(uid_path,"r") as uid_file:
            card_id = uid_file.read().replace('\n','')

    #generate new card id if not found
    if not card_id:
        #generate uid
        card_id = id_generator()
        #write uid to file on card
        with open(uid_path,"w+") as uid_file:
            uid_file.write("{}".format(card_id))
    
    backUpPath = backupMountPoint + "/" + card_id
    
    #display message that backup is in progress
    lcd_d.lcd_string("",lcd_d.LCD_LINE_2)
    message1 = "Backup"
    message2 = "In progress"
    scroll = message_thread.scrollThread(message1, message2)
    scroll.start()
    
    #use rsyn to back up files
    subprocess.call(["rsync", "-avhP", cardMountPoint+"/", backUpPath])
    scroll.stopit()
    scroll.join()
    
    lcd_d.lcd_string("Backup Complete",lcd_d.LCD_LINE_1)
    lcd_d.lcd_string("Shutdown device",lcd_d.LCD_LINE_2)
    shutdownDev()

    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_d.lcd_byte(0x01, lcd_d.LCD_CMD)
