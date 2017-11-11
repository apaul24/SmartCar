from __future__ import print_function
from datetime import date, datetime
import time, sys, obd, os, mysql.connector
import plotly as py
from plotly.graph_objs import *

################# Functions ####################

#Set credentials for plotly in order to plot online
def plotlyLogin(userName, apiKey):    
    py.tools.set_credentials_file(username=userName, api_key=apiKey)
    
#Connect to MySQL database and return cnx (localhost is default host)
def mysqlConnect(userName, password, database, host='localhost'):
    try:
        cnx = mysql.connector.connect(user=userName, password=password, host=host, database=database)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name and password.")
            sys.exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
            sys.exit()
        else:
            print(err)
            sys.exit()
    else:       
        return cnx

#Update rpm_table
def new_rpm(r):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_rpm = ("INSERT INTO rpm_table (rpm, time_stamp) VALUES (%s, %s)")
    data_rpm = (r.value.magnitude, now)
    cursor.execute(add_rpm, data_rpm)
    cnx.commit()
    time.sleep(0.5)

#Update fuel_level_table
def new_fuel_level(fl):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_fuel_level = ("INSERT INTO fuel_level_table (fuel_level, time_stamp) VALUES (%s, %s)")
    data_fuel_level = (round(fl.value.magnitude, 2), now)
    cursor.execute(add_fuel_level, data_fuel_level)
    cnx.commit()
    time.sleep(0.5)

#Update engine_load_table
def new_engine_load(e):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_engine_load = ("INSERT INTO engine_load_table (engine_load, time_stamp) VALUES (%s, %s)")
    data_engine_load = (round(e.value.magnitude, 2), now)
    cursor.execute(add_engine_load, data_engine_load)
    cnx.commit()
    time.sleep(0.5)

#Update speed_table
def new_speed(s):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_speed = ("INSERT INTO speed_table (speed, time_stamp) VALUES (%s, %s)")
    data_speed = (s.value.magnitude, now)
    cursor.execute(add_speed, data_speed)
    cnx.commit()
    time.sleep(0.5)

#Update oil_temp_table
def new_oil_temp(o):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_oil_temp = ("INSERT INTO oil_temp_table (oil_temp, time_stamp) VALUES (%s, %s)")
    data_oil_temp = (round((((o.value.magnitude * 9) / 5) + 32), 2), now) #convert from C to F
    cursor.execute(add_oil_temp, data_oil_temp)
    cnx.commit()
    time.sleep(0.5)

#Update fuel_rate_table
def new_fuel_rate(fr):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_fuel_rate = ("INSERT INTO fuel_rate_table (fuel_rate, time_stamp) VALUES (%s, %s)")
    data_fuel_rate = (round((fr.value.magnitude / 3.78541), 2), now) #convert from liter/hour to gallons/hour
    cursor.execute(add_fuel_rate, data_fuel_rate)
    cnx.commit()
    time.sleep(0.5)

#Query rpm data from MySQL database
def readRPMData():
    query = ("SELECT rpm, time_stamp FROM rpm_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    rpm_data = []
    time_stamp_data = []

    #Read data into lists
    for (rpm, time_stamp) in cursor:
        rpm_data.append(rpm)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=rpm_data)
    data = Data([trace])
    return data
        
#Plot rpm graph online
def plotRPMData(data):
    py.plotly.plot(data, filename = 'RPM vs. Time')

#Query fuel level data from MySQL database
def readFuelLevelData():
    query = ("SELECT fuel_level, time_stamp FROM fuel_level_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    fuel_level_data = []
    time_stamp_data = []

    #Read data into lists
    for (fuel_level, time_stamp) in cursor:
        fuel_level_data.append(fuel_level)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=fuel_level_data)
    data = Data([trace])
    return data
        
#Plot fuel level graph online
def plotFuelLevelData(data):
    py.plotly.plot(data, filename = 'Fuel Level vs. Time')

#Query engine load data from MySQL database
def readEngineLoadData():
    query = ("SELECT engine_load, time_stamp FROM engine_load_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    engine_load_data = []
    time_stamp_data = []

    #Read data into lists
    for (engine_load, time_stamp) in cursor:
        engine_load_data.append(engine_load)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=engine_load_data)
    data = Data([trace])
    return data
        
#Plot engine load graph online
def plotEngineLoadData(data):
    py.plotly.plot(data, filename = 'Engine Load vs. Time')

#Query speed data from MySQL database
def readSpeedData():
    query = ("SELECT speed, time_stamp FROM speed_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    speed_data = []
    time_stamp_data = []

    #Read data into lists
    for (speed, time_stamp) in cursor:
        speed_data.append(speed)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=speed_data)
    data = Data([trace])
    return data
        
#Plot speed graph online
def plotSpeedData(data):
    py.plotly.plot(data, filename = 'Speed vs. Time')

#Query oil temp data from MySQL database
def readOilTempData():
    query = ("SELECT oil_temp, time_stamp FROM oil_temp_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    oil_temp_data = []
    time_stamp_data = []

    #Read data into lists
    for (oil_temp, time_stamp) in cursor:
        oil_temp_data.append(oil_temp)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=oil_temp_data)
    data = Data([trace])
    return data
        
#Plot oil temp graph online
def plotOilTempData(data):
    py.plotly.plot(data, filename = 'Oil Temperature vs. Time')

#Query fuel rate data from MySQL database
def readFuelRateData():
    query = ("SELECT fuel_rate, time_stamp FROM fuel_rate_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    fuel_rate_data = []
    time_stamp_data = []

    #Read data into lists
    for (fuel_rate, time_stamp) in cursor:
        fuel_rate_data.append(fuel_rate)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=fuel_rate_data)
    data = Data([trace])
    return data
        
#Plot fuel rate graph online
def plotFuelRateData(data):
    py.plotly.plot(data, filename = 'Fuel Rate vs. Time')




