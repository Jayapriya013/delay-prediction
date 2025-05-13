import streamlit as st
import pickle
import pandas as pd

# Load model and encoders
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

origin_enc = encoders['origin']
destination_enc = encoders['destination']
carrier_enc = encoders['carrier']

# UI
st.title("✈️ Flight Delay Prediction App")

# Dropdowns from training data
origins = list(origin_enc.classes_)
destinations = list(destination_enc.classes_)
carriers = list(carrier_enc.classes_)

origin = st.selectbox("Origin Airport", origins)
destination = st.selectbox("Destination Airport", destinations)
carrier = st.selectbox("Carrier", carriers)

sched_dep_time = st.text_input("Scheduled Departure Time (HH:MM)", "08:00")
sched_arr_time = st.text_input("Scheduled Arrival Time (HH:MM)", "10:00")
actual_dep_time = st.text_input("Actual Departure Time (HH:MM)", "08:10")
year = st.number_input("Flight Year", min_value=2000, max_value=2100, step=1, value=2020)

# Convert time to minutes
def time_to_minutes(t):
    try:
        h, m = map(int, t.split(":"))
        return h * 60 + m
    except:
        return 0

# Predict button
if st.button("Predict Delay"):
    try:
        # Encode inputs
        origin_code = origin_enc.transform([origin])[0]
        destination_code = destination_enc.transform([destination])[0]
        carrier_code = carrier_enc.transform([carrier])[0]

        sched_dep_min = time_to_minutes(sched_dep_time)
        sched_arr_min = time_to_minutes(sched_arr_time)
        actual_dep_min = time_to_minutes(actual_dep_time)

        # 7 features input
        X = [[origin_code, destination_code, carrier_code,
              sched_dep_min, sched_arr_min, actual_dep_min, year]]

        prediction = model.predict(X)[0]

        if prediction == 1:
            st.error("🟥 Prediction: Delayed")
        else:
            st.success("🟩 Prediction: On-Time")

    except Exception as e:
        st.error(f"Error: {str(e)}")
