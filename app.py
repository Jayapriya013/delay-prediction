import streamlit as st
import numpy as np

# Title
st.title("✈️ Flight Delay Prediction (Based on Actual Time)")

# Input Form
st.subheader("Enter Flight Details")

origin = st.text_input("Origin Airport Code (e.g., JFK)", "")
destination = st.text_input("Destination Airport Code (e.g., LAX)", "")
carrier = st.text_input("Carrier Code (e.g., AA)", "")

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

# Predict Button
if st.button("Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    actual_dep_min = convert_to_minutes(actual_dep)

    if np.isnan(sched_dep_min) or np.isnan(actual_dep_min):
        st.error("❌ Please enter valid time in HH:MM format.")
    else:
        delay = actual_dep_min - sched_dep_min

        if delay > 15:
            st.error(f"🛑 Prediction: Flight is Delayed by {delay} minutes.")
        else:
            st.success("✅ Prediction: Flight is On-Time or within 15 minutes delay.")
