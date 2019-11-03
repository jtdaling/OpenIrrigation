#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 16:59:17 2018

@author: jantinus
"""
# For GPIO numbering see gpio.sh

#Import required modules
import time as t
import os
#import RPi.GPIO as GPIO
import sqlite3
import linecache
import math
import urllib
import urllib2
import json
from pathlib import Path

# irrigation type Sprinkler
irrigationtype = "1"
irrigation = 1


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

# reset irrigation parameter
# check if irridation.db excists
database_file = Path("/opt/OpenIrrigation/irrigation.db")
if database_file.is_file():
    '''dabase file exists'''
else:
    os.system("python /opt/OpenIrrigation/raindata.py")
    t.sleep(1)
    os.system ("python /opt/OpenIrrigation/raindatapastday.py")

#Date and time calculations for database usage
from datetime import *
currentweeknumber1 = datetime.today()
currentweeknumber = currentweeknumber1.strftime("%U")
lastsevendays = float(currentweeknumber)
pastweek = float(currentweeknumber)-1
currentdayofweek = float(datetime.today().weekday())
yesterday1 = datetime.now() - timedelta(days=1)
yesterday = float(yesterday1.strftime("%d"))

import datetime
"""current year for database usage"""
currentyear1 = datetime.datetime.now()
currentyear = currentyear1.year
currentday = currentyear1.day

"""Create a start time for database entry"""
ScriptStartTime = datetime.datetime.now().strftime("%H:%M")

#End

# reset raindata
totalrainfall = 0

# rainfall of last 24 hours
conn = sqlite3.connect('/opt/OpenIrrigation/raindata.db')
c = conn.cursor()
c.execute("SELECT sum(RainPastHour) FROM 'PrecepitationData' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
          [0, lastsevendays, currentday])
rainfalltoday = c.fetchone()[0]
if rainfalltoday is None:
    rainfalltoday = 0

if currentday == 1:
    c.execute("SELECT sum(RainPastHour) FROM 'PrecepitationData' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
              [0, lastsevendays - 1, yesterday])
    rainfallyesterday = c.fetchone()[0]
if currentdayofweek == 6:
    c.execute("SELECT sum(RainPastHour) FROM 'PrecepitationData' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
              [0, lastsevendays - 1, yesterday])
    rainfallyesterday = c.fetchone()[0]
else:
    c.execute("SELECT sum(RainPastHour) FROM 'PrecepitationData' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
              [0, lastsevendays, yesterday])
    rainfallyesterday = c.fetchone()[0]

try:
    rainfallyesterday = int(rainfallyesterday)
except TypeError:
    rainfallyesterday = 0

# Get weatherdata from OpenWeather
location = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 126).rstrip()
openWeatherKey = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 135).rstrip()
openWeatherURL = 'http://api.openweathermap.org/data/2.5/weather?id='+location+'&appid='+openWeatherKey+''

"""get weather data from openweathermap"""
weatherdata = urllib.urlopen(openWeatherURL)
data = json.loads(weatherdata.read())

''' current wind conditions'''
Wind = int(data['wind']['speed'] * 3.6)

'''Rain forecast today'''
openWeatherForecastURL = 'http://api.openweathermap.org/data/2.5/forecast?id='+location+'&appid='+openWeatherKey+''
weatherdata = urllib.urlopen(openWeatherForecastURL)
data = json.loads(weatherdata.read())

for x in range(1,9):
    cur_stamp = data['list'][x]['dt_txt']
    cur_date = cur_stamp[21:00]
    cur_hour = cur_stamp[20:30]

    try:
        rain = data['list'][x]['rain']['3h']
    except KeyError:
        rain = 0

    if x == 1:
        rain1 = rain
    if x == 2:
        rain2 = rain
    if x == 3:
        rain3 = rain
    if x == 4:
        rain4 = rain
    if x == 5:
        rain5 = rain
    if x == 6:
        rain6 = rain
    if x == 7:
        rain7 = rain
    if x == 8:
        rain8 = rain

RainForecast = int(rain1 + rain2 + rain3 + rain4 + rain5 + rain6 + rain7 + rain8)

'''temperature information next 12h'''
for x in range(0,11):
    cur_stamp = data['list'][x]['dt_txt']
    cur_date = cur_stamp[21:00]
    cur_hour = cur_stamp[20:30]

    '''max temperature next 12h'''

    try:
        temp_max = data['list'][x]['main']['temp_max']
    except KeyError:
        temp_max = 0

    if x == 0:
        temp_max1 = temp_max
    if x == 1:
        temp_max2 = temp_max
    if x == 2:
        temp_max3 = temp_max
    if x == 3:
        temp_max4 = temp_max
    if x == 4:
        temp_max5 = temp_max
    if x == 5:
        temp_max6 = temp_max
    if x == 6:
        temp_max7 = temp_max
    if x == 7:
        temp_max8 = temp_max
    if x == 8:
        temp_max9 = temp_max
    if x == 9:
        temp_max10 = temp_max
    if x == 10:
        temp_max11 = temp_max

MaxT = (max(temp_max1, temp_max2, temp_max3, temp_max4, temp_max5, temp_max6, temp_max7, temp_max8, temp_max9, temp_max10, temp_max11)- 272.15)

for x in range(0,11):
    cur_stamp = data['list'][x]['dt_txt']
    cur_date = cur_stamp[21:00]
    cur_hour = cur_stamp[20:30]

    '''min temperature next 12h'''
    try:
        temp_min = data['list'][x]['main']['temp_min']
    except KeyError:
        temp_min = 0

    if x == 0:
        temp_min1 = temp_min
    if x == 1:
        temp_min2 = temp_min
    if x == 2:
        temp_min3 = temp_min
    if x == 3:
        temp_min4 = temp_min
    if x == 4:
        temp_min5 = temp_min
    if x == 5:
        temp_min6 = temp_min
    if x == 6:
        temp_min7 = temp_min
    if x == 7:
        temp_min8 = temp_min
    if x == 8:
        temp_min9 = temp_min
    if x == 9:
        temp_min10 = temp_min
    if x == 10:
        temp_min11 = temp_min

MinT = (min(temp_min1, temp_min2, temp_min3, temp_min4, temp_min5, temp_min6, temp_min7, temp_min8, temp_min9,
            temp_min10, temp_min11) - 272.15)

avgtemp = (MinT + MaxT) / 2


# valve sequence starting with valve 1
for valvesequence in range(0,16):
    valvesequence = valvesequence + 1

    # Valve number used as ID in irrigation database
    DatabaseId = valvesequence

    # irrigation info past 3 days
    conn = sqlite3.connect('/opt/OpenIrrigation/irrigation.db')
    c = conn.cursor()

    if currentday == 1:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 1, yesterday])
        irrigationneeded1 = c.fetchone()[0]
    if currentdayofweek == 6:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 1, yesterday])
        irrigationneeded1 = c.fetchone()[0]
    else:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays, yesterday])
        irrigationneeded1 = c.fetchone()[0]

    if currentday == 2:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 1, yesterday - 1])
        irrigationneeded2 = c.fetchone()[0]
    if currentdayofweek == 0:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 1, yesterday - 1])
        irrigationneeded2 = c.fetchone()[0]
    else:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays, yesterday - 1])
        irrigationneeded2 = c.fetchone()[0]

    if currentday == 3:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 2, yesterday - 1])
        irrigationneeded3 = c.fetchone()[0]
    if currentdayofweek == 1:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 2, yesterday - 1])
        irrigationneeded3 = c.fetchone()[0]
    else:
        c.execute(
            "SELECT sum(IrrigationNeeded) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays, yesterday - 1])
        irrigationneeded3 = c.fetchone()[0]

    try:
        irrigationneeded1 = 0
    except TypeError:
        irrigationneeded1 = 0
    try:
        irrigationneeded2 = 0
    except TypeError:
        irrigationneeded2 = 0
    try:
        irrigationneeded3 = 0
    except TypeError:
        irrigationneeded3 = 0

    TotalIrrigationneeded = min(
        value for value in [irrigationneeded1, irrigationneeded2, irrigationneeded3] if value is not None)

    if currentday == 1:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 1, yesterday])
        irrigationAmount1 = c.fetchone()[0]
    if currentdayofweek == 6:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 1, yesterday])
        irrigationAmount1 = c.fetchone()[0]
    else:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays, yesterday])
        irrigationAmount1 = c.fetchone()[0]

    if currentday == 2:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 1, yesterday - 1])
        irrigationAmount2 = c.fetchone()[0]
    if currentdayofweek == 0:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 1, yesterday - 1])
        irrigationAmount2 = c.fetchone()[0]
    else:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays, yesterday - 1])
        irrigationAmount2 = c.fetchone()[0]

    if currentday == 3:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 2, yesterday - 1])
        irrigationAmount3 = c.fetchone()[0]
    if currentdayofweek == 1:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays - 2, yesterday - 1])
        irrigationAmount3 = c.fetchone()[0]
    else:
        c.execute(
            "SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
            [DatabaseId, lastsevendays, yesterday - 1])
        irrigationAmount3 = c.fetchone()[0]
    try:
        irrigationAmount1 = 0
    except TypeError:
        irrigationAmount1 = 0
    try:
        irrigationAmount2 = 0
    except TypeError:
        irrigationAmount2 = 0
    try:
        irrigationAmount3 = 0
    except TypeError:
        irrigationAmount3 = 0

    TotalIrrigationAmount = min(
        value for value in [irrigationAmount1, irrigationAmount2, irrigationAmount3] if value is not None)

    Irrigationcorrectionpast = (TotalIrrigationneeded - TotalIrrigationAmount) / 3

    try:
        Irrigationcorrectionpast = 0
    except TypeError:
        Irrigationcorrectionpast = 0

    #Data lookup in gardendata.txt
    try:
        irrigationAmount1 = 0
    except TypeError:
        irrigationAmount1 = 0

    '''Switch Position (On/Off)'''
    Switch = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', valvesequence + 103).strip()
    '''NAME'''
    Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', valvesequence + 1).strip()
    print(Name)
    ValveType = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', valvesequence + 86).strip()
    PlantName = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', valvesequence + 69).strip()
    maxwindspeed = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', valvesequence + 52).strip()
    SeasonLength = 12
    NumberOfWeeks = 52 / float(12) * SeasonLength
    irrigationoutput = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', valvesequence + 18).strip())
    IrrigationEfficiency = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', valvesequence + 35).strip())

    # get parameters from selected plant
    if PlantName != '0':
        conn = sqlite3.connect('/opt/OpenIrrigation/plantdata.db')
        c = conn.cursor()
        c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [PlantName])
        PlantId = c.fetchone()[0]
        c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
        GrowthMinT = c.fetchone()[0]
        c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
        GrowthMaxT = c.fetchone()[0]
        c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
        YearlyAmountWater = c.fetchone()[0]
    else:
        YearlyAmountWater = 0

    # Calculated water requirements
    WaterPerWeek = YearlyAmountWater / NumberOfWeeks
    WaterPerDay = WaterPerWeek / 7
    if WaterPerDay > 0:
        MaxIrrigationTime = (WaterPerDay - rainfallyesterday - RainForecast - rainfalltoday + Irrigationcorrectionpast) / float(irrigationoutput * (IrrigationEfficiency * 0.01)) * 60
    else:
        MaxIrrigationTime = 0
    GrowthOptT = (GrowthMinT + GrowthMaxT) / 2

    if valvesequence == 1:
        gpio = 'gpio4'
    if valvesequence == 2:
        gpio = 'gpio5'
    if valvesequence == 3:
        gpio = 'gpio6'
    if valvesequence == 4:
        gpio = 'gpio12'
    if valvesequence == 5:
        gpio = 'gpio13'
    if valvesequence == 6:
        gpio = 'gpio16'
    if valvesequence == 7:
        gpio = 'gpio17'
    if valvesequence == 8:
        gpio = 'gpio18'
    if valvesequence == 9:
        gpio = 'gpio19'
    if valvesequence == 10:
        gpio = 'gpio20'
    if valvesequence == 11:
        gpio = 'gpio21'
    if valvesequence == 12:
        gpio = 'gpio22'
    if valvesequence == 13:
        gpio = 'gpio23'
    if valvesequence == 14:
        gpio = 'gpio24'
    if valvesequence == 15:
        gpio = 'gpio26'
    if valvesequence == 16:
        gpio = 'gpio27'

    # check if ValveType is equal to irrigationtype that was scheduled to run
    if ValveType != irrigationtype:
        os.system("echo 0 > /sys/class/gpio/" + gpio + "/value")
        print('valvetype is not scheduled for irrigating')
        irrigation = 0

    # check if valve is switched OFF
    if Switch == '0':
        os.system("echo 0 > /sys/class/gpio/"+gpio+"/value")
        print('valve is switched off')
        irrigation = 0

    # check if valve is switched OFF
    if Switch == 'OFF':
        os.system("echo 0 > /sys/class/gpio/"+gpio+"/value")
        print('valve is switched off')
        irrigation = 0

    # check if irrigation is not required due to rain
    if MaxIrrigationTime < 0:
        irrigationneeded = 0
        print('Irrigation canceled due to rain')
        os.system("echo 0 > /sys/class/gpio/"+gpio+"/value")
        # Give a 0 value for no irrigation in database
        StartTime = 0
        EndTime = 0
        # Connect to the database
        conn = sqlite3.connect('irrigation.db')
        c = conn.cursor()
        # Create Database entry for irrigation time
        irrigationtime = float(EndTime) - int(StartTime)
        irrigationamount = round((irrigationtime * float(irrigationoutput) / 3600), 1)
        # Connect to the database
        conn = sqlite3.connect('/opt/OpenIrrigation/irrigation.db')
        c = conn.cursor()
        def create_table():
            c.execute(
                'CREATE TABLE IF NOT EXISTS IrrigationResults(Id REAL, CurrentYear REAL, CurrentWeekNumber REAL, CurrentDay REAL, Time REAL, IrrigationNeeded, IrrigationAmount REAL, AvgTemp REAL, TotalRainFall REAL)')
            c.execute('''INSERT INTO IrrigationResults(Id, CurrentYear, CurrentWeekNumber,CurrentDay, Time, IrrigationNeeded, IrrigationAmount, AvgTemp, TotalRainFall)
                        VALUES(?,?,?,?,?,?,?,?,?)''', (
                DatabaseId, currentyear, currentweeknumber, currentday, ScriptStartTime, irrigationneeded,
                irrigationamount, avgtemp, totalrainfall))
            print('Database updated')
            conn.commit()
            c.close()
            conn.close()
        create_table()
        os.system('/usr/bin/python /opt/OpenIrrigation/htmlgenerator.py')
        irrigation = 0

    # check for wind speed exceedence
    if Wind > maxwindspeed:
        print('Wind is to strong, aborting')
        os.system('/usr/bin/python /opt/OpenIrrigation/htmlgenerator.py')
        irrigation = 0

    # check minimum temperature not to low
    if MinT <= 3:
        irrigationneeded = 0
        print('Warning: cold night, aborting')
        os.system("echo 0 > /sys/class/gpio/"+gpio+"/value")
        print('The irrigation is shutting down now')
        # Give a 0 value for no irrigation in database
        StartTime = 0
        EndTime = 0
        # Connect to the database
        conn = sqlite3.connect('/opt/OpenIrrigation/irrigation.db')
        c = conn.cursor()
        # Create Database entry for irrigation time
        irrigationtime = float(EndTime) - int(StartTime)
        irrigationamount = round((irrigationtime * float(irrigationoutput) / 3600), 1)
        # Connect to the database
        conn = sqlite3.connect('/opt/OpenIrrigation/irrigation.db')
        c = conn.cursor()
        def create_table():
            c.execute(
                'CREATE TABLE IF NOT EXISTS IrrigationResults(Id REAL, CurrentYear REAL, CurrentWeekNumber REAL, CurrentDay REAL, Time REAL, IrrigationNeeded, IrrigationAmount REAL, AvgTemp REAL, TotalRainFall REAL)')
            c.execute('''INSERT INTO IrrigationResults(Id, CurrentYear, CurrentWeekNumber,CurrentDay, Time, IrrigationNeeded, IrrigationAmount, AvgTemp, TotalRainFall)
            VALUES(?,?,?,?,?,?,?,?,?)''', (
            DatabaseId, currentyear, currentweeknumber, currentday, ScriptStartTime, irrigationneeded, irrigationamount,
            avgtemp, totalrainfall))
            print('Database updated')
            conn.commit()
            c.close()
            conn.close()
        create_table()
        irrigation = 2
        os.system('/usr/bin/python /opt/OpenIrrigation/htmlgenerator.py')
    if irrigation != 0:
        # ---irrigation time calculation---
        # temperature factor to calculate irrigation time
        if avgtemp < GrowthOptT:
            Tcalc1 = 1 - ((GrowthOptT - avgtemp) / float(GrowthOptT - GrowthMinT))
            if Tcalc1 <= 0:
                Tcalc = 0
            else:
                Tcalc = Tcalc1
        if avgtemp > GrowthOptT:
            Tcalc2 = 1 - (avgtemp - GrowthOptT) / float(GrowthOptT - GrowthMinT)
            if Tcalc2 <= 0.7:
                Tcalc = 0.7
            else:
                Tcalc = Tcalc2

        if avgtemp == GrowthOptT:
            Tcalc = 1

        TemperatureFactor = (math.sin(1.570795 * Tcalc))

        irrigationneeded = 0
        irrigationtime = (TemperatureFactor * MaxIrrigationTime * 0.5)
        print('The irrigation will turn on for ', irrigationtime, ' minutes')
        # Create a start time for valve open
        StartTime = datetime.datetime.now()
        os.system("echo 1 > /sys/class/gpio/"+gpio+"/value")
        t.sleep(float(irrigationtime * 60))
        print('The irrigation is shutting down now')
        os.system("echo 0 > /sys/class/gpio/"+gpio+"/value")
        # Create an end time for valve closed
        EndTime = datetime.datetime.now()
        # Create Database entry for irrigation time
        irrigationtimereal1 = EndTime - StartTime
        irrigationtimereal = irrigationtimereal1.seconds
        irrigationamount = round((irrigationtimereal * float(irrigationoutput) / 3600), 1)
        # Connect to the database
        conn = sqlite3.connect('/opt/OpenIrrigation/irrigation.db')
        c = conn.cursor()
        def create_table():
            c.execute(
                'CREATE TABLE IF NOT EXISTS IrrigationResults(Id REAL, CurrentYear REAL, CurrentWeekNumber REAL, CurrentDay REAL, Time REAL, IrrigationNeeded, IrrigationAmount REAL, AvgTemp REAL, TotalRainFall REAL)')
            c.execute('''INSERT INTO IrrigationResults(Id, CurrentYear, CurrentWeekNumber,CurrentDay, Time, IrrigationNeeded, IrrigationAmount, AvgTemp, TotalRainFall)
            VALUES(?,?,?,?,?,?,?,?,?)''', (
            DatabaseId, currentyear, currentweeknumber, currentday, ScriptStartTime, irrigationneeded, irrigationamount,
            avgtemp, totalrainfall))
            print('Database updated')
            conn.commit()
            c.close()
            conn.close()
        create_table()
        os.system('/usr/bin/python /opt/OpenIrrigation/htmlgenerator.py')
    irrigation = 1
#Continue the loop for all 16 valves
if valvesequence == 17:
    print('updating index.html')
    os.system('/usr/bin/python /opt/OpenIrrigation/htmlgenerator.py')
    exit()


