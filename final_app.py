# importing libraries
from pkg_resources import add_activation_listener
import streamlit as st
import datetime
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os
from streamlit_folium import folium_static
import folium
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
import io
from folium import plugins
import base64
import hashlib
import sqlite3 
from datetime import datetime,timedelta
import geopy
from geopy import distance
from geopy.geocoders import Nominatim



# Security
#passlib,hashlib,bcrypt,scrypt



# Security
#passlib,hashlib,bcrypt,scrypt
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management

conn = sqlite3.connect('data.db')
conn1=sqlite3.connect('userdata.db')
c = conn.cursor()
c1 = conn1.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,start_point1 TEXT,start_point2 TEXT,start_time TEXT,start_Location TEXT,end_point1 TEXT,end_point2 TEXT,end_time TEXT,end_Location TEXT,date TEXT,distance TEXT)')
	c1.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password,start_point1,start_point2,start_time,start_Location,end_point1 ,end_point2 ,end_time,end_Location,date ,distance):
	c.execute('INSERT INTO userstable(username,password,start_point1,start_point2 ,start_time,start_Location,end_point1 ,end_point2 ,end_time,end_Location,date ,distance) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(username,password,start_point1,start_point2,start_time,start_Location,end_point1 ,end_point2 ,end_time,end_Location,date ,distance))
	conn.commit()
def add_userdata1(username,password):
    c1.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn1.commit()
def login_user1(username,password):
    c1.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    userdata = c1.fetchall()
    return userdata

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
def login_user_ver(username):
	c1.execute('SELECT username FROM userstable WHERE username =?',(username,))
	data = c1.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def getLocation():
    options = Options()
    #options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    
    options.add_argument("--use--fake-ui-for-media-stream")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")


    driver = webdriver.Chrome(executable_path = 'chrome driver location',options=options)#Edit path of chromedriver accordingly
    timeout = 0
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(0)
    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')   
    longitude = [x.text for x in longitude]    
    longitude = float(longitude[0])    
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')    
    latitude = [x.text for x in latitude]    
    latitude = float(latitude[0])    
    driver.quit()    
    return (latitude,longitude)
def getLocation_Name():
	geolocator = Nominatim(user_agent="geoapiExercises")
	Lat = str(getLocation()[0])
	Long = str(getLocation()[1])
	location = geolocator.reverse(Lat+","+Long)
	return location

def render_map(cord):
    m = folium.Map(tiles= 'OpenStreetMap',zoom_start=20,location=cord)#map variable
    folium.Marker(location = cord).add_to(m)#places marker at the current location
    # save map data to data object
    data = io.BytesIO()
    m.save(data, close_file=False)
    folium_static(m,width= 500,height=300)

def current_time():
    

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")#variable storing time
    return current_time
def current_date():
    date=datetime.now().date()
    return date
def user_dates():
    c.execute('SELECT date FROM userstable ')
    user_dates=c.fetchall()
    return user_dates
def user_names():
    c1.execute('SELECT username FROM userstable ')
    user_names=c1.fetchall()
    return user_names
def user_data(username,date):
    c.execute('SELECT distance FROM userstable WHERE username =? AND date = ?',(username,date))
    distance=c.fetchall()
    return distance



def distance_cal(cord1,cord2):
    start = cord1
    end = cord2
    d1 = distance.distance(start,end)#variable storing distance
    return d1




def main():
	

	

	menu = ["Home","SignUp","Login",'Travel Statics','Admin statics']
	choice = st.sidebar.radio("Menu",menu)
	if 'start' not in st.session_state:
		st.session_state['start']=(0,0)
	if 'end' not in st.session_state:
		st.session_state['end']=(0,0)
	if 'start_time' not in st.session_state:
		st.session_state['start_time']= 0
	if 'end_time' not in st.session_state:
		st.session_state['end_time']=0
	if 'check' not in st.session_state:
     		st.session_state['check']=0
	
	
	if choice=='Home':
		
			
		st.image('background.png')
		st.header('Click singup to Register')
	elif choice=='Travel Statics':
		st.subheader('Waana see How much distance you covered today')
		username = st.text_input("User Name")
		password = st.text_input("Password",type='password')
		if st.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			result=login_user1(username,password)
			if result:
				final_dates = [i[0] for i in user_dates()]
				final_dates=list(set(final_dates))
				sel_date=st.selectbox('Select date',final_dates)
				distances1= [i[0] for i in user_data(username,sel_date)]
				final_distances=[float(i.split()[0]) for i in distances1]
				st.write('Travel History:',final_distances)
				st.write('Total distance travelled :',sum(final_distances))
		#st.write(final_result)
	elif choice=='Admin statics':
		Admin_username = str(st.text_input("Admin User Name"))
		Admin_password = str(st.text_input("Admin Password",type='password'))
		if st.checkbox("Login"):
			if Admin_username=='admin_111' and Admin_password=='111admin':
				user_name=[i[0] for i in user_names()]
				user_name=list(set(user_name))
				username=st.selectbox('Username',user_name)
				final_dates = [i[0] for i in user_dates()]
				final_dates=list(set(final_dates))
				sel_date=st.selectbox('Select date',final_dates)
				distances1= [i[0] for i in user_data(username,sel_date)]
				final_distances=[float(i.split()[0]) for i in distances1]
				st.write('Travel History:',final_distances)
				st.write('Total distance travelled :',sum(final_distances))
		
		
	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			result=login_user_ver(new_user)
			if result:
				st.error('Username already taken')
			else:
				add_userdata1(new_user,new_password)
				
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
	

	elif choice == "Login":
		st.subheader("Start your Journey")
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			result=login_user1(username,password)
			if result:
				sel_cl,disp_cl = st.columns(2)
				if sel_cl.button('Journey start point'):
					st.session_state['start']= getLocation()
					geolocator = Nominatim(user_agent="geoapiExercises")
					Lat = str(st.session_state['start'][0])
					Long = str(st.session_state['start'][1])
					location = geolocator.reverse(Lat+","+Long)
					
					st.session_state['LName1']=location
					st.session_state['check']=1
					
					render_map(st.session_state['start'])
					st.session_state['start_time']=current_time()

					st.write('You are at',st.session_state['start'])

				
				if disp_cl.button('Journey end point'):
						st.session_state['end']= getLocation()
						geolocator = Nominatim(user_agent="geoapiExercises")
						Lat = str(st.session_state['end'][0])
						Long = str(st.session_state['end'][1])
						location = geolocator.reverse(Lat+","+Long)
						

						st.session_state['LName2']=location
						st.session_state['check']=2+st.session_state['check']
						render_map(st.session_state['end'])
						st.session_state['end_time']=current_time()

						st.write('You are at',st.session_state['end'])
						start_point=st.session_state['start']
						end_point=st.session_state['end']
						start_point1 = st.session_state['start'][0]
						start_point2 = st.session_state['start'][1]
						end_point1 = st.session_state['end'][0]
						end_point2 = st.session_state['end'][1]
						start_time=st.session_state['start_time']
						end_time=st.session_state['end_time']
						start_Location=st.session_state['LName1']
						end_Location=st.session_state['LName2']

						
						distance= distance_cal(start_point,end_point)
						date=current_date()
			else:
				st.error("No existing user account, Do SignUp")
			if st.session_state['check']==3:
				create_usertable()
				add_userdata(username,make_hashes(password),str(start_point1),str(start_point2),str(start_time),str(start_Location),str(end_point1) ,str(end_point2) ,str(end_time),str(end_Location),str(date), str(distance))
			if st.session_state['check']==2:
				st.error("Start your journey")
				
					


				
					
				
				




	



if __name__ == '__main__':
    main()

