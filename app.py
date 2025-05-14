import streamlit as st
import numpy as np
import pickle

# Load the model and encoders
with open("model.pkl", "rb") as f:
    model_data = pickle.load(f)

model = model_data['model']

# If encoders exist
origin_enc = model_data.get('origin_enc', None)
destination_enc = model_data.get('destination_enc', None)
carrier_enc = model_data.get('carrier_enc', None)

# Airport and carrier options
origin_options = ['JFK', 'LAX', 'ORD', 'ATL', 'DFW', 'DEN', 'SFO', 'LAS', 'SEA', 'MIA']
destination_options = ['LAX', 'JFK', 'ATL', 'ORD', 'SEA', 'MCO', 'PHX', 'IAH', 'BOS', 'CLT']
carrier_options = ['AA', 'DL', 'UA', 'SW', 'AS', 'NK', 'B6', 'F9']

# Title
st.title("✈️ Flight Delay Prediction (Model-Based)")

# Input Form
st.subheader("Enter Flight Details")

origin = st.selectbox("Origin Airport", origin_options)
destination = st.selectbox("Destination Airport", destination_options)
carrier = st.selectbox("Carrier", carrier_options)

sched_dep = st.text_input("Scheduled Departure Time (HH:MM)", "")
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM)", "")
year = st.number_input("Flight Year", min_value=2000, max_value=2030, value=2024)

# Convert HH:MM to minutes
def convert_to_minutes(time_str):
    try:
        h, m = map(int, time_str.strip().split(":"))
        if 0 <= h < 24 and 0 <= m < 60:
            return h * 60 + m
    except:
        return np.nan

# Predict
if st.button("Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    sched_arr_min = convert_to_minutes(sched_arr)

    if np.isnan(sched_dep_min) or np.isnan(sched_arr_min):
        st.error("❌ Please enter valid time in HH:MM format.")
    else:
        try:
            # Use encoders if available, else manual encoding
            if origin_enc:
                origin_encoded = origin_enc.transform([origin])[0]
            else:
                origin_encoded = origin_options.index(origin)

            if destination_enc:
                destination_encoded = destination_enc.transform([destination])[0]
            else:
                destination_encoded = destination_options.index(destination)

            if carrier_enc:
                carrier_encoded = carrier_enc.transform([carrier])[0]
            else:
                carrier_encoded = carrier_options.index(carrier)

            input_features = np.array([[origin_encoded, destination_encoded, carrier_encoded,
                                        sched_dep_min, sched_arr_min, year]])

            prediction = model.predict(input_features)[0]

            if prediction == 1:
                st.error("🛑 Prediction: Flight is Delayed.")
            else:
                st.success("✅ Prediction: Flight is On-Time.")

        except Exception as e:
            st.error(f"⚠️ Error in prediction: {str(e)}")
