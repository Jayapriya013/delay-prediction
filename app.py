import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load model safely
with open("model.pkl", "rb") as f:
    loaded_data = pickle.load(f)

# If your model was saved as a dict: {"model": xgb_model}
# Update this line based on the actual key in your pkl
if isinstance(loaded_data, dict):
    model = loaded_data.get("model")
else:
    model = loaded_data

# Streamlit UI
st.title("🛬 Flight Delay Prediction App")

dest_airport = st.selectbox("Destination Airport", ["ATL", "LAX", "ORD", "DFW", "DEN", "JFK", "SFO", "SEA", "LAS", "MCO"])
carrier = st.selectbox("Carrier", ["AA", "DL", "UA", "WN", "AS", "NK", "B6", "F9"])
sched_dep = st.text_input("Scheduled Departure Time (HH:MM)", "10:00")
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM)", "12:30")
actual_dep = st.text_input("Actual Departure Time (HH:MM)", "10:20")
flight_year = st.number_input("Flight Year", min_value=2000, max_value=2030, value=2025)

def time_to_minutes(t):
    try:
        h, m = map(int, t.split(":"))
        return h * 60 + m
    except:
        return None

if st.button("Predict Delay"):
    sched_dep_min = time_to_minutes(sched_dep)
    sched_arr_min = time_to_minutes(sched_arr)
    actual_dep_min = time_to_minutes(actual_dep)

    if None in (sched_dep_min, sched_arr_min, actual_dep_min):
        st.error("❌ Please enter valid time values in HH:MM format.")
    elif model is None:
        st.error("❌ Model not loaded correctly.")
    else:
        try:
            input_data = pd.DataFrame([{
                "DEST_AIRPORT": dest_airport,
                "CARRIER": carrier,
                "SCHEDULED_DEP_TIME": sched_dep_min,
                "SCHEDULED_ARR_TIME": sched_arr_min,
                "ACTUAL_DEP_TIME": actual_dep_min,
                "FLIGHT_YEAR": flight_year
            }])

            prediction = model.predict(input_data)

            if prediction[0] == 1:
                st.error("🛑 Prediction: Flight is Delayed.")
            else:
                st.success("✅ Prediction: Flight is On-Time.")
        except Exception as e:
            st.error(f"⚠️ Error during prediction: {str(e)}")
