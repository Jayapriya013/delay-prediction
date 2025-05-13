import streamlit as st
import numpy as np

# App title
st.title("✈️ Flight Delay Prediction (Rule-Based)")

# Subheader
st.subheader("📝 Enter Flight Details")

# Dropdown options
origin_options = ['JFK', 'LAX', 'ORD', 'ATL', 'DFW', 'DEN', 'SFO', 'LAS', 'SEA', 'MIA']
destination_options = ['LAX', 'JFK', 'ATL', 'ORD', 'SEA', 'MCO', 'PHX', 'IAH', 'BOS', 'CLT']
carrier_options = ['AA', 'DL', 'UA', 'SW', 'AS', 'NK', 'B6', 'F9']
airport_names = ['John F. Kennedy Intl', 'Los Angeles Intl', 'O\'Hare Intl', 'Hartsfield–Jackson ATL',
                 'Dallas/Fort Worth', 'Denver Intl', 'San Francisco Intl', 'Las Vegas', 'Seattle-Tacoma', 'Miami Intl']

# Layout for inputs
col1, col2, col3 = st.columns(3)
with col1:
    origin = st.selectbox("Origin Airport", origin_options)
with col2:
    destination = st.selectbox("Destination Airport", destination_options)
with col3:
    carrier = st.selectbox("Carrier", carrier_options)

col4, col5 = st.columns(2)
with col4:
    sched_dep = st.text_input("🕐 Scheduled Departure Time (HH:MM)", "")
with col5:
    sched_arr = st.text_input("🕘 Scheduled Arrival Time (HH:MM)", "")

col6, col7 = st.columns(2)
with col6:
    year = st.number_input("📅 Flight Year", min_value=2000, max_value=2030, value=2024)
with col7:
    airport_name = st.selectbox("🏢 Airport Name", airport_names)

# Helper function
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

# Delay prediction using dummy rule (just for demo – actual logic can use dataset)
if st.button("🔍 Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    sched_arr_min = convert_to_minutes(sched_arr)

    if np.isnan(sched_dep_min) or np.isnan(sched_arr_min):
        st.error("❌ Please enter valid HH:MM format for departure and arrival times.")
    else:
        # Dummy logic: Assume flights scheduled late in the day are more delayed
        if sched_dep_min > 1200:
            delay = 25  # simulated delay
            st.error(f"🛑 Prediction: Flight is Delayed by {delay} minutes.")
        else:
            st.success("✅ Prediction: Flight is On-Time.")

        st.info(f"📍 Airport: {airport_name}")
