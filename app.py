import streamlit as st
import pickle
import numpy as np
import pandas as pd

# -----------------------------
def time_to_minutes(time_str):
    try:
        h, m = map(int, str(time_str).split(':'))
        return h * 60 + m
    except:
        return np.nan

@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['model'], data['le_origin'], data['le_dest'], data['le_carrier']

# Load model and encoders
model, le_origin, le_dest, le_carrier = load_model()

# -----------------------------
st.title("✈️ Flight Delay Prediction App")
st.write("Enter flight details to predict if it will be **Delayed** or **On-Time**.")

# Dropdown options
origin_options = sorted(le_origin.classes_.tolist())
destination_options = sorted(le_dest.classes_.tolist())
carrier_options = sorted(le_carrier.classes_.tolist())

# Inputs
origin = st.selectbox("Origin Airport Code:", origin_options)
destination = st.selectbox("Destination Airport Code:", destination_options)
carrier = st.selectbox("Airline Carrier:", carrier_options)

year = st.number_input("Year of Flight (e.g., 2023)", min_value=2000, max_value=2100, value=2023)
month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=5)
sched_dep = st.text_input("Scheduled Departure Time (HH:MM):", "09:30")
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM):", "11:15")

# -----------------------------
if st.button("Predict"):
    sched_dep_min = time_to_minutes(sched_dep)
    sched_arr_min = time_to_minutes(sched_arr)

    if np.isnan(sched_dep_min) or np.isnan(sched_arr_min):
        st.error("⚠️ Invalid time format. Please use HH:MM (e.g., 09:30).")
    else:
        input_data = {
            'origin_enc': le_origin.transform([origin])[0],
            'destination_enc': le_dest.transform([destination])[0],
            'carrier_enc': le_carrier.transform([carrier])[0],
            'year': year,
            'month': month,
            'sched_dep_min': sched_dep_min,
            'sched_arr_min': sched_arr_min
        }

        input_df = pd.DataFrame([input_data])

        pred = model.predict(input_df)[0]
        result = "🟥 Delayed" if pred == 1 else "🟩 On-Time"
        st.success(f"Prediction: **{result}**")
