Angell Owen 
Photography Backup Project 
March 2017


In order for this device to work properly it will need to be set up in Linux on a Raspberry Pi 3 running in terminal only mode on Raspbian OS.  

It will need the program Rsync to run and backup.py needs to be scheduled to run on startup. 

It is setup using a 16x2 character LCD screen using I2C protocol and two hardwired buttons on GPIO 17 and 18. 

The device prompts user to enter backup drive and SD card and confirms with user. 

It backs up the files, displays status on screen and shuts down device.
