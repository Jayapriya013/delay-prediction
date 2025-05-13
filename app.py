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

# Convert HH:MM to minutes
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
    try:
        # Convert times to minutes
        sched_dep_min = time_to_minutes(sched_dep_time)
        sched_arr_min = time_to_minutes(sched_arr_time)
        actual_dep_min = time_to_minutes(actual_dep_time)

        # Encode categorical features
        origin_enc = origin_encoder.transform([origin])[0]
        destination_enc = destination_encoder.transform([destination])[0]
        carrier_enc = carrier_encoder.transform([carrier])[0]

        # Prepare input for prediction
        input_data = np.array([[origin_enc, destination_enc, carrier_enc,
                                sched_dep_min, sched_arr_min, year]])
        
        # Make prediction
        prediction = model.predict(input_data)[0]

        # Display prediction result
        if prediction == 1:
            st.error("🔴 Prediction: Flight is likely to be Delayed.")
        else:
            st.success("🟢 Prediction: Flight is likely to be On Time.")

        # Rule-based actual delay check
        actual_delay = abs(actual_dep_min - sched_dep_min)
        if actual_delay <= 15:
            st.info("ℹ️ Note: Actual departure is on time or within 15 minutes.")
        else:
            st.warning(f"⚠️ Note: Actual departure delayed by {actual_delay} minutes.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


        
