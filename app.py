import streamlit as st
import requests
from streamlit_folium import folium_static
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from os import system, name

st.markdown("<h1 style='text-align: center; color: black;'>NY Taxi</h1>",
            unsafe_allow_html=True)

st.subheader('Please provide the following information:')
col1, col2 = st.columns(2)

with col1:
    date_input = st.date_input('date')

with col2:
    time_input = st.time_input('time')

col3, col4= st.columns(2)
with col3:
    pickup_address = st.text_input('pickup address')

with col4:
    dropoff_address = st.text_input('drop-off address')

passenger_count = st.number_input('number of passengers')

# convert address to Lat, long

def convert_function(address):
    geolocator = Nominatim(user_agent="coordinateconverter")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

pickup_lat, pickup_long = convert_function(pickup_address)
dropoff_lat, dropoff_long = convert_function(dropoff_address)



url = 'https://hamzabenkirane-vx4qmeuejq-ew.a.run.app/predict'

params = {
    'pickup_datetime': f"{date_input} {time_input}",
    'pickup_longitude': pickup_long,
    'pickup_latitude': pickup_lat,
    'dropoff_longitude': dropoff_long,
    'dropoff_latitude': dropoff_lat,
    'passenger_count': passenger_count
}

response = requests.get(url, params=params).json()

st.write('The fare of your taxi ride is ', round(response['prediction'],1))

# Map

m = folium.Map(location=[40.7,-73.9], zoom_start=10)

folium.Marker([pickup_long, pickup_lat], popup="pickup position").add_to(m)
folium.Marker([dropoff_long, dropoff_lat], popup="dropoff position").add_to(m)

folium_static(m)
