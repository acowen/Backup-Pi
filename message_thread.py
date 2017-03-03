""" Angell Owen 
    Last Update - Mar 2017
    Photography Backup Device
    message_thread.py - scrolls messages on one line using multi threading
"""

import threading
import lcd_d
import time

#Multi threaded class used to scroll messages on the screen while the main app continues to process 
class scrollThread(threading.Thread):
    """ Thread to scroll two messages on 1 line until stopit is called """

    def __init__(self, message, message2):
        threading.Thread.__init__(self)
        self._stopper = threading.Event()
        self.message = message
        self.message2 = message2
        
    def run(self):
        #loop until flag stopped is set
        while (self.stopped() == False):
            
            #display first message
            lcd_d.lcd_string(self.message,lcd_d.LCD_LINE_1)
            for i in range(0,5):
                if self.stopped():
                    return
                else:
                    time.sleep(.25)
                
            #display second message
            lcd_d.lcd_string(self.message2,lcd_d.LCD_LINE_1)
            for i in range(0,5):
                if self.stopped():
                    return
                else:
                    time.sleep(.25)
            
    def stopit(self):
        """when called will set stopped"""
        self._stopper.set()

    def stopped(self):
        """returns if flag is set to stop thread"""
        return self._stopper.isSet()
