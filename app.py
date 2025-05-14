import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the model and encoders
with open('model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    le_origin = model_data['le_origin']
    le_destination = model_data['le_destination']
    le_carrier = model_data['le_carrier']

# Time conversion function
def hhmm_to_minutes(time_str):
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except:
        return 0

# Streamlit app UI
st.set_page_config(page_title="Flight Delay Predictor", layout="centered")
st.title("✈️ Flight Delay Predictor")

# User inputs
origin = st.selectbox("Origin Airport", le_origin.classes_)
destination = st.selectbox("Destination Airport", le_destination.classes_)
carrier = st.selectbox("Carrier", le_carrier.classes_)
sched_dep_time = st.text_input("Scheduled Departure Time (HH:MM)", "10:00")
sched_arr_time = st.text_input("Scheduled Arrival Time (HH:MM)", "12:00")
actual_dep_time = st.text_input("Actual Departure Time (HH:MM)", "10:15")
year = st.number_input("Flight Year", min_value=2000, max_value=2100, value=2024)

# Prediction
if st.button("Predict Delay"):
    try:
        sched_dep_min = hhmm_to_minutes(sched_dep_time)
        sched_arr_min = hhmm_to_minutes(sched_arr_time)
        actual_dep_min = hhmm_to_minutes(actual_dep_time)

        # Encode inputs
        origin_encoded = le_origin.transform([origin])[0]
        destination_encoded = le_destination.transform([destination])[0]
        carrier_encoded = le_carrier.transform([carrier])[0]

        # Input vector (7 features)
        input_data = np.array([[origin_encoded, destination_encoded, carrier_encoded,
                                sched_dep_min, sched_arr_min, actual_dep_min, year]])

        # Predict
        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.error("🛑 Prediction: Flight is Delayed.")
        else:
            st.success("✅ Prediction: Flight is On-Time.")

    except Exception as e:
        st.warning(f"⚠️ Error in prediction: {e}")
