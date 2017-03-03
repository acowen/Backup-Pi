""" Angell Owen 
    Last Update - Mar 2017
    Photography Backup Device
    usb.py - Used to mount USB and SD card and get information on them. 
"""

import os

def get_device_name(device):
    """returns decive name from /dev. ex. /dev/sda1 returns sda1"""
    return os.path.basename(device)
    
def get_parent_device(device):
    """returns the name of the parent drive. ex: sda1 returns sda"""
    return os.path.basename(device)[:3]
    
def get_parent_block_path(device):
    return "/sys/block/%s" % get_parent_device(device)

def get_vendor(device):
    """" returns the vendor name of the parent drive"""
    path = get_parent_block_path(device) + "/device/vendor"
    
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    
    return None

def get_model_name(device):
    """returns the model name from the parent device"""
    path = get_parent_block_path(device) + "/device/model"
    
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return None

def get_media_path(device):
    """gets the name of the path that device is mounted """
    return "/media/" + get_device_name(device)

def is_mounted(device):
    """ checks if device is mounted """
    return os.path.ismount(get_media_path(device))

def mount_partition(partition):
    """mounts the partition /dev/* """
    mediaPath = get_media_path(partition)
    if not is_mounted(mediaPath):
        os.system("mkdir -p " + mediaPath)
        os.system("mount %s %s -o umask=000" % (partition, mediaPath))
    return mediaPath

def unmount_patition(partition):
    """unmounts the partition""" 
    path = get_media_path(partition)
    if is_mounted(path):
        os.system("umount " + path)
        
