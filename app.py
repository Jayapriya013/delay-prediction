import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load encoders and model
model = pickle.load(open("model.pkl", "rb"))
origin_encoder = pickle.load(open("origin_encoder.pkl", "rb"))
destination_encoder = pickle.load(open("destination_encoder.pkl", "rb"))
carrier_encoder = pickle.load(open("carrier_encoder.pkl", "rb"))

# ✅ Time conversion helper
def time_to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m

# Streamlit app UI
st.title("Flight Delay Prediction")

carrier = st.selectbox("Carrier", carrier_encoder.classes_)
origin = st.selectbox("Origin Airport", origin_encoder.classes_)
destination = st.selectbox("Destination Airport", destination_encoder.classes_)

sched_dep_time = st.text_input("Scheduled Departure Time (HH:MM)", "10:00")
sched_arr_time = st.text_input("Scheduled Arrival Time (HH:MM)", "11:15")
actual_dep_time = st.text_input("Actual Departure Time (HH:MM)", "10:20")
year = st.number_input("Flight Year", min_value=2000, max_value=2030, value=2020)

# ✅ Prediction logic
if st.button("Predict Delay"):
    try:
        sched_dep_min = time_to_minutes(sched_dep_time)
        sched_arr_min = time_to_minutes(sched_arr_time)
        actual_dep_min = time_to_minutes(actual_dep_time)

        origin_enc = origin_encoder.transform([origin])[0]
        destination_enc = destination_encoder.transform([destination])[0]
        carrier_enc = carrier_encoder.transform([carrier])[0]

        input_data = np.array([[origin_enc, destination_enc, carrier_enc,
                                sched_dep_min, sched_arr_min, year]])
        
        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.error("🔴 Prediction: Flight is likely to be Delayed.")
        else:
            st.success("🟢 Prediction: Flight is likely to be On Time.")

        actual_delay = abs(actual_dep_min - sched_dep_min)
        if actual_delay <= 15:
            st.info("ℹ️ Note: Actual departure is on time or within 15 minutes.")
        else:
            st.warning(f"⚠️ Note: Actual departure delayed by {actual_delay} minutes.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
