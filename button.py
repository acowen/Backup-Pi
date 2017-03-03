""" Angell Owen 
    Last Update - Mar 2017
    Photography Backup Device
    button.py - used to get input from user from hardwired buttons when needed.
"""

import RPi.GPIO as GPIO
import time

def get_press():
    """Returns the button pressed as an int 1 or 2 
    GPIO input 17 = Button 2 
    GPIO input 18 = button 1
    """
       
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    x = 0
    y = 0
    
    while True: 
        input_state = GPIO.input(18)
        input_state2 = GPIO.input(17)

        if input_state2 == False:
            print('button 2 pressed')
            return 2

        if input_state == False:
            print('button 1 pressed')
            return 1

        time.sleep(.1)
