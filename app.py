import streamlit as st
import numpy as np
import joblib

# Load the XGBoost model
model = joblib.load("model.pkl")  # Ensure this file is in the same directory

# Manual encodings (must match training)
airport_dict = {'JFK': 0, 'LAX': 1, 'ORD': 2, 'ATL': 3, 'DFW': 4, 'DEN': 5, 'SFO': 6, 'LAS': 7, 'SEA': 8, 'MIA': 9}
destination_dict = {'LAX': 0, 'JFK': 1, 'ATL': 2, 'ORD': 3, 'SEA': 4, 'MCO': 5, 'PHX': 6, 'IAH': 7, 'BOS': 8, 'CLT': 9}
carrier_dict = {'AA': 0, 'DL': 1, 'UA': 2, 'SW': 3, 'AS': 4, 'NK': 5, 'B6': 6, 'F9': 7}

# Title
st.title("✈️ Flight Delay Prediction using XGBoost")

st.subheader("Enter Flight Details")

# UI Inputs
origin = st.selectbox("Origin Airport", list(airport_dict.keys()))
destination = st.selectbox("Destination Airport", list(destination_dict.keys()))
carrier = st.selectbox("Carrier", list(carrier_dict.keys()))
sched_dep = st.text_input("Scheduled Departure Time (HH:MM)", "")
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM)", "")
actual_dep = st.text_input("Actual Departure Time (HH:MM)", "")
year = st.number_input("Flight Year", min_value=2000, max_value=2030, value=2025)

# Convert time string to total minutes
def convert_to_minutes(time_str):
    try:
        h, m = map(int, time_str.strip().split(":"))
        return h * 60 + m
    except:
        return np.nan

# Prediction Logic
if st.button("Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    sched_arr_min = convert_to_minutes(sched_arr)
    actual_dep_min = convert_to_minutes(actual_dep)

    if np.isnan(sched_dep_min) or np.isnan(actual_dep_min) or np.isnan(sched_arr_min):
        st.error("❌ Please enter valid time values in HH:MM format.")
    else:
        delay = actual_dep_min - sched_dep_min

        features = np.array([[
            airport_dict[origin],
            destination_dict[destination],
            carrier_dict[carrier],
            sched_dep_min,
            sched_arr_min,
            actual_dep_min,
            year,
            delay
        ]])

        prediction = model.predict(features)[0]

        if prediction == 1:
            st.error(f"🛑 Prediction: Flight is Delayed.")
        else:
            st.success("✅ Prediction: Flight is On-Time.")
