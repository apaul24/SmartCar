from __future__ import print_function
from datetime import date, datetime
import time, sys, os, mysql.connector
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

while True:
    #Ask user for type of analysis (Cumulative and/or By trip)
    analysisType = input("Enter type of analysis (1 = Cumulative; 2 = By trip; 3 = Quit): ")

    #Plot statistical graphs of cumulative data read from MySQL database
    if analysisType != 3:
        
        print ("Now plotting data...")

        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, analysisType, "rpm_table", True),
            "RPM",
            analysisType
            )
        
        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, analysisType, "engine_load_table", True),
            "Engine Load",
            analysisType
            )
        
        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, analysisType, "speed_table", True),
            "Speed",
            analysisType
            )

        smartCar.plotData(
            smartCar.readParameterData(ms.cursor, analysisType, "coolant_temp_table", True),
            "Coolant Temperature",
            analysisType
            )
        
        print ("Data plotted online successfully!")
        
    elif analysisType == 3:
	ms.cursor.close()
	ms.cnx.close()
	print ("System is OK to shutdown.")
        break
