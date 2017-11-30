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
    if not r.is_null():
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        endOfTrip = False
        add_rpm = ("INSERT INTO rpm_table (rpm, time_stamp, end_of_trip) VALUES (%s, %s, %s)")
        data_rpm = (r.value.magnitude, now, endOfTrip)
        ms.cursor.execute(add_rpm, data_rpm)
        ms.cnx.commit()
        time.sleep(0.14)
    else:
        return
            
#Update fuel_level_table
def new_fuel_level(fl):
    if not fl.is_null():
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        endOfTrip = False
        add_fuel_level = ("INSERT INTO fuel_level_table (fuel_level, time_stamp, end_of_trip) VALUES (%s, %s, %s)")
        data_fuel_level = (round(fl.value.magnitude, 2), now, endOfTrip)
        ms.cursor.execute(add_fuel_level, data_fuel_level)
        ms.cnx.commit()
        time.sleep(0.14)
    else:
        return

#Update engine_load_table
def new_engine_load(e):
    if not e.is_null():
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        endOfTrip = False
        add_engine_load = ("INSERT INTO engine_load_table (engine_load, time_stamp, end_of_trip) VALUES (%s, %s, %s)")
        data_engine_load = (round(e.value.magnitude, 2), now, endOfTrip)
        ms.cursor.execute(add_engine_load, data_engine_load)
        ms.cnx.commit()
        time.sleep(0.14)
    else:
        return

#Update speed_table
def new_speed(s):
    if not s.is_null():
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        endOfTrip = False
        add_speed = ("INSERT INTO speed_table (speed, time_stamp, end_of_trip) VALUES (%s, %s, %s)")
        data_speed = (s.value.magnitude, now, endOfTrip)
        ms.cursor.execute(add_speed, data_speed)
        ms.cnx.commit()
        time.sleep(0.14)
    else:
        return

#Update air_flow_table
def new_air_flow(af):
    if not af.is_null():
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        endOfTrip = False
        add_air_flow = ("INSERT INTO air_flow_table (air_flow, time_stamp, end_of_trip) VALUES (%s, %s, %s)")
        data_air_flow = (round(af.value.magnitude, 2), now, endOfTrip)
        ms.cursor.execute(add_air_flow, data_air_flow)
        ms.cnx.commit()
        time.sleep(0.14)
    else:
        return

#Update throttle_position_table
def new_throttle_position(tp):
    if not tp.is_null():
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        endOfTrip = False
        add_throttle_position = ("INSERT INTO throttle_position_table (throttle_position, time_stamp, end_of_trip) VALUES (%s, %s, %s)")
        data_throttle_position = (round(tp.value.magnitude, 2), now, endOfTrip)
        ms.cursor.execute(add_throttle_position, data_throttle_position)
        ms.cnx.commit()
        time.sleep(0.14)
    else:
        return

#Update coolant_temp_table
def new_coolant_temp(ct):
    if not ct.is_null():
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        endOfTrip = False
        add_coolant_temp = ("INSERT INTO coolant_temp_table (coolant_temp, time_stamp, end_of_trip) VALUES (%s, %s, %s)")
        data_coolant_temp = (round(((ct.value.magnitude * 1.8) + 32), 2), now, endOfTrip) #convert temp from C to F
        ms.cursor.execute(add_coolant_temp, data_coolant_temp)
        ms.cnx.commit()
        time.sleep(0.14)
    else:
        return

#Update parameter table for end of trip
def markEndOfTrip(parameterName, tableName):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    endOfTrip = True
    add_test = ("INSERT INTO {} ({}, time_stamp, end_of_trip) VALUES (%s, %s, %s)".format(tableName, parameterName))
    data_test = (0, now, endOfTrip)
    ms.cursor.execute(add_test, data_test)
    ms.cnx.commit()

#Query parameter data from MySQL database
def readParameterData(cursor, lastRowNum, analysisType, tableName, hist):

    #Initialize empty list to store parameter and time_stamp data
    parameter_data = []

    #Read data into list either (1) cumulatively or (2) by trip
    if analysisType == 1:
        #Select new data in MySQL to be appended to existing trace if it already exists
        query = ("SELECT * FROM {} LIMIT {},18446744073709551615".format(tableName, lastRowNum-1))
        ms.cursor.execute(query)

        #Read in new data from MySQL into parameter list
        for (i, parameter, time_stamp, end_of_trip) in cursor:
            if end_of_trip == False:
                parameter_data.append((parameter, time_stamp))
            elif end_of_trip == True:
                pass

        #Initialize empty lists to store x-data and y-data
        x_data = []
        y_data = []

        #Read parameter data into x_data and y_data lists
        for i in parameter_data:
            y_data.append(i[0])
            x_data.append(i[1])

        #Append null value so graph will plot with gaps
        y_data.append(None)
        x_data.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        #Check if plotting histogram or line plot
        if hist == True:
            #Create histogram trace for all data
            trace = Histogram(x=y_data, histnorm='probability')
        elif hist == False:        
            #Create line trace for all data
            trace = Scatter(x=x_data, y=y_data)
            
        data = [trace]
        return data
            
    elif analysisType == 2:  
        #Select all data in MySQL to be read by trip
        query = ("SELECT * FROM {}".format(tableName))
        ms.cursor.execute(query)

        #Read in data from MySQL into parameter list, but divide data by trip using '-'        
        for (i, parameter, time_stamp, end_of_trip) in cursor:
            if end_of_trip == False:
                parameter_data.append(parameter)
            elif end_of_trip == True:
                parameter_data.append('-')

        #Initialize empty lists to store y-data
        y_data = []
        traces = []

        #Read data in y_data list for each trip
        for i in parameter_data:
            if i != '-':
                y_data.append(i)
            elif i == '-':                
                #Create histogram trace for trip
                t = Histogram(x=y_data, histnorm='probability', opacity=0.75)
                traces.append(t)
                data = traces

                #Clear y_data to read in next trip if necessary
                y_data = []

        return data
        
#Plot graph for parameter data (raw data, histogram, or histogram per trip) online
def plotData(data, parameterName, analysisType):
    if analysisType == 0:
        py.plotly.plot(data, filename = '{} vs. Time'.format(parameterName), fileopt='extend', auto_open=False)
                
    elif analysisType == 2:
        layout = Layout(barmode='overlay')
        fig = Figure(data=data, layout=layout)
        py.plotly.plot(fig, filename = '{} Histogram per Trip'.format(parameterName), auto_open=False)
                
    elif analysisType == 1:
        py.plotly.plot(data, filename = '{} Overall Histogram'.format(parameterName), fileopt='extend', auto_open=False)

