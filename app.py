import streamlit as st
import numpy as np

# App title
st.title("✈️ Flight Delay Prediction (Rule-Based)")

# Subheader
st.subheader("📝 Enter Flight Details")

# Dropdowns for origin, destination, carrier
origin_options = ['JFK', 'LAX', 'ORD', 'ATL', 'DFW', 'DEN', 'SFO', 'LAS', 'SEA', 'MIA']
destination_options = ['LAX', 'JFK', 'ATL', 'ORD', 'SEA', 'MCO', 'PHX', 'IAH', 'BOS', 'CLT']
carrier_options = ['AA', 'DL', 'UA', 'SW', 'AS', 'NK', 'B6', 'F9']

col1, col2, col3 = st.columns(3)
with col1:
    origin = st.selectbox("Origin Airport", origin_options)
with col2:
    destination = st.selectbox("Destination Airport", destination_options)
with col3:
    carrier = st.selectbox("Carrier", carrier_options)

# Time inputs
col4, col5 = st.columns(2)
with col4:
    sched_dep = st.text_input("🕐 Scheduled Departure Time (HH:MM)", "")
with col5:
    actual_dep = st.text_input("🕒 Actual Departure Time (HH:MM)", "")

# Arrival and year inputs
col6, col7 = st.columns(2)
with col6:
    sched_arr = st.text_input("🕘 Scheduled Arrival Time (HH:MM)", "")
with col7:
    year = st.number_input("📅 Flight Year", min_value=2000, max_value=2030, value=2024)

# Time conversion helper
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
if st.button("🔍 Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    actual_dep_min = convert_to_minutes(actual_dep)

    if np.isnan(sched_dep_min) or np.isnan(actual_dep_min):
        st.error("❌ Please enter valid time in HH:MM format for both scheduled and actual departure.")
    else:
        delay = actual_dep_min - sched_dep_min

        if delay > 15:
            st.error(f"🛑 Prediction: Flight is Delayed by {delay} minutes.")
        else:
            st.success("✅ Prediction: Flight is On-Time.")
