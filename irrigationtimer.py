#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 16:59:17 2018

@author: jantinus
"""

from crontab import CronTab
import linecache
import datetime
from dateutil import tz
import time as t
import os


os.system('crontab -r')
scripTime = datetime.datetime.now()
resetTime = scripTime + datetime.timedelta(hours=24)

# get timezone
timeZone = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 142).strip()
# define time zones:
from_zone = tz.gettz('Europe/Vienna')
to_zone = tz.gettz('GMT')

# get times from gardendata.txt and caclulate intervals
sprinklertimeMorning = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 137).strip()
# define time in UTC
gmt = datetime.datetime.strptime(sprinklertimeMorning, '%H:%M')
# Tell the datetime object that it's in UTC time zone since
# datetime objects are 'naive' by default
gmt = gmt.replace(tzinfo=from_zone)
# Convert time zone
sprinklertimeMorning = gmt.astimezone(to_zone)
sprinklertimeMorning = datetime.datetime.strftime(sprinklertimeMorning, '%H:%M')

sprinklertimeEvening = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 139).strip()
# define time in UTC
gmt = datetime.datetime.strptime(sprinklertimeEvening, '%H:%M')
# Tell the datetime object that it's in UTC time zone since
# datetime objects are 'naive' by default
gmt = gmt.replace(tzinfo=from_zone)
# Convert time zone
sprinklertimeEvening = gmt.astimezone(to_zone)
sprinklertimeEvening = datetime.datetime.strftime(sprinklertimeEvening, '%H:%M')

driptimeStart = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 141).strip()
# define time in UTC
gmt = datetime.datetime.strptime(driptimeStart, '%H:%M')
# Tell the datetime object that it's in UTC time zone since
# datetime objects are 'naive' by default
gmt = gmt.replace(tzinfo=from_zone)
# Convert time zone
driptimeStart = gmt.astimezone(to_zone)
driptimeStart = datetime.datetime.strftime(driptimeStart, '%H:%M')
driptimeInterval = 2
driptime1 = driptimeStart
driptime2 = (datetime.datetime.strptime(driptime1, "%H:%M") + datetime.timedelta(hours=driptimeInterval)).strftime(
    "%H:%M")
driptime3 = (datetime.datetime.strptime(driptime2, "%H:%M") + datetime.timedelta(hours=driptimeInterval)).strftime(
    "%H:%M")
driptime4 = (datetime.datetime.strptime(driptime3, "%H:%M") + datetime.timedelta(hours=driptimeInterval)).strftime(
    "%H:%M")
driptime5 = (datetime.datetime.strptime(driptime4, "%H:%M") + datetime.timedelta(hours=driptimeInterval)).strftime(
    "%H:%M")
driptime6 = (datetime.datetime.strptime(driptime5, "%H:%M") + datetime.timedelta(hours=driptimeInterval)).strftime(
    "%H:%M")


#standardjobs
cron = CronTab(user='pi')

# restart irrigationcomputer at 02:23 every day
irrigationreboot = cron.new(command = 'reboot')
irrigationreboot.minute.on(23)
irrigationreboot.hour.on(2)

# check internet connection every 5 minutes
connectioncheck = cron.new(command = '/usr/bin/python /opt/OpenIrrigation/connectioncheck.py')
connectioncheck.minute.every(1)

# check if Balcony moisture sensor is running every minute
BalconyMoisture = cron.new(command = '/bin/sh /opt/OpenIrrigation/Balcony.sh')
BalconyMoisture.minute.every(1)

# get raindata every hour at 5 past
irrigationtimer = cron.new(command = '/usr/bin/python /opt/OpenIrrigation/cronjobController.py')
irrigationtimer.minute.on(1)

# get raindata every hour at 5 past
raindata = cron.new(command = '/usr/bin/python /opt/OpenIrrigation/raindata.py')
raindata.minute.on(5)

# add raindata past 24 hours to irrigation database
raindatapastday = cron.new(command = '/usr/bin/python /opt/OpenIrrigation/raindatapastday.py')
raindatapastday.minute.on(6)
raindatapastday.hour.on(3)

# Sprinkler in the morning
SprinklerMorning = cron.new(command = 'python /opt/OpenIrrigation/irrigationmainSprinkler.py')
SprinklerMorning.hour.on(sprinklertimeMorning[0:2])
SprinklerMorning.minute.on(sprinklertimeMorning[3:5])

# Sprinkler at evening
SprinklerEvening = cron.new(command = 'python /opt/OpenIrrigation/irrigationmainSprinkler.py')
SprinklerEvening.hour.on(sprinklertimeEvening[0:2])
SprinklerEvening.minute.on(sprinklertimeEvening[3:5])

# First drip irrigation
Drip1 = cron.new(command = 'python /opt/OpenIrrigation/irrigationmainDrip.py')
Drip1.hour.on(driptime1[0:2])
Drip1.minute.on(driptime1[3:5])

# Second drip irrigation
Drip2 = cron.new(command = 'python /opt/OpenIrrigation/irrigationmainDrip.py')
Drip2.hour.on(driptime2[0:2])
Drip2.minute.on(driptime2[3:5])

# Third drip irrigation
Drip3 = cron.new(command = 'python /opt/OpenIrrigation/irrigationmainDrip.py')
Drip3.hour.on(driptime3[0:2])
Drip3.minute.on(driptime3[3:5])

# Fourth drip irrigation
Drip4 = cron.new(command = 'python /opt/OpenIrrigation/irrigationmainDrip.py')
Drip4.hour.on(driptime4[0:2])
Drip4.minute.on(driptime4[3:5])

# Fifth drip irrigation
Drip5 = cron.new(command = 'python /opt/OpenIrrigation/irrigationmainDrip.py')
Drip5.hour.on(driptime5[0:2])
Drip5.minute.on(driptime5[3:5])

# Sixth drip irrigation
Drip6 = cron.new(command = 'python /opt/OpenIrrigation/irrigationmainDrip.py')
Drip6.hour.on(driptime6[0:2])
Drip6.minute.on(driptime6[3:5])

cron.write()

while True:
    # current time
    currenttime = datetime.datetime.now().strftime("%H:%M")
    # check if gardendata.txt has been updated
    def modification_date(filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)
    updatecheckTime = modification_date('/home/pi/.OpenIrrigation/gardendata.txt')
    if scripTime < updatecheckTime:
        break
    if scripTime > resetTime:
        break
    t.sleep(20)