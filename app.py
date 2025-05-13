import streamlit as st
import pickle
import numpy as np

# Load model and encoders
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        data = pickle.load(f)
    return data["model"], data["le_origin"], data["le_dest"], data["le_carrier"]

model, le_origin, le_dest, le_carrier = load_model()

# Title
st.title("✈️ Flight Delay Prediction App")

# Input Form
st.subheader("Enter Flight Details")

origin = st.selectbox("Origin Airport", le_origin.classes_)
destination = st.selectbox("Destination Airport", le_dest.classes_)
carrier = st.selectbox("Carrier", le_carrier.classes_)

sched_dep = st.text_input("Scheduled Departure Time (HH:MM)", "")
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM)", "")
actual_dep = st.text_input("Actual Departure Time (HH:MM)", "")
year = st.number_input("Flight Year", min_value=2000, max_value=2030, value=2024)

# Helper to convert HH:MM to minutes
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

# Prediction
if st.button("Predict Delay"):
    try:
        # Encode inputs
        origin_code = origin_enc.transform([origin])[0]
        destination_code = destination_enc.transform([destination])[0]
        carrier_code = carrier_enc.transform([carrier])[0]

        # Feature vector
        X = [[origin_code, destination_code, carrier_code,
              sched_dep_total_min, sched_arr_total_min,
              actual_dep_total_min, year]]

        # Model prediction (0: On-Time, 1: Delayed)
        prediction = model.predict(X)[0]

        if prediction == 1:
            st.error("🟥 Prediction: Delayed")
        else:
            st.success("🟩 Prediction: On-Time")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
