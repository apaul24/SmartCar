from __future__ import print_function
from datetime import date, datetime
import time, sys, obd, os, mysql.connector
import plotly as py
from plotly.graph_objs import *
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
cnx = smartCar.mysqlConnect(mysqlUser, mysqlPassword, mysqlDatabase, mysqlHost)
cursor = cnx.cursor()

#Auto connect to OBD scanner
connection = obd.Async()

#Check if connected to OBD scanner
if connection.is_connected():
    print("Car Connected!")
    print("Protocol: {}".format(connection.protocol_name()))
    print("Now monitoring...\n")

    #Choose parameters to monitor
    connection.watch(obd.commands.RPM, callback=new_rpm)
    connection.watch(obd.commands.FUEL_LEVEL, callback=new_fuel_level)
    connection.watch(obd.commands.ENGINE_LOAD, callback=new_engine_load)
    connection.watch(obd.commands.SPEED, callback=new_speed)
    connection.watch(obd.commands.OIL_TEMP, callback=new_oil_temp)
    connection.watch(obd.commands.FUEL_RATE, callback=new_fuel_rate)

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
        smartCar.plotRPMData(smartCar.readRPMData())
        smartCar.plotFuelLevelData(smartCar.readFuelLevelData())
        smartCar.plotEngineLoadData(smartCar.readEngineLoadData())
        smartCar.plotSpeedData(smartCar.readSpeedData())
        smartCar.plotOilTempData(smartCar.readOilTempData())
        smartCar.plotFuelRateData(smartCar.readFuelRateData())
        print ("Data plotted online successfully!")
        cursor.close()
        cnx.close()
    
        #Prompt user to shut down system
        print ("System is OK to shutdown.")

else:
    print("Unable to connect with car.")

    #Close connection with MySQL
    cursor.close()
    cnx.close()
