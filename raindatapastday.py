#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 16:59:17 2018

@author: jantinus
"""

#This script is used to add the collect raindata from the past day to irrigation.db
# The script runs at 4 am and provides yesterday's raindata for irrigation amount calculations

import os
import sqlite3
import linecache
import urllib
import json

# Fixed parameters
location = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 126).rstrip()
openWeatherKey = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 135).rstrip()
openWeatherURL = 'http://api.openweathermap.org/data/2.5/weather?id='+location+'&appid='+openWeatherKey+''
irrigationneeded = 0



# Calculate date and time information
from datetime import *
currentweeknumber1 = datetime.today()
currentweeknumber = currentweeknumber1.strftime("%U")

lastsevendays = float(currentweeknumber)
last2weeks = float(currentweeknumber) - 1
last3weeks = float(currentweeknumber) - 2
last4weeks = float(currentweeknumber) - 3
lastyear = float(currentweeknumber) - 51

import datetime
# current year for database usage
currentyear1 = datetime.datetime.now()
currentyear = currentyear1.year
currentday = currentyear1.day
yesterday = currentyear1.day - 1

# count the days the script has been running
conn = sqlite3.connect('/opt/OpenIrrigation/raindata.db')
c = conn.cursor()

# rainfall yesterday
c.execute("SELECT sum(RainPastHour) FROM 'PrecepitationData' WHERE CurrentWeekNumber=? AND CurrentDay=?", [lastsevendays,yesterday])
rainfallyesterday = c.fetchone()[0]
try:
    rainfallyesterday = 0
except KeyError:
    rainfallyesterday = 0

# Create a start time for database entry
ScriptStartTime = datetime.datetime.now().strftime("%H:%M")
# unique ID for database
DatabaseId = 0
irrigationamount = 0

# get MinMax temperature forecast
weatherdata = urllib.urlopen(openWeatherURL)
data = json.loads(weatherdata.read())

# max temperature today
MaxT = int(data['main']['temp_max'] - 272.15)
# min temperature today
MinT = int(data['main']['temp_min'] - 272.15)

avgtemp = (MinT + MaxT) / 2

# Connect to the database
conn = sqlite3.connect('/opt/OpenIrrigation/irrigation.db')
c = conn.cursor()
def create_table():
	c.execute(
		'CREATE TABLE IF NOT EXISTS IrrigationResults(Id REAL, CurrentYear REAL, CurrentWeekNumber REAL, CurrentDay REAL, Time REAL, IrrigationNeeded, IrrigationAmount REAL, AvgTemp REAL, TotalRainFall REAL)')
	c.execute('''INSERT INTO IrrigationResults(Id, CurrentYear, CurrentWeekNumber,CurrentDay, Time, IrrigationNeeded, IrrigationAmount, AvgTemp, TotalRainFall)
	VALUES(?,?,?,?,?,?,?,?,?)''', (DatabaseId, currentyear, currentweeknumber, currentday, ScriptStartTime, irrigationneeded, irrigationamount, avgtemp, rainfallyesterday))
	print('Database updated')
	conn.commit()
	c.close()
	conn.close()
create_table()

exit()
