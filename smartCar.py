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

#Auto connect to OBD scanner
connection = obd.Async()

#Check if connected to OBD scanner
if connection.is_connected():
    print("Car Connected!")
    print("Protocol: {}".format(connection.protocol_name()))
    print("Now monitoring...\n")

    #Choose parameters to monitor
    connection.watch(obd.commands.RPM, callback=smartCar.new_rpm)
    connection.watch(obd.commands.FUEL_LEVEL, callback=smartCar.new_fuel_level)
    connection.watch(obd.commands.ENGINE_LOAD, callback=smartCar.new_engine_load)
    connection.watch(obd.commands.SPEED, callback=smartCar.new_speed)
    connection.watch(obd.commands.MAF, callback=smartCar.new_air_flow)
    connection.watch(obd.commands.THROTTLE_POS, callback=smartCar.new_throttle_position)
    connection.watch(obd.commands.COOLANT_TEMP, callback=smartCar.new_coolant_temp)

    #Start monitoring
    connection.start()

    #Keep monitoring until user enters CTRL+C
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        #Stop monitoring and close connection to OBD scanner
        print ("Closing connection to OBD scanner...")
        connection.stop()
        connection.unwatch_all()
        connection.close()
        print ("Connection closed successfully!")
        
        #Plot data read from MySQL database and close connection
        print ("Now plotting data...")
        smartCar.plotRPMData(smartCar.readRPMData(ms.cursor))
        smartCar.plotFuelLevelData(smartCar.readFuelLevelData(ms.cursor))
        smartCar.plotEngineLoadData(smartCar.readEngineLoadData(ms.cursor))
        smartCar.plotSpeedData(smartCar.readSpeedData(ms.cursor))
        smartCar.plotAirFlowData(smartCar.readAirFlowData(ms.cursor))
        smartCar.plotThrottlePositionData(smartCar.readThrottlePositionData(ms.cursor))
        smartCar.plotCoolantTempData(smartCar.readCoolantTempData(ms.cursor))
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
