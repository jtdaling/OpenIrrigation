#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""connectioncheck.py: script that runs every 5 minutes to check if the WLAN0 connection is still alive. Weak signals can cause WLAN0 connection to break permanently"""


__author__ = "Jantinus Daling"
__license__ = "GNU GENERAL PUBLIC LICENSE"
__version__ = "version 3"

import urllib2
import os
import time as t


def internet_on():
    for timeout in [1]:
        try:
            response=urllib2.urlopen('https://openweathermap.org/',timeout=timeout)
            #return True
            print("internet connection ok")
            break;
        except urllib2.URLError as err: pass
        #return False
        print("no internet connection")
        os.system("ifconfig wlan0 down")
        t.sleep(1)
        os.system("ifconfig wlan0 up")
        t.sleep(30)

internet_on()
