from __future__ import print_function
from datetime import date, datetime
import time, sys, obd, os, mysql.connector
import plotly as py
from plotly.graph_objs import *
import mysqlConfig as ms
import smartCarFunctions as smartCar
from ConfigParser import SafeConfigParser

#Open .config file to read in credentials for MySQL and Plotly
parser = SafeConfigParser()
parser.read('smartCar.config')

#Plotly credentials
plotlyUser = parser.get('Plotly', 'username')
apiKey = parser.get('Plotly', 'api_key')

#MySQL credentials
mysqlUser = parser.get('MySQL', 'username')
mysqlPassword = parser.get('MySQL', 'password')
mysqlHost = parser.get('MySQL', 'host')
mysqlDatabase = parser.get('MySQL', 'database')
    
#Set credentials for plotly in order to plot online
smartCar.plotlyLogin(plotlyUser, apiKey)
    
#Connect to MySQL database
ms.cnx = smartCar.mysqlConnect(mysqlUser, mysqlPassword, mysqlDatabase, mysqlHost)
ms.cursor = ms.cnx.cursor()

#Grab last row number in MySQL to be able to append new raw data to Plotly
query = ("SELECT id FROM rpm_table ORDER by time_stamp, id")
i = (1,0) #If table is empty, set row number to 1
ms.cursor.execute(query)
for (i) in ms.cursor:
    pass
ms.lastRowNum = i[0]

#Auto connect to OBD scanner
connection = obd.Async()

#Check if connected to OBD scanner
if connection.is_connected():
    print("Car Connected!")
    print("Protocol: {}".format(connection.protocol_name()))

    #Read in fuel level while car is idle
    connection.watch(obd.commands.FUEL_LEVEL, callback=smartCar.new_fuel_level)
    connection.start()
    print("Reading fuel level...")
    time.sleep(1)
    connection.stop()
    print("Fuel level read successfully!")

    #Unsubscribe from fuel level parameter
    connection.unwatch(obd.commands.FUEL_LEVEL, callback=smartCar.new_fuel_level)

    #Choose parameters to monitor while driving
    connection.watch(obd.commands.RPM, callback=smartCar.new_rpm)
    connection.watch(obd.commands.ENGINE_LOAD, callback=smartCar.new_engine_load)
    connection.watch(obd.commands.SPEED, callback=smartCar.new_speed)
    connection.watch(obd.commands.COOLANT_TEMP, callback=smartCar.new_coolant_temp)

    #Start monitoring
    connection.start()
    print("Now monitoring. OK to drive.")

    #Keep monitoring until user enters CTRL+C
    try:
        while 1:
            pass   
    except KeyboardInterrupt:
        
        #Stop monitoring and unsubscribe from parameters 
        connection.stop()
        connection.unwatch_all()
        
        #Read in fuel level while car is idle
        connection.watch(obd.commands.FUEL_LEVEL, callback=smartCar.new_fuel_level)
        connection.start()
        print("Reading fuel level...")
        time.sleep(1)
        connection.stop()
        print("Fuel level read successfully!")
        
        #Stop monitoring fuel level and close connection to OBD scanner
        print ("Closing connection to OBD scanner...")
        connection.unwatch_all()
        connection.close()
        print ("Connection closed successfully!")

        #Mark end of trip in MySQL table for each parameter
        time.sleep(1)
        smartCar.markEndOfTrip("rpm", "rpm_table")
        smartCar.markEndOfTrip("fuel_level", "fuel_level_table")
        smartCar.markEndOfTrip("engine_load", "engine_load_table")
        smartCar.markEndOfTrip("speed", "speed_table")
        smartCar.markEndOfTrip("coolant_temp", "coolant_temp_table")
        
        #Plot raw data read from MySQL database and close connection
        print ("Now plotting data...")
        
        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, ms.lastRowNum, 1, "rpm_table", False),
            "RPM",
            0)
        
        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, ms.lastRowNum, 1, "fuel_level_table", False),
            "Fuel Level",
            0)
        
        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, ms.lastRowNum, 1, "engine_load_table", False),
            "Engine Load",
            0)
        
        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, ms.lastRowNum, 1, "speed_table", False),
            "Speed",
            0)
        
        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, ms.lastRowNum, 1, "coolant_temp_table", False),
            "Coolant Temperature",
            0)
        
        print ("Data plotted online successfully!")
        ms.cursor.close()
        ms.cnx.close()
    
        #Prompt user to shut down system
        print ("System is OK to shutdown.")

else:
    print("Unable to connect with car.")

    #Close connection with MySQL
    ms.cursor.close()
    ms.cnx.close()
