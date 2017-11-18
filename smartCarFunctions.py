from __future__ import print_function
from datetime import date, datetime
import time, sys, obd, os, mysql.connector
import plotly as py
from plotly.graph_objs import *
import mysqlConfig as ms

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
    ms.cursor.execute(add_rpm, data_rpm)
    ms.cnx.commit()
    time.sleep(0.142)

#Update fuel_level_table
def new_fuel_level(fl):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_fuel_level = ("INSERT INTO fuel_level_table (fuel_level, time_stamp) VALUES (%s, %s)")
    data_fuel_level = (round(fl.value.magnitude, 2), now)
    ms.cursor.execute(add_fuel_level, data_fuel_level)
    ms.cnx.commit()
    time.sleep(0.142)

#Update engine_load_table
def new_engine_load(e):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_engine_load = ("INSERT INTO engine_load_table (engine_load, time_stamp) VALUES (%s, %s)")
    data_engine_load = (round(e.value.magnitude, 2), now)
    ms.cursor.execute(add_engine_load, data_engine_load)
    ms.cnx.commit()
    time.sleep(0.142)

#Update speed_table
def new_speed(s):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_speed = ("INSERT INTO speed_table (speed, time_stamp) VALUES (%s, %s)")
    data_speed = (s.value.magnitude, now)
    ms.cursor.execute(add_speed, data_speed)
    ms.cnx.commit()
    time.sleep(0.142)

#Update air_flow_table
def new_air_flow(af):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_air_flow = ("INSERT INTO air_flow_table (air_flow, time_stamp) VALUES (%s, %s)")
    data_air_flow = (round(af.value.magnitude, 2), now)
    cursor.execute(add_air_flow, data_air_flow)
    cnx.commit()
    time.sleep(0.142)

#Update throttle_position_table
def new_throttle_position(tp):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_throttle_position = ("INSERT INTO throttle_position_table (throttle_position, time_stamp) VALUES (%s, %s)")
    data_throttle_position = (round(tp.value.magnitude, 2), now)
    cursor.execute(add_throttle_position, data_throttle_position)
    cnx.commit()
    time.sleep(0.142)

#Update coolant_temp_table
def new_coolant_temp(ct):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_coolant_temp = ("INSERT INTO coolant_temp_table (coolant_temp, time_stamp) VALUES (%s, %s)")
    data_coolant_temp = (round(((ct.value.magnitude * 1.8) + 32), 2), now) #convert temp from C to F
    cursor.execute(add_coolant_temp, data_coolant_temp)
    cnx.commit()
    time.sleep(0.142)


#Query rpm data from MySQL database
def readRPMData(cursor):
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
def readFuelLevelData(cursor):
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
def readEngineLoadData(cursor):
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
def readSpeedData(cursor):
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

#Query air flow data from MySQL database
def readAirFlowData(cursor):
    query = ("SELECT air_flow, time_stamp FROM air_flow_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    air_flow_data = []
    time_stamp_data = []

    #Read data into lists
    for (air_flow, time_stamp) in cursor:
        air_flow_data.append(air_flow)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=air_flow_data)
    data = Data([trace])
    return data
        
#Plot air flow graph online
def plotAirFlowData(data):
    py.plotly.plot(data, filename = 'Air Flow Rate vs. Time')

#Query throttle position data from MySQL database
def readThrottlePositionData(cursor):
    query = ("SELECT throttle_position, time_stamp FROM throttle_position_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    throttle_position_data = []
    time_stamp_data = []

    #Read data into lists
    for (throttle_position, time_stamp) in cursor:
        throttle_position_data.append(throttle_position)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=throttle_position_data)
    data = Data([trace])
    return data
        
#Plot throttle position graph online
def plotThrottlePositionData(data):
    py.plotly.plot(data, filename = 'Throttle Position vs. Time')

#Query coolant temperature data from MySQL database
def readCoolantTempData(cursor):
    query = ("SELECT coolant_temp, time_stamp FROM coolant_temp_table")
    cursor.execute(query)

    #Initialize empty lists to store data
    coolant_temp_data = []
    time_stamp_data = []

    #Read data into lists
    for (coolant_temp, time_stamp) in cursor:
        coolant_temp_data.append(coolant_temp)
        time_stamp_data.append(time_stamp)
        
    #Create a trace from the collected data
    trace = Scatter(x=time_stamp_data, y=coolant_temp_data)
    data = Data([trace])
    return data
        
#Plot coolant temperature graph online
def plotCoolantTempData(data):
    py.plotly.plot(data, filename = 'Engine Coolant Temperature vs. Time')




