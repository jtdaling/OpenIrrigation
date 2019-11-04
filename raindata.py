#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 16:59:17 2018

@author: jantinus
"""

#This script is used to collect raindata from OpenWeaterMap
# The script runs every hour and safes the data in raindata.db

import time as t
import os
import json
import sqlite3
import linecache
import urllib

# Calculate date and time information
""" current week for database usage """
from datetime import *
currentweeknumber1 = datetime.today()
currentweeknumber = currentweeknumber1.strftime("%U")
lastsevendays = float(currentweeknumber)
pastweek = float(currentweeknumber)-1

import datetime
"""current year for database usage """
currentyear1 = datetime.datetime.now()
currentyear = currentyear1.year
currentday = currentyear1.day

""" Create a start time for database entry """
ScriptStartTime = datetime.datetime.now().strftime("%H:%M")

# Fixed parameters
""" unique ID for database """
DatabaseId = 0
location = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 126).rstrip()
openWeatherKey = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 135).rstrip()
openWeatherURL = 'http://api.openweathermap.org/data/2.5/weather?id='+location+'&appid='+openWeatherKey+''

"""get weather data from openweathermap"""
weatherdata = urllib.urlopen(openWeatherURL)
data = json.loads(weatherdata.read())

temp = int(data['main']['temp'] - 272.15)
pressure = int(data['main']['pressure'])
temp_Min = int(data['main']['temp_min'] - 272.15)
temp_Max = int(data['main']['temp_max'] - 272.15)
humidity = int(data['main']['humidity'])
wind_speed = int(data['wind']['speed'] * 3.6)
try:
    rain = int(data['rain']['1h'])
except KeyError:
    rain = 0
try:
    rain3= int(data['rain']['3h'])
except KeyError:
    rain3= 0

if rain == 0 and rain3 > 0:
    rain = rain3 * 0.33

# Add data to database
conn = sqlite3.connect('/opt/OpenIrrigation/raindata.db')
c = conn.cursor()
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS PrecepitationData(Id REAL, CurrentYear REAL, CurrentWeekNumber REAL, CurrentDay REAL, Time REAL, RainPastHour REAL,Temp REAL, Pressure REAL, Humidity REAL, WindSpeed REAL)')
	c.execute('''INSERT INTO PrecepitationData(Id, CurrentYear, CurrentWeekNumber,CurrentDay, Time, RainPastHour, Temp, Pressure, Humidity, WindSpeed)
	VALUES(?,?,?,?,?,?,?,?,?,?)''', (DatabaseId,currentyear,currentweeknumber,currentday,ScriptStartTime,rain, temp, pressure, humidity, wind_speed))
	print('Database updated')
	conn.commit()
	c.close()
	conn.close()
create_table()
os.system('/usr/bin/python /opt/OpenIrrigation/htmlgenerator.py')
exit()
