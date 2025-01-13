
import minimalmodbus
import pandas as pd 
import plotly
import matplotlib.pyplot as plt
import datetime 
import numpy as np
import time
from dash import Dash, dcc, Input, Output, callback, html
import requests
import json



import os

from google.cloud.sql.connector import Connector, IPTypes
import pymysql

import sqlalchemy

#connecting to cloud sql








# initilize soil sensor-----------------------------------------------------
PORT='COM3'

#register numbers based on rs458 protocol
N_reg= 30
P_reg=31
K_reg=32
PH_reg=6
humidity_reg=18
temp_reg=19
cond_reg=21

values=(N_reg,P_reg,K_reg,PH_reg,humidity_reg,temp_reg,cond_reg)

#Set up instrument
instrument = minimalmodbus.Instrument(PORT,1,mode=minimalmodbus.MODE_RTU)

instrument.serial.baudrate = 9600

#Make the settings explicit
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.close_port_after_each_call = True
instrument.clear_buffers_before_each_transaction = True

#--------------------------------------------------------------------






#master data frames
masterlist=[]
master_air=[]
Master=pd.DataFrame(masterlist, columns = ["N","P","K","PH","humidity","temp","cond","time"]) 
Master_Air=pd.DataFrame(master_air, columns = ['pm01','pm02','pm10','pm003Count','atmp','rhum','rco2','tvoc','timestamp']) 


def soilsensor(a):
	global Master

	templist=[]
	df = pd.DataFrame(templist, 
                  columns = ["N","P","K","PH","humidity","temp","cond","time"]) 
	

	print("got here")



	templist=[]
	#print("gothere2")
	print(df)

	for i in values:

		value = instrument.read_register(i)
		print(value)
		templist.append(value) #temporary list of all values
		print("templist",templist)

		
 
		# add time and append using loc methods
	time = datetime.datetime.now()
	templist.append(str(time))
	df.loc[len(df)] = templist
	
	
	#Master=pd.concat([Master,df])
	#print('master',Master)

def requestairgradient():
		global Master_Air

		response=requests.get("https://api.airgradient.com/public/api/v1/locations/81542/measures/current?token=2932e6e4-a882-43d9-833c-ec57b87e49a7")
		jsona=response.json()
		dfresponse=pd.json_normalize(jsona) #getting json api response as data frame

		dfresponse=dfresponse[['pm01','pm02','pm10','pm003Count','atmp','rhum','rco2','tvoc','timestamp']] #sub smapling columns of interest

		dfresponse=dfresponse.iloc[0,:] #convert to string so it can be appended to data fram

		Master_Air.loc[len(Master_Air)] = dfresponse #adding last read to master air data frame

		print(Master_Air)





		return fig
		if __name__ == "__main__":
	   		 app2.run_server(debug=True)


["N","P","K","PH","humidity","temp","cond","time"]
#Pushing to sql server-------------------------------
def sqlsoilsensor():

	with pool.connect() as db_conn:
		db_conn.execute(
      	 	sqlalchemy.text(
       		"CREATE TABLE IF NOT EXISTS soil_sensor "
       		"( id SERIAL NOT NULL, n FLOAT NOT NULL, "
       		"p FLOAT NOT NULL, k FLOAT NOT NULL, "
       		"ph FLOAT NOT NULL, humidity FLOAT NOT NULL, "
       		"temp FLOAT NOT NULL, cond FLOAT NOT NULL, "
       		"time TIMESTAMP NOT NULL, "
        	"PRIMARY KEY (id));"))

		results = db_conn.execute(sqlalchemy.text("SELECT * FROM soil_sensor")).fetchall()
		print(results)
		print('here')
		insert_stmt = sqlalchemy.text( "INSERT INTO soil_sensor (n,p,k,ph,humidity,temp,cond,time) VALUES (:n,:p,:k,:ph,:humidity,:temp,:cond,:time)",)
		a = instrument.read_register(N_reg)
		b=instrument.read_register(P_reg)
		c=instrument.read_register(K_reg)
		d=instrument.read_register(PH_reg)
		e=instrument.read_register(humidity_reg)
		f=instrument.read_register(temp_reg)
		g=instrument.read_register(cond_reg)
		h=datetime.datetime.now()
		print('time',h)
		db_conn.execute(insert_stmt, n= a, p= b, k= c, ph=d, humidity=e, temp=f, cond=g,time=h)
		#db_conn.execute(insert_stmt, n= a, p= b, k= c)
		results = db_conn.execute(sqlalchemy.text("SELECT * FROM soil_sensor")).fetchall()
		print(results)
		print('here')


connector = Connector()

# function to return the database connection-----------------------------------------------------
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "fluid-shoreline-441820-j4:northamerica-northeast1:biobox",
        "pymysql",
        user="root",
        password="biobox2024",
        db="biobox"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)
# insert statement
insert_stmt = sqlalchemy.text(
    "INSERT INTO my_table (id, title) VALUES (:id, :title)",
)
#-------------------------------------------------------------------------



print("starting")
#takevalues(a)
#pubdata()
#pub2()
#soilsensor()
sqlsoilsensor()
requestairgradient()


print("ending")


#how


#to do
	#deal with ram storage issue: maybe every 500 updates delete first 250 lines or something 
	#maybe average all the data first?


#before meeting, make update quicker? make nice demo, change units


#add to permanent data with timestamp


#want to save all values to one array with timestamp
#now = datetime.datetime.now()
#current_data=pd.array(now,N,P,K,PH,moisture)
#data=pd.append(data,current_data)



#to get data from cloud to here? 
#api to pull data in same array as above would be ideal


#create dashboard using dash - dash enterprise would be used in the future
#dash suggests running in an virtual environment 

# app.py


#next steps. find mean, add date time, upload to dashboard

def pub2():
	global Master_Air
	global Master
	app2 = Dash(__name__)
	app2.layout = html.Div(
   		 html.Div([
       		 html.H4('Soil sensor reading'),
       		 #html.Div(id='live-update-text'),
       		 dcc.Graph(id='live-update-graph'),
       		 dcc.Interval(
           		 id='interval-component',
           		 interval=15*1000, # in milliseconds
           		 n_intervals=0
       		 )
		   		 ])
		)
	takevalues(2)
	@callback(Output('live-update-graph', 'figure'),
        		     Input('interval-component', 'n_intervals'))
	def update_graph_live(n):
		takevalues(2)
		requestairgradient()
			#if dcc.interval
    		 # Collect some data
# Create the graph with subplots
		fig = plotly.tools.make_subplots(rows=3, cols=1, vertical_spacing=0.2)
		fig['layout']['margin'] = {
		    'l': 30, 'r': 10, 'b': 30, 't': 10
		}
		fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

		fig.append_trace({
		   'x': Master['time'],
		   'y': Master['humidity'],
	 	   'name': 'humidity reading',
	 	   'mode': 'lines+markers',
	  	  'type': 'scatter'
		}, 1, 1)
		fig.append_trace({
  		 'x': Master['time'],
   		 'y': Master['temp'],
   		 'text': Master['time'],
   		 'name': 'Temperature Reading',
   		 'mode': 'lines+markers',
   		 'type': 'scatter'
		}, 2, 1)
		fig.append_trace({
  		 'x': Master_Air['timestamp'],
   		 'y': Master_Air['rco2'],
   		 'text': Master['time'],
   		 'name': 'C02 reading',
   		 'mode': 'lines+markers',
   		 'type': 'scatter'
		}, 3, 1)

