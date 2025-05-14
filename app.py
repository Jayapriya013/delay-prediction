import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the XGBoost model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Streamlit page config
st.set_page_config(page_title="Flight Delay Predictor", layout="centered", page_icon="🛫")

st.title("🛬 Flight Delay Prediction App")

# UI Inputs
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

# Predict button
if st.button("Predict Delay"):
    sched_dep_min = time_to_minutes(sched_dep)
    sched_arr_min = time_to_minutes(sched_arr)
    actual_dep_min = time_to_minutes(actual_dep)

    if None in (sched_dep_min, sched_arr_min, actual_dep_min):
        st.error("❌ Please enter valid time values in HH:MM format.")
    else:
        # Prepare input
        input_data = {
            "DEST_AIRPORT": dest_airport,
            "CARRIER": carrier,
            "SCHEDULED_DEP_TIME": sched_dep_min,
            "SCHEDULED_ARR_TIME": sched_arr_min,
            "ACTUAL_DEP_TIME": actual_dep_min,
            "FLIGHT_YEAR": flight_year
        }

        input_df = pd.DataFrame([input_data])

        # Convert categorical columns if needed (make sure this matches training preprocessing)
        # Example: If LabelEncoder or OneHotEncoder was used, you must match that here.
        # For now, we assume model handles it internally (via pipeline or encoding inside model training)

        try:
            prediction = model.predict(input_df)

            if prediction[0] == 1:
                st.error("🛑 Prediction: Flight is Delayed.")
            else:
                st.success("✅ Prediction: Flight is On-Time.")
        except Exception as e:
            st.error(f"⚠️ Error during prediction: {str(e)}")
