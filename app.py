import streamlit as st
import numpy as np
import pickle
import pandas as pd

# Load the XGBoost model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Title
st.title("✈️ Flight Delay Prediction (XGBoost Model)")

# Input Form
st.subheader("Enter Flight Details")

# Dropdown options for origin, destination, carrier
origin_options = ['JFK', 'LAX', 'ORD', 'ATL', 'DFW', 'DEN', 'SFO', 'LAS', 'SEA', 'MIA']
destination_options = ['LAX', 'JFK', 'ATL', 'ORD', 'SEA', 'MCO', 'PHX', 'IAH', 'BOS', 'CLT']
carrier_options = ['AA', 'DL', 'UA', 'SW', 'AS', 'NK', 'B6', 'F9']

origin = st.selectbox("Origin Airport", origin_options)
destination = st.selectbox("Destination Airport", destination_options)
carrier = st.selectbox("Carrier", carrier_options)

sched_dep = st.text_input("Scheduled Departure Time (HH:MM)", "")
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM)", "")
actual_dep = st.text_input("Actual Departure Time (HH:MM)", "")
year = st.number_input("Flight Year", min_value=2000, max_value=2030, value=2024)

# Function to convert HH:MM to minutes
def convert_to_minutes(time_str):
    try:
        if ":" not in time_str:
            raise ValueError
        h, m = map(int, time_str.strip().split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m
    except:
        return np.nan

# Prepare the data for prediction
def prepare_input_data(origin, destination, carrier, sched_dep_min, sched_arr_min, actual_dep_min, year):
    # You might need to map these categorical variables to numerical values as done during model training
    origin_map = {'JFK': 0, 'LAX': 1, 'ORD': 2, 'ATL': 3, 'DFW': 4, 'DEN': 5, 'SFO': 6, 'LAS': 7, 'SEA': 8, 'MIA': 9}
    destination_map = {'LAX': 0, 'JFK': 1, 'ATL': 2, 'ORD': 3, 'SEA': 4, 'MCO': 5, 'PHX': 6, 'IAH': 7, 'BOS': 8, 'CLT': 9}
    carrier_map = {'AA': 0, 'DL': 1, 'UA': 2, 'SW': 3, 'AS': 4, 'NK': 5, 'B6': 6, 'F9': 7}
    
    data = {
        'origin': origin_map.get(origin, -1),
        'destination': destination_map.get(destination, -1),
        'carrier': carrier_map.get(carrier, -1),
        'sched_dep': sched_dep_min,
        'sched_arr': sched_arr_min,
        'actual_dep': actual_dep_min,
        'year': year
    }
    return pd.DataFrame([data])

# Predict Button
if st.button("Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    actual_dep_min = convert_to_minutes(actual_dep)

    if np.isnan(sched_dep_min) or np.isnan(actual_dep_min):
        st.error("❌ Please enter valid time in HH:MM format.")
    else:
        # Prepare the input data for prediction
        input_data = prepare_input_data(origin, destination, carrier, sched_dep_min, sched_arr_min=None, actual_dep_min=sched_dep_min, year=year)
        
        # Use the model to predict the flight delay
        prediction = model.predict(input_data)
        
        delay = prediction[0]
        
        # Display the result
        if delay > 15:
            st.error(f"🛑 Prediction: Flight is Delayed by {delay} minutes.")
        else:
            st.success("✅ Prediction: Flight is On-Time.")
