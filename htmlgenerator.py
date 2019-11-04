# -*- coding: utf-8 -*-
import linecache
import requests
import urllib
import json
import os

NSupplyNeeded = float(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',130))
OrganicMatter = float(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',131))
GrassCycling = float(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',129))
PercentageN  = float(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',132)) #first number e.g. 12-10-18
GardenSize = float(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',128))
Patentkali = float(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',133)) #(kg/ha) Fall only

NameValve1 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',2)
NameValve2 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',3)
NameValve3 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',4)
NameValve4 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',5)
NameValve5 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',6)
NameValve6 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',7)
NameValve7 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',8)
NameValve8 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',9)
NameValve9 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',10)
NameValve10 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',11)
NameValve11 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',12)
NameValve12 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',13)
NameValve13 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',14)
NameValve14 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',15)
NameValve15 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',16)
NameValve16 = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',17)

valvetype1 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 87))
valvetype2 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 88))
valvetype3 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 89))
valvetype4 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 90))
valvetype5 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 91))
valvetype6 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 92))
valvetype7 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 93))
valvetype8 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 94))
valvetype9 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 95))
valvetype10 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 96))
valvetype11 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 97))
valvetype12 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 98))
valvetype13 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 99))
valvetype14 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 100))
valvetype15 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 101))
valvetype16 = int(linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 102))

#Date and time calculations for database usage
import sqlite3
# date and time calculations for database usage
from datetime import *
currentweeknumber1 = datetime.today()
currentweeknumber = currentweeknumber1.strftime("%U")
lastsevendays = float(currentweeknumber)
last2weeks = float(currentweeknumber) - 1
last3weeks = float(currentweeknumber) - 2
last4weeks = float(currentweeknumber) - 3
lastyear = float(currentweeknumber) - 51
yesterday1 = datetime.now() - timedelta(days=1)
yesterday = yesterday1.strftime("%d")
import datetime
currentyear1 = datetime.datetime.now()
currentyear = currentyear1.year
currentday = currentyear1.day

# Get rainfalladata for today and yesterday and calculate rainfall past 24 hours
conn = sqlite3.connect('/opt/OpenIrrigation/raindata.db')
c = conn.cursor()
c.execute("SELECT sum(RainPastHour) FROM 'PrecepitationData' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=?",
          [0, lastsevendays, currentday])
rainfalltoday = c.fetchone()[0]

# current time
currenttime = datetime.datetime.now().strftime("%H:%M")

c.execute("SELECT sum(RainPastHour) FROM 'PrecepitationData' WHERE Id=? AND CurrentWeekNumber=? AND CurrentDay=? AND Time >?",[0, lastsevendays, yesterday, currenttime])
rainfallyesterday = c.fetchone()[0]
if rainfallyesterday is None:
    rainfallyesterday = 0

rainfallpast24hrs = rainfalltoday + rainfallyesterday


# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',70).strip()
conn = sqlite3.connect('plantdata.db')
c = conn.cursor()
if Name is not 0:
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT1 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT1 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater1 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',71).strip()
if Name is not 0:
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT2 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT2 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater2 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',72).strip()
if Name is not 0:
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT3 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT3 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater3 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',73).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT4 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT4 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater4 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',74).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT5 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT5 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater5 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',75).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT6 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT6 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater6 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',76).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT7 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT7 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater7 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',77).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT8 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT8 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater8 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',78).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT9 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT9 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater9 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',79).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT10 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT10 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater10 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',80).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT11 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT11 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater11 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',81).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT12 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT12 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater12 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',82).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT13 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT13 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater13 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',83).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT14 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT14 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater14 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',84).strip()
if Name is not '0' and Name is not 'None':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT15 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT15 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater15 = c.fetchone()[0]

# parameters from selected plant
Name = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt',85).strip()
if Name is not '0':
    c.execute("SELECT PlantId FROM 'PlantInfo' WHERE PlantName=?", [Name])
    PlantId = c.fetchone()[0]
    c.execute("SELECT MinTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMinT16 = c.fetchone()[0]
    c.execute("SELECT MaxTemperature FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    GrowthMaxT16 = c.fetchone()[0]
    c.execute("SELECT WaterPerSeason FROM 'PlantInfo' WHERE PlantId=?", [PlantId])
    YearlyAmountWater16 = c.fetchone()[0]


if GrassCycling > 0:
        NSupplyFromCompost1 = float(OrganicMatter /10 * 9) #(kg/ha)
        NSupplyFromGras = 12 * 0.250
        NSupplyFromCompost = NSupplyFromCompost1 + NSupplyFromGras

else:
        NSupplyFromCompost = float(OrganicMatter /10 * 9) #(kg/ha)

# Amount of N
march = str(round((float(1)/6 * ((NSupplyNeeded - NSupplyFromCompost) / PercentageN) * 100) * (float(GardenSize)/10000),1)) # Kg
april = str(round((float(1)/6 * ((NSupplyNeeded - NSupplyFromCompost) / PercentageN) * 100) * (float(GardenSize)/10000),1)) # Kg
may = str(round((float(1)/6 * ((NSupplyNeeded - NSupplyFromCompost) / PercentageN) * 100) * (float(GardenSize)/10000),1)) # Kg
june = str(round((float(1)/6 * ((NSupplyNeeded - NSupplyFromCompost) / PercentageN) * 100) * (float(GardenSize)/10000),1)) # Kg
july = str(round((float(1)/6 * ((NSupplyNeeded - NSupplyFromCompost) / PercentageN) * 100) * (float(GardenSize)/10000),1)) # Kg
august = str(round((float(1)/6 * ((NSupplyNeeded - NSupplyFromCompost) / PercentageN) * 100) * (float(GardenSize)/10000),1)) # Kg

patentkali = str(round((Patentkali) * (float(GardenSize)/10000),1)) # KG

compost1 = str(OrganicMatter /10 * GardenSize /2) # Kg in March-April
compost2 = str(OrganicMatter /10 * GardenSize /2) # Kg in September-Oktober

# Get weatherdata from OpenWeather
location = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 126).rstrip()
openWeatherKey = linecache.getline('/home/pi/.OpenIrrigation/gardendata.txt', 135).rstrip()

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

avgtemp = int((MinT + MaxT) / 2)

#TODO
# average temperature today
#conn = sqlite3.connect('/opt/OpenIrrigation/irrigation.db')
#c = conn.cursor()
#c.execute("SELECT avg(AvgTemp) FROM 'IrrigationResults' ORDER BY Id DESC LIMIT 1 WHERE CurrentWeekNumber=? AND CurrentDay=?", [lastsevendays,currentday])
#avgtemp = int(c.fetchone()[0])
#if avgtemp is None:
#        avgtemp = 0
#print avgtemp

# irrigation amount valve 1 today
conn = sqlite3.connect('/opt/OpenIrrigation/irrigation.db')
c = conn.cursor()
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=1", [lastsevendays,currentday])
irrigationamount1 = c.fetchone()[0]
if irrigationamount1 is None:
        irrigationamount1 = 0

# irrigation amount valve 2 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=2", [lastsevendays,currentday])
irrigationamount2 = c.fetchone()[0]
if irrigationamount2 is None:
        irrigationamount2 = 0

# irrigation amount valve 3 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=3", [lastsevendays,currentday])
irrigationamount3 = c.fetchone()[0]
if irrigationamount3 is None:
        irrigationamount3 = 0

# irrigation amount valve 4 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=4", [lastsevendays,currentday])
irrigationamount4 = c.fetchone()[0]
if irrigationamount4 is None:
        irrigationamount4 = 0

# irrigation amount valve 5 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=5", [lastsevendays,currentday])
irrigationamount5 = c.fetchone()[0]
if irrigationamount5 is None:
        irrigationamount5 = 0

# irrigation amount valve 6 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=6", [lastsevendays,currentday])
irrigationamount6 = c.fetchone()[0]
if irrigationamount6 is None:
        irrigationamount6 = 0

# irrigation amount valve 7 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=7", [lastsevendays,currentday])
irrigationamount7 = c.fetchone()[0]
if irrigationamount7 is None:
        irrigationamount7 = 0

# irrigation amount valve 8 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=8", [lastsevendays,currentday])
irrigationamount8 = c.fetchone()[0]
if irrigationamount8 is None:
        irrigationamount8 = 0

# irrigation amount valve 9 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=9", [lastsevendays,currentday])
irrigationamount9 = c.fetchone()[0]
if irrigationamount9 is None:
        irrigationamount9 = 0

# irrigation amount valve 10 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=10", [lastsevendays,currentday])
irrigationamount10 = c.fetchone()[0]
if irrigationamount10 is None:
        irrigationamount10 = 0

# irrigation amount valve 11 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=11", [lastsevendays,currentday])
irrigationamount11 = c.fetchone()[0]
if irrigationamount11 is None:
        irrigationamount11 = 0

# irrigation amount valve 12 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=12", [lastsevendays,currentday])
irrigationamount12 = c.fetchone()[0]
if irrigationamount12 is None:
        irrigationamount12 = 0

# irrigation amount valve 13 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=13", [lastsevendays,currentday])
irrigationamount13 = c.fetchone()[0]
if irrigationamount13 is None:
        irrigationamount13 = 0

# irrigation amount valve 14 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=14", [lastsevendays,currentday])
irrigationamount14 = c.fetchone()[0]
if irrigationamount14 is None:
        irrigationamount14 = 0

# irrigation amount valve 15 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=15", [lastsevendays,currentday])
irrigationamount15 = c.fetchone()[0]
if irrigationamount15 is None:
        irrigationamount15 = 0

# irrigation amount valve 16 today
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=16", [lastsevendays,currentday])
irrigationamount16 = c.fetchone()[0]
if irrigationamount16 is None:
        irrigationamount16 = 0

c.execute("SELECT avg(AvgTemp) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=1", [lastsevendays])
AverageTemperaturePastWeek = c.fetchone()[0]
if AverageTemperaturePastWeek is None:
        AverageTemperaturePastWeek = 0

# irrigation valve 1 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=1", [lastsevendays])
IrrigationValve11 = c.fetchone()[0]
if IrrigationValve11 is not None:
        IrrigationValve1 = round(float(IrrigationValve11),1)
else:
        IrrigationValve1 = 0
c.execute("SELECT sum(TotalRainFall) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=0", [lastsevendays])
RainValve11 = c.fetchone()[0]
if RainValve11 is not None:
        RainValve1 = round(float(RainValve11),1)
else:
        RainValve1 = 0
TotalWaterPastWeek1 = IrrigationValve1 + RainValve1

# irrigation valve 2 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=2", [lastsevendays])
IrrigationValve21 = c.fetchone()[0]
if IrrigationValve21 is not None:
        IrrigationValve2 = round(float(IrrigationValve21),1)
else:
        IrrigationValve2 = 0
TotalWaterPastWeek2 = IrrigationValve2 + RainValve1

# irrigation valve 3 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=3", [lastsevendays])
IrrigationValve31 = c.fetchone()[0]
if IrrigationValve31 is not None:
        IrrigationValve3 = round(float(IrrigationValve31),1)
else:
        IrrigationValve3 = 0
TotalWaterPastWeek3 = IrrigationValve3 + RainValve1

# irrigation valve 4 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=4", [lastsevendays])
IrrigationValve41 = c.fetchone()[0]
if IrrigationValve41 is not None:
        IrrigationValve4 = round(float(IrrigationValve41),1)
else:
        IrrigationValve4 = 0
TotalWaterPastWeek4 = IrrigationValve4 + RainValve1

# irrigation valve 5 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=5", [lastsevendays])
IrrigationValve51 = c.fetchone()[0]
if IrrigationValve51 is not None:
        IrrigationValve5 = round(float(IrrigationValve51),1)
else:
        IrrigationValve5 = 0
TotalWaterPastWeek5 = IrrigationValve5 + RainValve1

# irrigation valve 6 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=6", [lastsevendays])
IrrigationValve61 = c.fetchone()[0]
if IrrigationValve61 is not None:
        IrrigationValve6 = round(float(IrrigationValve61),1)
else:
        IrrigationValve6 = 0
TotalWaterPastWeek6 = IrrigationValve6 + RainValve1

# irrigation valve 7 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=7", [lastsevendays])
IrrigationValve71 = c.fetchone()[0]
if IrrigationValve71 is not None:
        IrrigationValve7 = round(float(IrrigationValve71),1)
else:
        IrrigationValve7 = 0
TotalWaterPastWeek7 = IrrigationValve7 + RainValve1

# irrigation valve 8 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=8", [lastsevendays])
IrrigationValve81 = c.fetchone()[0]
if IrrigationValve81 is not None:
        IrrigationValve8 = round(float(IrrigationValve81),1)
else:
        IrrigationValve8 = 0
TotalWaterPastWeek8 = IrrigationValve8 + RainValve1

# irrigation valve 9 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=9", [lastsevendays])
IrrigationValve91 = c.fetchone()[0]
if IrrigationValve91 is not None:
        IrrigationValve9 = round(float(IrrigationValve91),1)
else:
        IrrigationValve9 = 0
TotalWaterPastWeek9 = IrrigationValve9 + RainValve1

# irrigation valve 10 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=10", [lastsevendays])
IrrigationValve101 = c.fetchone()[0]
if IrrigationValve101 is not None:
        IrrigationValve10 = round(float(IrrigationValve101),1)
else:
        IrrigationValve10 = 0
TotalWaterPastWeek10 = IrrigationValve10 + RainValve1

# irrigation valve 11 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=11", [lastsevendays])
IrrigationValve111 = c.fetchone()[0]
if IrrigationValve111 is not None:
        IrrigationValve11 = round(float(IrrigationValve111),1)
else:
        IrrigationValve11 = 0
TotalWaterPastWeek11 = IrrigationValve11 + RainValve1

# irrigation valve 12 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=12", [lastsevendays])
IrrigationValve121 = c.fetchone()[0]
if IrrigationValve121 is not None:
        IrrigationValve12 = round(float(IrrigationValve121),1)
else:
        IrrigationValve12 = 0
TotalWaterPastWeek12 = IrrigationValve12 + RainValve1

# irrigation valve 13 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=13", [lastsevendays])
IrrigationValve131 = c.fetchone()[0]
if IrrigationValve131 is not None:
        IrrigationValve13 = round(float(IrrigationValve131),1)
else:
        IrrigationValve13 = 0
TotalWaterPastWeek13 = IrrigationValve13 + RainValve1

# irrigation valve 14 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=14", [lastsevendays])
IrrigationValve141 = c.fetchone()[0]
if IrrigationValve141 is not None:
        IrrigationValve14 = round(float(IrrigationValve141),1)
else:
        IrrigationValve14 = 0
TotalWaterPastWeek14 = IrrigationValve14 + RainValve1

# irrigation valve 15 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=15", [lastsevendays])
IrrigationValve151 = c.fetchone()[0]
if IrrigationValve151 is not None:
        IrrigationValve15 = round(float(IrrigationValve151),1)
else:
        IrrigationValve15 = 0
TotalWaterPastWeek15 = IrrigationValve15 + RainValve1

# irrigation valve 16 in the past week
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=16", [lastsevendays])
IrrigationValve161 = c.fetchone()[0]
if IrrigationValve161 is not None:
        IrrigationValve16 = round(float(IrrigationValve161),1)
else:
        IrrigationValve16 = 0
TotalWaterPastWeek16 = IrrigationValve16 + RainValve1


# irrigation valve 1 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=1", [last2weeks])
Irrigation2Valve11 = c.fetchone()[0]
if Irrigation2Valve11 is not None:
        Irrigation2Valve1 = round(float(Irrigation2Valve11),1)
else:
        Irrigation2Valve1 = 0
c.execute("SELECT sum(TotalRainFall) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=0", [last2weeks])
RainValve11 = c.fetchone()[0]
if RainValve11 is not None:
        RainValve11 = 0
        if RainValve11 is not None:
                RainValve1 = round(float(RainValve11),1)
else:
        RainValve1 = 0
TotalWaterPast2Weeks1 = Irrigation2Valve1 + RainValve1

# irrigation valve 2 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=2", [last2weeks])
Irrigation2Valve21 = c.fetchone()[0]
if Irrigation2Valve21 is not None:
        Irrigation2Valve2 = round(float(Irrigation2Valve21),1)
else:
        Irrigation2Valve2 = 0
TotalWaterPast2Weeks2 = Irrigation2Valve2 + RainValve1

# irrigation valve 3 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=3", [last2weeks])
Irrigation2Valve31 = c.fetchone()[0]
if Irrigation2Valve31 is not None:
        Irrigation2Valve3 = round(float(Irrigation2Valve31),1)
else:
        Irrigation2Valve3 = 0
TotalWaterPast2Weeks3 = Irrigation2Valve3 + RainValve1

# irrigation valve 4 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=4", [last2weeks])
Irrigation2Valve41 = c.fetchone()[0]
if Irrigation2Valve41 is not None:
        Irrigation2Valve4 = round(float(Irrigation2Valve41),1)
else:
        Irrigation2Valve4 = 0
TotalWaterPast2Weeks4 = Irrigation2Valve4 + RainValve1

# irrigation valve 5 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=5", [last2weeks])
Irrigation2Valve51 = c.fetchone()[0]
if Irrigation2Valve51 is not None:
        Irrigation2Valve5 = round(float(Irrigation2Valve51),1)
else:
        Irrigation2Valve5 = 0
TotalWaterPast2Weeks5 = Irrigation2Valve5 + RainValve1

# irrigation valve 6 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=6", [last2weeks])
Irrigation2Valve61 = c.fetchone()[0]
if Irrigation2Valve61 is not None:
        Irrigation2Valve6 = round(float(Irrigation2Valve61),1)
else:
        Irrigation2Valve6 = 0
TotalWaterPast2Weeks6 = Irrigation2Valve6 + RainValve1

# irrigation valve 7 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=7", [last2weeks])
Irrigation2Valve71 = c.fetchone()[0]
if Irrigation2Valve71 is not None:
        Irrigation2Valve7 = round(float(Irrigation2Valve71),1)
else:
        Irrigation2Valve7 = 0
TotalWaterPast2Weeks7 = Irrigation2Valve7 + RainValve1

# irrigation valve 8 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=8", [last2weeks])
Irrigation2Valve81 = c.fetchone()[0]
if Irrigation2Valve81 is not None:
        Irrigation2Valve8 = round(float(Irrigation2Valve81),1)
else:
        Irrigation2Valve8 = 0
TotalWaterPast2Weeks8 = Irrigation2Valve8 + RainValve1

# irrigation valve 9 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=9", [last2weeks])
Irrigation2Valve91 = c.fetchone()[0]
if Irrigation2Valve91 is not None:
        Irrigation2Valve9 = round(float(Irrigation2Valve91),1)
else:
        Irrigation2Valve9 = 0
TotalWaterPast2Weeks9 = Irrigation2Valve9 + RainValve1

# irrigation valve 10 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=10", [last2weeks])
Irrigation2Valve101 = c.fetchone()[0]
if Irrigation2Valve101 is not None:
        Irrigation2Valve10 = round(float(Irrigation2Valve101),1)
else:
        Irrigation2Valve10 = 0
TotalWaterPast2Weeks10 = Irrigation2Valve10 + RainValve1

# irrigation valve 11 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=11", [last2weeks])
Irrigation2Valve111 = c.fetchone()[0]
if Irrigation2Valve111 is not None:
        Irrigation2Valve11 = round(float(Irrigation2Valve111),1)
else:
        Irrigation2Valve11 = 0
TotalWaterPast2Weeks11 = Irrigation2Valve11 + RainValve1

# irrigation valve 12 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=12", [last2weeks])
Irrigation2Valve121 = c.fetchone()[0]
if Irrigation2Valve121 is not None:
        Irrigation2Valve12 = round(float(Irrigation2Valve121),1)
else:
        Irrigation2Valve12 = 0
TotalWaterPast2Weeks12 = Irrigation2Valve12 + RainValve1

# irrigation valve 13 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=13", [last2weeks])
Irrigation2Valve131 = c.fetchone()[0]
if Irrigation2Valve131 is not None:
        Irrigation2Valve13 = round(float(Irrigation2Valve131),1)
else:
        Irrigation2Valve13 = 0
TotalWaterPast2Weeks13 = Irrigation2Valve13 + RainValve1

# irrigation valve 14 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=14", [last2weeks])
Irrigation2Valve141 = c.fetchone()[0]
if Irrigation2Valve141 is not None:
        Irrigation2Valve14 = round(float(Irrigation2Valve141),1)
else:
        Irrigation2Valve14 = 0
TotalWaterPast2Weeks14 = Irrigation2Valve14 + RainValve1

# irrigation valve 15 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=15", [last2weeks])
Irrigation2Valve151 = c.fetchone()[0]
if Irrigation2Valve151 is not None:
        Irrigation2Valve15 = round(float(Irrigation2Valve151),1)
else:
        Irrigation2Valve15 = 0
TotalWaterPast2Weeks15 = Irrigation2Valve15 + RainValve1

# irrigation valve 16 in the past 2 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=16", [last2weeks])
Irrigation2Valve161 = c.fetchone()[0]
if Irrigation2Valve161 is not None:
        Irrigation2Valve16 = round(float(Irrigation2Valve161),1)
else:
        Irrigation2Valve16 = 0
TotalWaterPast2Weeks16 = Irrigation2Valve16 + RainValve1

# irrigation valve 1 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=1", [last3weeks])
Irrigation3Valve11 = c.fetchone()[0]
if Irrigation3Valve11 is not None:
        Irrigation3Valve1 = round(float(Irrigation3Valve11),1)
else:
        Irrigation3Valve1 = 0
c.execute("SELECT sum(TotalRainFall) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=0", [last3weeks])
RainValve11 = c.fetchone()[0]
if RainValve11 is not None:
        RainValve1 = round(float(RainValve11),1)
else:
        RainValve1 = 0
TotalWaterPast3Weeks1 = Irrigation3Valve1 + RainValve1

# irrigation valve 2 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=2", [last3weeks])
Irrigation3Valve21 = c.fetchone()[0]
if Irrigation3Valve21 is not None:
        Irrigation3Valve2 = round(float(Irrigation3Valve21),1)
else:
        Irrigation3Valve2 = 0
TotalWaterPast3Weeks2 = Irrigation3Valve2 + RainValve1

# irrigation valve 3 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=3", [last3weeks])
Irrigation3Valve31 = c.fetchone()[0]
if Irrigation3Valve31 is not None:
        Irrigation3Valve3 = round(float(Irrigation3Valve31),1)
else:
        Irrigation3Valve3 = 0
TotalWaterPast3Weeks3 = Irrigation3Valve3 + RainValve1

# irrigation valve 4 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=4", [last3weeks])
Irrigation3Valve41 = c.fetchone()[0]
if Irrigation3Valve41 is not None:
        Irrigation3Valve4 = round(float(Irrigation3Valve41),1)
else:
        Irrigation3Valve4 = 0
TotalWaterPast3Weeks4 = Irrigation3Valve4 + RainValve1

# irrigation valve 5 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=5", [last3weeks])
Irrigation3Valve51 = c.fetchone()[0]
if Irrigation3Valve51 is not None:
        Irrigation3Valve5 = round(float(Irrigation3Valve51),1)
else:
        Irrigation3Valve5 = 0
TotalWaterPast3Weeks5 = Irrigation3Valve5 + RainValve1

# irrigation valve 6 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=6", [last3weeks])
Irrigation3Valve61 = c.fetchone()[0]
if Irrigation3Valve61 is not None:
        Irrigation3Valve6 = round(float(Irrigation3Valve61),1)
else:
        Irrigation3Valve6 = 0
TotalWaterPast3Weeks6 = Irrigation3Valve6 + RainValve1

# irrigation valve 7 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=7", [last3weeks])
Irrigation3Valve71 = c.fetchone()[0]
if Irrigation3Valve71 is not None:
        Irrigation3Valve7 = round(float(Irrigation3Valve71),1)
else:
        Irrigation3Valve7 = 0
TotalWaterPast3Weeks7 = Irrigation3Valve7 + RainValve1

# irrigation valve 8 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=8", [last3weeks])
Irrigation3Valve81 = c.fetchone()[0]
if Irrigation3Valve81 is not None:
        Irrigation3Valve8 = round(float(Irrigation3Valve81),1)
else:
        Irrigation3Valve8 = 0
TotalWaterPast3Weeks8 = Irrigation3Valve8 + RainValve1

# irrigation valve 9 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=9", [last3weeks])
Irrigation3Valve91 = c.fetchone()[0]
if Irrigation3Valve91 is not None:
        Irrigation3Valve9 = round(float(Irrigation3Valve91),1)
else:
        Irrigation3Valve9 = 0
TotalWaterPast3Weeks9 = Irrigation3Valve9 + RainValve1

# irrigation valve 10 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=10", [last3weeks])
Irrigation3Valve101 = c.fetchone()[0]
if Irrigation3Valve101 is not None:
        Irrigation3Valve10 = round(float(Irrigation3Valve101),1)
else:
        Irrigation3Valve10 = 0
TotalWaterPast3Weeks10 = Irrigation3Valve10 + RainValve1

# irrigation valve 11 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=11", [last3weeks])
Irrigation3Valve111 = c.fetchone()[0]
if Irrigation3Valve111 is not None:
        Irrigation3Valve11 = round(float(Irrigation3Valve111),1)
else:
        Irrigation3Valve11 = 0
TotalWaterPast3Weeks11 = Irrigation3Valve11 + RainValve1

# irrigation valve 12 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=12", [last3weeks])
Irrigation3Valve121 = c.fetchone()[0]
if Irrigation3Valve121 is not None:
        Irrigation3Valve12 = round(float(Irrigation3Valve121),1)
else:
        Irrigation3Valve12 = 0
TotalWaterPast3Weeks12 = Irrigation3Valve12 + RainValve1

# irrigation valve 13 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=13", [last3weeks])
Irrigation3Valve131 = c.fetchone()[0]
if Irrigation3Valve131 is not None:
        Irrigation3Valve13 = round(float(Irrigation3Valve131),1)
else:
        Irrigation3Valve13 = 0
TotalWaterPast3Weeks13 = Irrigation3Valve13 + RainValve1

# irrigation valve 14 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=14", [last3weeks])
Irrigation3Valve141 = c.fetchone()[0]
if Irrigation3Valve141 is not None:
        Irrigation3Valve14 = round(float(Irrigation3Valve141),1)
else:
        Irrigation3Valve14 = 0
TotalWaterPast3Weeks14 = Irrigation3Valve14 + RainValve1

# irrigation valve 15 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=15", [last3weeks])
Irrigation3Valve151 = c.fetchone()[0]
if Irrigation3Valve151 is not None:
        Irrigation3Valve15 = round(float(Irrigation3Valve151),1)
else:
        Irrigation3Valve15 = 0
TotalWaterPast3Weeks15 = Irrigation3Valve15 + RainValve1

# irrigation valve 16 in the past 3 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=16", [last3weeks])
Irrigation3Valve161 = c.fetchone()[0]
if Irrigation3Valve161 is not None:
        Irrigation3Valve16 = round(float(Irrigation3Valve161),1)
else:
        Irrigation3Valve16 = 0
TotalWaterPast3Weeks16 = Irrigation3Valve16 + RainValve1

# irrigation valve 1 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=1", [last4weeks])
Irrigation4Valve11 = c.fetchone()[0]
if Irrigation4Valve11 is not None:
        Irrigation4Valve1 = round(float(Irrigation4Valve11),1)
else:
        Irrigation4Valve1 = 0
c.execute("SELECT sum(TotalRainFall) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=0", [last4weeks])
RainValve11 = c.fetchone()[0]
if RainValve11 is not None:
        RainValve1 = round(float(RainValve11),1)
else:
        RainValve1 = 0
TotalWaterPast4Weeks1 = Irrigation4Valve1 + RainValve1

# irrigation valve 2 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=2", [last4weeks])
Irrigation4Valve21 = c.fetchone()[0]
if Irrigation4Valve21 is not None:
        Irrigation4Valve2 = round(float(Irrigation4Valve21),1)
else:
        Irrigation4Valve2 = 0
TotalWaterPast4Weeks2 = Irrigation4Valve2 + RainValve1

# irrigation valve 3 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=3", [last4weeks])
Irrigation4Valve31 = c.fetchone()[0]
if Irrigation4Valve31 is not None:
        Irrigation4Valve3 = round(float(Irrigation4Valve31),1)
else:
        Irrigation4Valve3 = 0
TotalWaterPast4Weeks3 = Irrigation4Valve3 + RainValve1

# irrigation valve 4 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=4", [last4weeks])
Irrigation4Valve41 = c.fetchone()[0]
if Irrigation4Valve41 is not None:
        Irrigation4Valve4 = round(float(Irrigation4Valve41),1)
else:
        Irrigation4Valve4 = 0
TotalWaterPast4Weeks4 = Irrigation4Valve4 + RainValve1

# irrigation valve 5 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=5", [last4weeks])
Irrigation4Valve51 = c.fetchone()[0]
if Irrigation4Valve51 is not None:
        Irrigation4Valve5 = round(float(Irrigation4Valve51),1)
else:
        Irrigation4Valve5 = 0
TotalWaterPast4Weeks5 = Irrigation4Valve5 + RainValve1

# irrigation valve 6 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=6", [last4weeks])
Irrigation4Valve61 = c.fetchone()[0]
if Irrigation4Valve61 is not None:
        Irrigation4Valve6 = round(float(Irrigation4Valve61),1)
else:
        Irrigation4Valve6 = 0
TotalWaterPast4Weeks6 = Irrigation4Valve6 + RainValve1

# irrigation valve 7 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=7", [last4weeks])
Irrigation4Valve71 = c.fetchone()[0]
if Irrigation4Valve71 is not None:
        Irrigation4Valve7 = round(float(Irrigation4Valve71),1)
else:
        Irrigation4Valve7 = 0
TotalWaterPast4Weeks7 = Irrigation4Valve7 + RainValve1

# irrigation valve 8 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=8", [last4weeks])
Irrigation4Valve81 = c.fetchone()[0]
if Irrigation4Valve81 is not None:
        Irrigation4Valve8 = round(float(Irrigation4Valve81),1)
else:
        Irrigation4Valve8 = 0
TotalWaterPast4Weeks8 = Irrigation4Valve8 + RainValve1

# irrigation valve 9 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=9", [last4weeks])
Irrigation4Valve91 = c.fetchone()[0]
if Irrigation4Valve91 is not None:
        Irrigation4Valve9 = round(float(Irrigation4Valve91),1)
else:
        Irrigation4Valve9 = 0
TotalWaterPast4Weeks9 = Irrigation4Valve9 + RainValve1

# irrigation valve 10 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=10", [last4weeks])
Irrigation4Valve101 = c.fetchone()[0]
if Irrigation4Valve101 is not None:
        Irrigation4Valve10 = round(float(Irrigation4Valve101),1)
else:
        Irrigation4Valve10 = 0
TotalWaterPast4Weeks10 = Irrigation4Valve10 + RainValve1

# irrigation valve 11 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=11", [last4weeks])
Irrigation4Valve111 = c.fetchone()[0]
if Irrigation4Valve111 is not None:
        Irrigation4Valve11 = round(float(Irrigation4Valve111),1)
else:
        Irrigation4Valve11 = 0
TotalWaterPast4Weeks11 = Irrigation4Valve11 + RainValve1

# irrigation valve 12 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=12", [last4weeks])
Irrigation4Valve121 = c.fetchone()[0]
if Irrigation4Valve121 is not None:
        Irrigation4Valve12 = round(float(Irrigation4Valve121),1)
else:
        Irrigation4Valve12 = 0
TotalWaterPast4Weeks12 = Irrigation4Valve12 + RainValve1

# irrigation valve 13 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=13", [last4weeks])
Irrigation4Valve131 = c.fetchone()[0]
if Irrigation4Valve131 is not None:
        Irrigation4Valve13 = round(float(Irrigation4Valve131),1)
else:
        Irrigation4Valve13 = 0
TotalWaterPast4Weeks13 = Irrigation4Valve13 + RainValve1

# irrigation valve 14 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=14", [last4weeks])
Irrigation4Valve141 = c.fetchone()[0]
if Irrigation4Valve141 is not None:
        Irrigation4Valve14 = round(float(Irrigation4Valve141),1)
else:
        Irrigation4Valve14 = 0
TotalWaterPast4Weeks14 = Irrigation4Valve14 + RainValve1

# irrigation valve 15 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=15", [last4weeks])
Irrigation4Valve151 = c.fetchone()[0]
if Irrigation4Valve151 is not None:
        Irrigation4Valve15 = round(float(Irrigation4Valve151),1)
else:
        Irrigation4Valve15 = 0
TotalWaterPast4Weeks15 = Irrigation4Valve15 + RainValve1

# irrigation valve 16 in the past 4 weeks
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=16", [last4weeks])
Irrigation4Valve161 = c.fetchone()[0]
if Irrigation4Valve161 is not None:
        Irrigation4Valve16 = round(float(Irrigation4Valve161),1)
else:
        Irrigation4Valve16 = 0
TotalWaterPast4Weeks16 = Irrigation4Valve16 + RainValve1

# irrigation valve 1 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=1", [currentyear])
IrrigationyValve11 = c.fetchone()[0]
if IrrigationyValve11 is not None:
        IrrigationyValve1 = round(float(IrrigationyValve11),1)
else:
        IrrigationyValve1 = 0
c.execute("SELECT sum(TotalRainFall) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND Id=0", [currentyear])
RainValve11 = c.fetchone()[0]
if RainValve11 is not None:
        RainValve1 = round(float(RainValve11),1)
else:
        RainValve1 = 0
TotalWatery1 = IrrigationyValve1 + RainValve1

# irrigation valve 2 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=2", [currentyear])
IrrigationyValve21 = c.fetchone()[0]
if IrrigationyValve21 is not None:
        IrrigationyValve2 = round(float(IrrigationyValve21),1)
else:
        IrrigationyValve2 = 0
TotalWatery2 = IrrigationyValve2 + RainValve1

# irrigation valve 3 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=3", [currentyear])
IrrigationyValve31 = c.fetchone()[0]
if IrrigationyValve31 is not None:
        IrrigationyValve3 = round(float(IrrigationyValve31),1)
else:
        IrrigationyValve3 = 0
TotalWatery3 = IrrigationyValve3 + RainValve1

# irrigation valve 4 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=4", [currentyear])
IrrigationyValve41 = c.fetchone()[0]
if IrrigationyValve41 is not None:
        IrrigationyValve4 = round(float(IrrigationyValve41),1)
else:
        IrrigationyValve4 = 0
TotalWatery4 = IrrigationyValve4 + RainValve1

# irrigation valve 5 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=5", [currentyear])
IrrigationyValve51 = c.fetchone()[0]
if IrrigationyValve51 is not None:
        IrrigationyValve5 = round(float(IrrigationyValve51),1)
else:
        IrrigationyValve5 = 0
TotalWatery5 = IrrigationyValve5 + RainValve1

# irrigation valve 6 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=6", [currentyear])
IrrigationyValve61 = c.fetchone()[0]
if IrrigationyValve61 is not None:
        IrrigationyValve6 = round(float(IrrigationyValve61),1)
else:
        IrrigationyValve6 = 0
TotalWatery6 = IrrigationyValve6 + RainValve1

# irrigation valve 7 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=7", [currentyear])
IrrigationyValve71 = c.fetchone()[0]
if IrrigationyValve71 is not None:
        IrrigationyValve7 = round(float(IrrigationyValve71),1)
else:
        IrrigationyValve7 = 0
TotalWatery7 = IrrigationyValve7 + RainValve1

# irrigation valve 8 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=8", [currentyear])
IrrigationyValve81 = c.fetchone()[0]
if IrrigationyValve81 is not None:
        IrrigationyValve8 = round(float(IrrigationyValve81),1)
else:
        IrrigationyValve8 = 0
TotalWatery8 = IrrigationyValve8 + RainValve1

# irrigation valve 9 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=9", [currentyear])
IrrigationyValve91 = c.fetchone()[0]
if IrrigationyValve91 is not None:
        IrrigationyValve9 = round(float(IrrigationyValve91),1)
else:
        IrrigationyValve9 = 0
TotalWatery9 = IrrigationyValve9 + RainValve1

# irrigation valve 10 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=10", [currentyear])
IrrigationyValve101 = c.fetchone()[0]
if IrrigationyValve101 is not None:
        IrrigationyValve10 = round(float(IrrigationyValve101),1)
else:
        IrrigationyValve10 = 0
TotalWatery10 = IrrigationyValve10 + RainValve1

# irrigation valve 11 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=11", [currentyear])
IrrigationyValve111 = c.fetchone()[0]
if IrrigationyValve111 is not None:
        IrrigationyValve11 = round(float(IrrigationyValve111),1)
else:
        IrrigationyValve11 = 0
TotalWatery11 = IrrigationyValve11 + RainValve1

# irrigation valve 12 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=12", [currentyear])
IrrigationyValve121 = c.fetchone()[0]
if IrrigationyValve121 is not None:
        IrrigationyValve12 = round(float(IrrigationyValve121),1)
else:
        IrrigationyValve12 = 0
TotalWatery12 = IrrigationyValve12 + RainValve1

# irrigation valve 13 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=13", [currentyear])
IrrigationyValve131 = c.fetchone()[0]
if IrrigationyValve131 is not None:
        IrrigationyValve13 = round(float(IrrigationyValve131),1)
else:
        IrrigationyValve13 = 0
TotalWatery13 = IrrigationyValve13 + RainValve1

# irrigation valve 14 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=14", [currentyear])
IrrigationyValve141 = c.fetchone()[0]
if IrrigationyValve141 is not None:
        IrrigationyValve14 = round(float(IrrigationyValve141),1)
else:
        IrrigationyValve14 = 0
TotalWatery14 = IrrigationyValve14 + RainValve1

# irrigation valve 15 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=15", [currentyear])
IrrigationyValve151 = c.fetchone()[0]
if IrrigationyValve151 is not None:
        IrrigationyValve15 = round(float(IrrigationyValve151),1)
else:
        IrrigationyValve15 = 0
TotalWatery15 = IrrigationyValve15 + RainValve1

# irrigation valve 16 in the past year
c.execute("SELECT sum(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentYear=? AND Id=16", [currentyear])
IrrigationyValve161 = c.fetchone()[0]
if IrrigationyValve161 is not None:
        IrrigationyValve16 = round(float(IrrigationyValve161),1)
else:
        IrrigationyValve16 = 0
TotalWatery16 = IrrigationyValve16 + RainValve1

# times irrigated valve 1 today
c.execute("SELECT count(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=1", [lastsevendays,currentday])
irrigationcount1 = c.fetchone()[0]
if irrigationcount1 is None:
        irrigationcount1 = 0

# times irrigated valve 2 today
c.execute("SELECT count(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=2", [lastsevendays,currentday])
irrigationcount2 = c.fetchone()[0]
if irrigationcount2 is None:
        irrigationcount2 = 0

# times irrigated valve 3 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=3", [lastsevendays,currentday])
irrigationcount3 = c.fetchone()[0]
if irrigationcount3 is None:
        irrigationcount3 = 0

# times irrigated valve 4 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=4", [lastsevendays,currentday])
irrigationcount4 = c.fetchone()[0]
if irrigationcount4 is None:
        irrigationcount4 = 0

# times irrigated valve 5 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=5",
          [lastsevendays, currentday])
irrigationcount5 = c.fetchone()[0]
if irrigationcount5 is None:
    irrigationcount5 = 0

# times irrigated valve 6 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=6",
          [lastsevendays, currentday])
irrigationcount6 = c.fetchone()[0]
if irrigationcount6 is None:
    irrigationcount6 = 0

# times irrigated valve 7 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=7",
          [lastsevendays, currentday])
irrigationcount7 = c.fetchone()[0]
if irrigationcount7 is None:
    irrigationcount7 = 0

# times irrigated valve 8 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=8",
          [lastsevendays, currentday])
irrigationcount8 = c.fetchone()[0]
if irrigationcount8 is None:
    irrigationcount8 = 0

# times irrigated valve 9 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=9",
          [lastsevendays, currentday])
irrigationcount9 = c.fetchone()[0]
if irrigationcount9 is None:
    irrigationcount9 = 0

# times irrigated valve 10 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=10",
          [lastsevendays, currentday])
irrigationcount10 = c.fetchone()[0]
if irrigationcount10 is None:
    irrigationcount10 = 0

# times irrigated valve 11 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=11",
          [lastsevendays, currentday])
irrigationcount11 = c.fetchone()[0]
if irrigationcount11 is None:
    irrigationcount11 = 0

# times irrigated valve 12 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=12",
          [lastsevendays, currentday])
irrigationcount12 = c.fetchone()[0]
if irrigationcount12 is None:
    irrigationcount12 = 0

# times irrigated valve 13 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=13",
          [lastsevendays, currentday])
irrigationcount13 = c.fetchone()[0]
if irrigationcount13 is None:
    irrigationcount13 = 0

# times irrigated valve 14 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=14",
          [lastsevendays, currentday])
irrigationcount14 = c.fetchone()[0]
if irrigationcount14 is None:
    irrigationcount14 = 0

# times irrigated valve 15 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=15",
          [lastsevendays, currentday])
irrigationcount15 = c.fetchone()[0]
if irrigationcount15 is None:
    irrigationcount15 = 0

# times irrigated valve 16 today
c.execute("SELECT COUNT(IrrigationAmount) FROM 'IrrigationResults' WHERE CurrentWeekNumber=? AND CurrentDay=? AND Id=16",
          [lastsevendays, currentday])
irrigationcount16 = c.fetchone()[0]
if irrigationcount16 is None:
    irrigationcount16 = 0

# Generate the index.html page
with open('/var/www/html/index.html', 'w') as out:
        out.write('<html>')
        out.write('<head><title>')
        out.write('Open Irrigation Software')
        out.write('</title></head>')


        out.write('<body style="margin: 0px; padding: 0px; font-family: arial, sans-serif;">')
        out.write('<style media="screen" type="text/css">')
        out.write('<style>')
        out.write('h2 {')
        out.write('  display: block;')
        out.write('  align: left;')
        out.write('  margin-top: 0.83em;')
        out.write('  margin-bottom: 0.83em;')
        out.write('  margin-left: 0;')
        out.write('  margin-right: 0;')
        out.write('  padding: 0px;')
        out.write('  position: relative;')


        out.write('  font-size: 1.8em;')
        out.write('}')

        out.write('h3 {')
        out.write('  display: block;')
        out.write('  align: left;')
        out.write('  margin-top: 0.83em;')
        out.write('  margin-bottom: 0.83em;')
        out.write('  margin-left: 0;')
        out.write('  margin-right: 0;')
        out.write('  padding: 0px;')
        out.write('  position: relative;')
        out.write('  font-weight: bold;')
        out.write('  color: #1671AE;')
        out.write('  font-size: 1.2em;')
        out.write('}')
        out.write('h4 {')
        out.write('  display: block;')
        out.write('  margin-top: 0.83em;')
        out.write('  margin-bottom: 0.83em;')
        out.write('  align: left;')
        out.write('  margin-left: 0;')
        out.write('  margin-right: 0;')
        out.write('  padding: 0px;')
        out.write('  position: relative;')
        out.write('  font-weight: bold;')
        out.write('  color: #4F4F4F;')
        out.write('  font-size: 1.2em;')
        out.write('}')
        out.write('h5 {')
        out.write('  display: block;')
        out.write('  margin-top: 0;')
        out.write('  margin-bottom: 0;')
        out.write('  align: left;')
        out.write('  margin-left: 0;')
        out.write('  margin-right: 0;')
        out.write('  padding: 0px;')
        out.write('  position: relative;')
        out.write('  font-weight: bold;')
        out.write('  color: #4F4F4F;')
        out.write('  font-size: 1.0em;')
        out.write('}')
        out.write('meter {')
        out.write('width: 90%;')
        out.write('height: 15px;')
        #out.write('-webkit-appearance: none; /* Reset appearance */')
        out.write('border: 1px solid #ccc;')
        out.write('border-radius: 3px;')
        out.write('}')
        out.write('.StandardButton {')
        out.write('background-color:#1671AE;')
        out.write('-moz-border-radius:4px;')
        out.write('-webkit-border-radius:4px;')
        out.write('border-radius:4px;')
        out.write('border:1px solid #4b8f29;')
        out.write('display:inline-block;')
        out.write('cursor:pointer;')
        out.write('color:#ffffff;')
        out.write('font-family:Arial;')
        out.write('font-size:12px;')
        out.write('font-weight:bold;')
        out.write('margin: 5px;')
        out.write('padding:10px 16px;')
        out.write('text-decoration:none;')
        out.write('text-shadow:0px 0px 0px #5b8a3c;')
        out.write('}')
        out.write('.StandardButton:hover {')
        out.write('background-color:#72b352;')
        out.write('}')
        out.write('.StandardButton:active {')
        out.write('position:relative;')
        out.write('top:1px;')
        out.write('}')
        out.write('</style>')
        
        out.write('<body style="margin: 0px; padding: 0px; font-family: arial, sans-serif;">')

        # out.write('<table width="100%" style="height: 100%;" cellpadding="10" cellspacing="0" border="0">')
        # out.write('<tr>')

        out.write('<!-- ============ HEADER SECTION ============== -->')
        out.write('<table width="100%" cellpadding="10" cellspacing="0" border="0">')
        out.write('<tr>')
        out.write('<td colspan="2" height="80px" bgcolor="#5B7AA7"> ')
        out.write('<font size="5.5" color="#F6DE82" align="center" valign="center"><b>OPEN IRRIGATION</b></font>')
        out.write('</td></tr>')

        out.write('<!-- ============ NAVIGATION BAR SECTION ============== -->')
        out.write('<tr><td colspan="2" valign="middle" height="50" bgcolor=#EBF1FA>')
        out.write('<a href="/index.html" class="StandardButton">HOME</a>')
        out.write('<a href="gardendata.html" class="StandardButton">SETTINGS</a>')

        out.write('<style media="screen" type="text/css">')
        out.write('.StandardButton {')
        out.write('background-color:#1671AE;')
        out.write('-moz-border-radius:4px;')
        out.write('-webkit-border-radius:4px;')
        out.write('border-radius:4px;')
        out.write('border:1px solid #1671AE;')
        out.write('display:inline-block;')
        out.write('cursor:pointer;')
        out.write('color:#F4F6F7;')
        out.write('font-family:Arial;')
        out.write('font-size:12px;')
        out.write('font-weight:bold;')
        out.write('margin: 5px;')
        out.write('padding:10px 16px;')
        out.write('text-decoration:none;')
        out.write('text-shadow:0px 0px 0px #5b8a3c;')
        out.write('}')
        out.write('.StandardButton:hover {')
        out.write('background-color:#1671AE;')
        out.write('}')
        out.write('.StandardButton:active {')
        out.write('position:relative;')
        out.write('top:1px;')
        out.write('}')
        out.write('</style>')
        out.write('</td></tr>')

        out.write('</td></tr>')

        out.write('<tr>')
        out.write('<!-- ============ LEFT COLUMN (MENU) ============== -->')
        out.write('<td width="80%" valign="top" bgcolor=#FAFBFB>')
        if MinT <= 0:
                out.write('<hr>')
                out.write('<style>')
                out.write('header {')
                out.write('background-color: Red ;')
                out.write('}')
                out.write('</style>')
                out.write('<header>')
                out.write('<font size="5" face="arial" color="white"> <div align="center"</br>Warning! Protect system from frost</br></font></div>')
                out.write('</header>')
                out.write('<hr>')
        if MinT > 0 and MinT <= 3:
                out.write('<hr>')
                out.write('<style>')
                out.write('header {')
                out.write('background-color: DarkOrange  ;')
                out.write('}')
                out.write('</style>')
                out.write('<header>')
                out.write('<font size="5" face="arial" color="white"> <div align="center"</br>Caution, Protect system from frost</br></font></div>')
                out.write('</header>')
                out.write('<hr>')
        out.write('<font size="5" face="arial" color="#1671AE"> <div align="center"></br>Overview of supplied water</br></br></font></div>')
        out.write('<style>')
        out.write('body {')
        out.write('background-color: #FAFBFB ;')
        out.write('}')
        out.write('table {')
        out.write('font-family: arial, sans-serif;')
        out.write('color: #4F4F4F;')
        out.write('border-collapse: collapse;')
        out.write('width: 100%;')
        out.write('}')
        out.write('td, th {')
        out.write('border: 1px solid #dddddd;')
        out.write('txt-align: center;')
        out.write('padding: 8px;')
        out.write('}')
        out.write('tr:nth-child(even) {')
        out.write('background-color: #EBF1FA;')
        out.write('}')
        out.write('</style>')
        out.write('<table>')
        out.write('<tr>')
        out.write('<th>Period</th>')
        if valvetype1 is not 0:
            out.write('<th>'+NameValve1+'</th>')
        if valvetype2 is not 0:
            out.write('<th>'+NameValve2+'</th>')
        if valvetype3 is not 0:
            out.write('<th>'+NameValve3+'</th>')
        if valvetype4 is not 0:
            out.write('<th>'+NameValve4+'</th>')
        if valvetype5 is not 0:
            out.write('<th>'+NameValve5+'</th>')
        if valvetype6 is not 0:
            out.write('<th>' + NameValve6 + '</th>')
        if valvetype7 is not 0:
            out.write('<th>' + NameValve7 + '</th>')
        if valvetype8 is not 0:
            out.write('<th>' + NameValve8 + '</th>')
        if valvetype9 is not 0:
            out.write('<th>' + NameValve9 + '</th>')
        if valvetype10 is not 0:
            out.write('<th>' + NameValve10 + '</th>')
        if valvetype11 is not 0:
            out.write('<th>' + NameValve11 + '</th>')
        if valvetype12 is not 0:
            out.write('<th>' + NameValve12 + '</th>')
        if valvetype13 is not 0:
            out.write('<th>' + NameValve13 + '</th>')
        if valvetype14 is not 0:
            out.write('<th>' + NameValve14 + '</th>')
        if valvetype15 is not 0:
            out.write('<th>' + NameValve15 + '</th>')
        if valvetype16 is not 0:
            out.write('<th>' + NameValve16 + '</th>')

        out.write('</tr>')
        out.write('<tr>')
        out.write('<td align="center">This week</td>')
        if valvetype1 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek1))
            out.write('</td>')
        if valvetype2 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek2))
            out.write('</td>')
        if valvetype3 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek3))
            out.write('</td>')
        if valvetype4 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek4))
            out.write('</td>')
        if valvetype5 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek5))
            out.write('</td>')
        if valvetype6 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek6))
            out.write('</td>')
        if valvetype7 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek7))
            out.write('</td>')
        if valvetype8 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek8))
            out.write('</td>')
        if valvetype9 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek9))
            out.write('</td>')
        if valvetype10 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek10))
            out.write('</td>')
        if valvetype11 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek11))
            out.write('</td>')
        if valvetype12 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek12))
            out.write('</td>')
        if valvetype13 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek13))
            out.write('</td>')
        if valvetype14 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek14))
            out.write('</td>')
        if valvetype15 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek15))
            out.write('</td>')
        if valvetype16 is not 0:
            out.write('<td align="center">')
            out.write(str(TotalWaterPastWeek16))
            out.write('</td>')


        out.write('<tr>')
        out.write('<td align="center">Past week</td>')
        if valvetype1 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks1))
                out.write('</td>')
        if valvetype2 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks2))
                out.write('</td>')
        if valvetype3 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks3))
                out.write('</td>')
        if valvetype4 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks4))
                out.write('</td>')
        if valvetype5 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks5))
                out.write('</td>')

        if valvetype6 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks6))
                out.write('</td>')

        if valvetype7 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks7))
                out.write('</td>')

        if valvetype8 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks8))
                out.write('</td>')

        if valvetype9 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks9))
                out.write('</td>')

        if valvetype10 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks10))
                out.write('</td>')

        if valvetype11 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks11))
                out.write('</td>')

        if valvetype12 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks12))
                out.write('</td>')

        if valvetype13 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks13))
                out.write('</td>')

        if valvetype14 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks14))
                out.write('</td>')

        if valvetype15 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks15))
                out.write('</td>')

        if valvetype16 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast2Weeks16))
                out.write('</td>')


        out.write('<tr>')
        out.write('<td align="center">For 2 weeks</td>')
        if valvetype1 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks1))
                out.write('</td>')
        if valvetype2 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks2))
                out.write('</td>')
        if valvetype3 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks3))
                out.write('</td>')
        if valvetype4 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks4))
                out.write('</td>')
        if valvetype5 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks5))
                out.write('</td>')
        if valvetype6 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks6))
                out.write('</td>')
        if valvetype7 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks7))
                out.write('</td>')
        if valvetype8 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks8))
                out.write('</td>')
        if valvetype9 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks9))
                out.write('</td>')
        if valvetype10 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks10))
                out.write('</td>')
        if valvetype11 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks11))
                out.write('</td>')
        if valvetype12 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks12))
                out.write('</td>')
        if valvetype13 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks13))
                out.write('</td>')
        if valvetype14 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks14))
                out.write('</td>')
        if valvetype15 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks15))
                out.write('</td>')
        if valvetype16 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast3Weeks16))
                out.write('</td>')

        out.write('<tr>')
        out.write('<td align="center">For 3 weeks</td>')
        if valvetype1 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks1))
                out.write('</td>')
        if valvetype2 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks2))
                out.write('</td>')
        if valvetype3 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks3))
                out.write('</td>')
        if valvetype4 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks4))
                out.write('</td>')
        if valvetype5 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks5))
                out.write('</td>')
        if valvetype6 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks6))
                out.write('</td>')
        if valvetype7 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks7))
                out.write('</td>')
        if valvetype8 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks8))
                out.write('</td>')
        if valvetype9 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks9))
                out.write('</td>')
        if valvetype10 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks10))
                out.write('</td>')
        if valvetype11 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks11))
                out.write('</td>')
        if valvetype12 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks12))
                out.write('</td>')
        if valvetype13 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks13))
                out.write('</td>')
        if valvetype14 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks14))
                out.write('</td>')
        if valvetype15 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks15))
                out.write('</td>')
        if valvetype16 is not 0:
                out.write('<td align="center">')
                out.write(str(TotalWaterPast4Weeks16))
                out.write('</td>')

        out.write('<tr>')
        out.write('<td align="center"><b>This year</b></td>')
        if valvetype1 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery1))
                out.write('</b></td>')
        if valvetype2 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery2))
                out.write('</b></td>')
        if valvetype3 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery3))
                out.write('</b></td>')
        if valvetype4 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery4))
                out.write('</b></td>')
        if valvetype5 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery5))
                out.write('</b></td>')
        if valvetype6 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery6))
                out.write('</b></td>')
        if valvetype7 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery7))
                out.write('</b></td>')
        if valvetype8 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery8))
                out.write('</b></td>')
        if valvetype9 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery9))
                out.write('</b></td>')
        if valvetype10 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery10))
                out.write('</b></td>')
        if valvetype11 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery11))
                out.write('</b></td>')
        if valvetype12 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery12))
                out.write('</b></td>')
        if valvetype13 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery13))
                out.write('</b></td>')
        if valvetype14 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery14))
                out.write('</b></td>')
        if valvetype15 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery15))
                out.write('</b></td>')
        if valvetype16 is not 0:
                out.write('<td align="center"><b>')
                out.write(str(TotalWatery16))
                out.write('</b></td>')

        out.write('</table>')

        out.write('<font size="5" face="arial" color="#1671AE"> <div align="center"></br>Fertilizer Overview</br></br></font></div>')

        out.write('<table>')
        out.write('<tr>')
        out.write('<th>Month</th>')
        out.write('<th>NPK Amount (Kg)</th>')
        out.write('<th>Compost Amount (Kg)</th>')
        out.write('<th>Patentkalie Amount (Kg)</th>')
        out.write('</tr>')
        out.write('<tr>')
        out.write('<td align="center">March</td>')
        out.write('<td align="center">')
        out.write(march)
        out.write('</td>')
        out.write('<td align="center">')
        out.write(compost1)
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<tr>')
        out.write('<td align="center">April</td>')
        out.write('<td align="center">')
        out.write(april)
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<tr>')
        out.write('<td align="center">May</td>')
        out.write('<td align="center">')
        out.write(may)
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<tr>')
        out.write('<td align="center">June</td>')
        out.write('<td align="center">')
        out.write(june)
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<tr>')
        out.write('<td align="center">July</td>')
        out.write('<td align="center">')
        out.write(july)
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<tr>')
        out.write('<td align="center">August</td>')
        out.write('<td align="center">')
        out.write(august)
        out.write('</td>')
        out.write('<td align="center">')
        out.write('  ')
        out.write('</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<tr>')
        out.write('<td align="center">September</td>')
        out.write('<td align="center">')
        out.write(' ')
        out.write('</td>')
        out.write('<td align="center">')
        out.write(compost2)
        out.write('</td>')
        out.write('<td align="center">')
        out.write(patentkali)
        out.write('</td>')
        out.write('</table>')

        out.write('<!-- ============ RIGHT COLUMN (CONTENT) ============== -->')
        out.write('<td width="20%" valign="top" bgcolor=#FAFBFB>')
        out.write('<font size="5" face="arial" color="#1671AE"> <div align="center"></br>Today\'s Information</br></br></font></div>')
        out.write('<div align="center"><font size="2">Average temperature&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font><br>')
        out.write('<font size="7">'+str(avgtemp)+'</font> <sup>o</sup>C</div>')
        out.write('<br>')
        if rainfallpast24hrs > 0:
                out.write('<hr>')
                out.write('<div align="center"><font size="2">Rainfall past 24 hrs: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font><br>')
                out.write('<font size="4">'+str(rainfallpast24hrs)+'</font> mm<br>')
        if int(RainForecast) > 0:
                out.write('<hr>')
                out.write('<div align="center"><font size="2">Rain forecasted: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font><br>')
                out.write('<font size="4">'+str(RainForecast)+'</font> mm<br>')
        out.write('<hr>')
        out.write('<br>')

        out.write('<i>T effect on growth:<br>')
        out.write('50% is optimal.<br>')
        out.write('Left is cold and right is warm.</i>')
        out.write('<br>')

        if valvetype1 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve1+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT1)/ float(GrowthMaxT1-GrowthMinT1)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount1)+' mm<br>')
                if valvetype1 == 1:
                        out.write('<meter value="'+str(irrigationcount1 / float(2))+'"></meter><br>')
                if valvetype1 == 2:
                        out.write('<meter value="'+str(irrigationcount1 / float(5))+'"></meter><br>')

        if valvetype2 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve2+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT2)/ float(GrowthMaxT2-GrowthMinT2)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount2)+' mm<br>')
                if valvetype2 == 1:
                        if float(irrigationamount2) > 0:
                                out.write('<meter value="'+str(irrigationcount2 / float(2))+'"></meter><br>')
                if valvetype2 == 2:
                        out.write('<meter value="'+str(irrigationcount2 / float(5))+'"></meter><br>')

        if valvetype3 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve3+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT3)/ float(GrowthMaxT3-GrowthMinT3)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount3)+' mm<br>')
                if valvetype3 == 1:
                        if float(irrigationamount3) > 0:
                                out.write('<meter value="'+str(irrigationcount3 / float(2))+'"></meter><br>')
                if valvetype3 == 2:
                        out.write('<meter value="'+str(irrigationcount3 / float(5))+'"></meter><br>')
                out.write('<br>')

        if valvetype4 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve4+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT4)/ float(GrowthMaxT4-GrowthMinT4)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount4)+' mm<br>')
                if valvetype4 == 1:
                        if float(irrigationamount4) > 0:
                                out.write('<meter value="'+str(irrigationcount4 / float(2))+'"></meter><br>')
                if valvetype4 == 2:
                        out.write('<meter value="'+str(irrigationcount4 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype5 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve5+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT5)/ float(GrowthMaxT5-GrowthMinT5)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount5)+' mm<br>')
                if valvetype5 == 1:
                        if float(irrigationamount5) > 0:
                                out.write('<meter value="'+str(irrigationcount5 / float(2))+'"></meter><br>')
                if valvetype5 == 2:
                        out.write('<meter value="'+str(irrigationcount5 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype6 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve6+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT6)/ float(GrowthMaxT6-GrowthMinT6)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount6)+' mm<br>')
                if valvetype6 == 1:
                        if float(irrigationamount6) > 0:
                                out.write('<meter value="'+str(irrigationcount6 / float(2))+'"></meter><br>')
                if valvetype6 == 2:
                        out.write('<meter value="'+str(irrigationcount6 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype7 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve7+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT7)/ float(GrowthMaxT7-GrowthMinT7)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount7)+' mm<br>')
                if valvetype7 == 1:
                        if float(irrigationamount7) > 0:
                                out.write('<meter value="'+str(irrigationcount7 / float(2))+'"></meter><br>')
                if valvetype7 == 2:
                        out.write('<meter value="'+str(irrigationcount7 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype8 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve8+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT8)/ float(GrowthMaxT8-GrowthMinT8)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount8)+' mm<br>')
                if valvetype8 == 1:
                        if float(irrigationamount8) > 0:
                                out.write('<meter value="'+str(irrigationcount8 / float(2))+'"></meter><br>')
                if valvetype8 == 2:
                        out.write('<meter value="'+str(irrigationcount8 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype9 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve9+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT9)/ float(GrowthMaxT9-GrowthMinT9)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount9)+' mm<br>')
                if valvetype9 == 1:
                        if float(irrigationamount9) > 0:
                                out.write('<meter value="'+str(irrigationcount9 / float(2))+'"></meter><br>')
                if valvetype9 == 2:
                        out.write('<meter value="'+str(irrigationcount9 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype10 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve10+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT10)/ float(GrowthMaxT10-GrowthMinT10)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount10)+' mm<br>')
                if valvetype10 == 1:
                        if float(irrigationamount10) > 0:
                                out.write('<meter value="'+str(irrigationcount10 / float(2))+'"></meter><br>')
                if valvetype10 == 2:
                        out.write('<meter value="'+str(irrigationcount10 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype11 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve11+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT11)/ float(GrowthMaxT11-GrowthMinT11)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount11)+' mm<br>')
                if valvetype11 == 1:
                        if float(irrigationamount11) > 0:
                                out.write('<meter value="'+str(irrigationcount11 / float(2))+'"></meter><br>')
                if valvetype11 == 2:
                        out.write('<meter value="'+str(irrigationcount11 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype12 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve12+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT12)/ float(GrowthMaxT12-GrowthMinT12)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount12)+' mm<br>')
                if valvetype12 == 1:
                        if float(irrigationamount12) > 0:
                                out.write('<meter value="'+str(irrigationcount12 / float(2))+'"></meter><br>')
                if valvetype12 == 2:
                        out.write('<meter value="'+str(irrigationcount12 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype13 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve13+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT13)/ float(GrowthMaxT13-GrowthMinT13)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount13)+' mm<br>')
                if valvetype13 == 1:
                        if float(irrigationamount13) > 0:
                                out.write('<meter value="'+str(irrigationcount13 / float(2))+'"></meter><br>')
                if valvetype13 == 2:
                        out.write('<meter value="'+str(irrigationcount13 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype14 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve14+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT14)/ float(GrowthMaxT14-GrowthMinT14)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount14)+' mm<br>')
                if valvetype14 == 1:
                        if float(irrigationamount14) > 0:
                                out.write('<meter value="'+str(irrigationcount14 / float(2))+'"></meter><br>')
                if valvetype14 == 2:
                        out.write('<meter value="'+str(irrigationcount14 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype15 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve15+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT15)/ float(GrowthMaxT15-GrowthMinT15)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount15)+' mm<br>')
                if valvetype15 == 1:
                        if float(irrigationamount15) > 0:
                                out.write('<meter value="'+str(irrigationcount15 / float(2))+'"></meter><br>')
                if valvetype15 == 2:
                        out.write('<meter value="'+str(irrigationcount15 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')
        if valvetype16 is not 0:
                out.write('<br>')
                out.write('<b>'+NameValve16+':</b><br>')
                growthfactor = (float(avgtemp)-GrowthMinT16)/ float(GrowthMaxT16-GrowthMinT16)
                out.write('T effect on growth:')
                out.write('<meter low=".25" optimum=".5" high=".75" value= '+str(growthfactor)+' ></meter><br>')
                out.write('Irrigation: '+str(irrigationamount16)+' mm<br>')
                if valvetype16 == 1:
                        if float(irrigationamount16) > 0:
                                out.write('<meter value="'+str(irrigationcount16 / float(2))+'"></meter><br>')
                if valvetype16 == 2:
                        out.write('<meter value="'+str(irrigationcount16 / float(5))+'"></meter><br>')
                out.write('<br>')
                out.write('<hr>')

        out.write('<!-- ============ FOOTER SECTION ============== -->')
        out.write('<tr><td colspan="2" align="center" height="20" bgcolor=#FAFBFB></td></tr>')
        out.write('</table>')
        out.write('</body>')

        out.write('<html>')
print ('the page was sucessfully generated')
exit()