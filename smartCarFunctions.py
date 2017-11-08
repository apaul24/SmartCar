from __future__ import print_function
from datetime import date, datetime
import time, sys, obd, os, mysql.connector
import plotly as py
from plotly.graph_objs import *

######## Functions ########

#Update rpm_table
def new_rpm(r):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_rpm = ("INSERT INTO rpm_table (rpm, time_stamp) VALUES (%s, %s)")
    data_rpm = (r.value.magnitude, now)
    cursor.execute(add_rpm, data_rpm)
    cnx.commit()
    time.sleep(0.5)

#Update fuel_level_table
def new_fuel(f):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_fuel_level = ("INSERT INTO fuel_level_table (fuel_level, time_stamp) VALUES (%s, %s)")
    data_fuel_level = (round(f.value.magnitude, 2), now)
    cursor.execute(add_fuel_level, data_fuel_level)
    cnx.commit()
    time.sleep(0.5)

#Query data from MySQL database
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
        
#Plot graphs online
def plotRPMData(data):
    py.plotly.plot(data, filename = 'RPM vs. Time')

#Set credentials for plotly in order to plot online
def plotlyLogin(userName, apiKey):    
    py.tools.set_credentials_file(username=userName, api_key=apiKey)
    
#Connect to MySQL database and return cnx (localhost is default host)
def mysqlConnect(userName, password, database, host='localhost'):
try:
    cnx = mysql.connector.connect(user=username, password=password, host=host, database=database)

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


