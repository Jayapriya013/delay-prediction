import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model and encoders
model = joblib.load("model.pkl")
le_origin = joblib.load("le_origin.pkl")
le_destination = joblib.load("le_destination.pkl")
le_carrier = joblib.load("le_carrier.pkl")

# Function to convert HH:MM to minutes
def time_to_minutes(t):
    try:
        h, m = map(int, t.split(":"))
        return h * 60 + m
    except:
        return None

# App UI
st.set_page_config(page_title="Flight Delay Predictor", layout="centered")
st.title("✈️ Flight Delay Predictor")

# Inputs
origin = st.selectbox("Origin Airport", le_origin.classes_)
destination = st.selectbox("Destination Airport", le_destination.classes_)
carrier = st.selectbox("Carrier", le_carrier.classes_)

# Empty time input fields
sched_dep_time = st.text_input("Scheduled Departure Time (HH:MM)", "")
sched_arr_time = st.text_input("Scheduled Arrival Time (HH:MM)", "")
actual_dep_time = st.text_input("Actual Departure Time (HH:MM)", "")
year = st.number_input("Flight Year", min_value=2000, max_value=2100, value=2024)

if st.button("Predict Delay"):
    # Convert times to minutes
    sched_dep_min = time_to_minutes(sched_dep_time)
    sched_arr_min = time_to_minutes(sched_arr_time)
    actual_dep_min = time_to_minutes(actual_dep_time)

    # Validate time format
    if None in [sched_dep_min, sched_arr_min, actual_dep_min]:
        st.error("❌ Please enter valid time in HH:MM format.")
    else:
        try:
            # Encode categorical values
            origin_enc = le_origin.transform([origin])[0]
            destination_enc = le_destination.transform([destination])[0]
            carrier_enc = le_carrier.transform([carrier])[0]

            # Feature vector (7 features)
            features = np.array([[origin_enc, destination_enc, carrier_enc,
                                  sched_dep_min, sched_arr_min, actual_dep_min, year]])

            # Make prediction
            prediction = model.predict(features)[0]

            # Show result
            if prediction == 1:
                st.warning("✈️ The flight is likely to be **delayed**.")
            else:
                st.success("🟢 The flight is likely to be **on time**.")

        except Exception as e:
            st.error(f"⚠️ Error in prediction: {str(e)}")
