from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException



from datetime import datetime , timedelta

import pytz
import requests
import matplotlib.pyplot as plt
import pandas as pd
from google.cloud.sql.connector import Connector, IPTypes
import pymysql

import smtplib, ssl


def brevo():


	configuration = sib_api_v3_sdk.Configuration()
	





	configuration.api_key['api-key'] = 'send me a slack - github wont allow keys to be pushed'

	api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
	subject = "from the Python SDK!"
	sender = {"name":"Jeff","email":"jeff@verdant.com"}
	replyTo = {"name":"Luke","email":"jeff@verdant.com"}
	html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
	to = [{"email":"jeff@verdant.com","name":"Luke"}]
	params = {"parameter":"My param value","subject":"test flood alert"}
	send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=replyTo, html_content=html_content, sender=sender, subject=subject)

	try:
	    api_response = api_instance.send_transac_email(send_smtp_email)
	    print(api_response)
	except ApiException as e:
	    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
	## conect to email__________________________________________
def send_email():
	port = 465  # For SSL
	password = input("Type your password and press enter: ")

	# Create a secure SSL context
	context = ssl.create_default_context()

	#______________________________________

	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
	    server.login("my@gmail.com", password)
	    sender_email = "jeff@verdant.com"
	    receiver_email = "luke@verdant.com"
	    message = """\
	    Subject: Hi there
	    

	    This message is sent from Python. Your lawn is flooding"""
	    server.sendmail(sender_email, receiver_email, message) 
		

def past24h():
	url ="https://api.tomorrow.io/v4/weather/history/recent"
	params = {
	    "apikey": "send me a slack - github wont allow keys to be pushed",
	    "location": "45.478383,-73.590833",  # Latitude, Longitude
	}
	response = requests.get(url, params=params)
	if response.status_code == 200:
		data=response.json()
		#print(response.json())
		timelines = data["timelines"]
		intervals = timelines["hourly"]
		#print(intervals)


		# Prepare a list of dictionaries for Pandas
		rows = []
		for interval in intervals:
		    time = interval["time"]
		    values = interval["values"]
		    rows.append({
		        "time": time,
		        "temperature": values.get("temperature"),
		        "precipitationProbability": values.get("precipitationProbability"),
		        "rainAccumulationLwe": values.get("rainAccumulationLwe"),
		        "rainAccumulation": values.get("rainAccumulation")
		    })
		df = pd.DataFrame(rows)

		# Display the DataFrame
		#print(df)
		return df

	else:
		print(f"Error: {response.status_code}, {response.text}")


def next5days():
	url = "https://api.tomorrow.io/v4/timelines"
	start_time=datetime.utcnow().isoformat()+"Z"
	end_time=(datetime.utcnow()+timedelta(hours=100)).isoformat()+"Z"
	print(start_time)
	params = {
	    "apikey": "send me a slack - github wont allow keys to be pushed",
	    "location": "45.478383,-73.590833",  # Latitude, Longitude
	    "fields": ["temperature", "precipitationProbability","rainAccumulation","rainAccumulationLwe"],
	    "timesteps": "1h",  # 1 hour increments
	    "startTime": start_time,
	    "endTime": end_time
	}
	response = requests.get(url, params=params)

	if response.status_code == 200:
		data=response.json()
		#print(response.json())
		timelines = data["data"]["timelines"]
		intervals = timelines[0]["intervals"]
		print(intervals)

		# Prepare a list of dictionaries for Pandas
		rows = []
		for interval in intervals:
		    time = interval["startTime"]
		    values = interval["values"]
		    rows.append({
		        "time": time,
		        "temperature": values.get("temperature"),
		        "precipitationProbability": values.get("precipitationProbability"),
		        "rainAccumulationLwe": values.get("rainAccumulationLwe"),
		        "rainAccumulation": values.get("rainAccumulation")
		    })
		df = pd.DataFrame(rows)

		# Display the DataFrame
		print(df)
	else:
		print(f"Error: {response.status_code}, {response.text}")

def current():
	url = "https://api.tomorrow.io/v4/weather/realtime"
	params = {
    "apikey": "send me a slack - github wont allow keys to be pushed",
    "location": "45.478383,-73.590833",  # Latitude, Longitude
    "fields": ["temperature", "precipitationProbability","rainAccumulation","rainAccumulationLwe"],
	}
	response = requests.get(url, params=params)
	if response.status_code == 200:
		data=response.json()
		#print(response.json())
		now = data["data"]["values"]
		# Prepare a list of dictionaries for Pandas
		rows = []
		values = now
		rows.append({
	        "time": values.get("time"),
	        "temperature": values.get("temperature"),
	        "precipitationProbability": values.get("precipitationProbability"),
	        "rainAccumulationLwe": values.get("rainAccumulationLwe"),
	        "rainAccumulation": values.get("rainAccumulation")
	    })
		df = pd.DataFrame(rows)

		# Display the DataFrame
		print(df)
		return df 
	else:
		print(f"Error: {response.status_code}, {response.text}")	




#get sql connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "fluid-shoreline-441820-j4:northamerica-northeast1:biobox",
        "pymysql",
        user="root",
        password="shoot me a message",
        db="biobox"
    )
    return conn

# create connection pool



def sqlfetch(): #get the x most recent values of 
	cursor.execute("SELECT TIME, moisture FROM soil_sensor ORDER BY TIME DESC LIMIT 10")
	rows = cursor.fetchall()
	return rows

def alert():
	#if the precipitation in the df is properly matched to the soil moiste, all good. If it is raining by the soil moisture is no longer going up, thats a problem
	#define delta soil moistre, find slop of readings
	current()
	sqlfetch()
	moistnow=rows[0][1]
	moist1hago=rows[1][1]
	deltamoisture=moistnow-moist1hago
	deltarain=df.iloc[0]
	deltarain=deltarain[rainAccumulation]
	rate=deltamoisture/deltarain #if delta moisture is positive and rate decreases from 1 reading to the next, then you are in a potential flooding event



	moist2ago=rows[2][1]
	moist3hago=rows[3][1]
	deltamoisture2=moist2ago-moist3hago
	deltarain2=df.iloc[1]
	deltarain2=deltarain2[rainAccumulation]
	rate2=deltamoisture2/deltarain2

	if deltrain>0:
		if deltamoisture>0:
			if rate<rate2:
				send_email()
			else:
				pass
		else:
			pass
	else:
		pass





##uncomment to work

# pool = sqlalchemy.create_engine(
#     "mysql+pymysql://",
#     creator=getconn,
# )
# connector = Connector()

brevo()
#alert()
#next5days()
#TODO pull moisture data and compare against weather data
#how do i want to compare 

#current()
# send_email()

# print("starting")
# try:
#     while True:
#         #alert()
#         time.sleep(10)
# except KeyboardInterrupt:
#     print('interrupted!')

