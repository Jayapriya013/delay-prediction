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

sched_dep = st.text_input("Scheduled Departure Time (HH:MM)", "12:00")
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM)", "14:00")
actual_dep = st.text_input("Actual Departure Time (HH:MM)", "12:20")
year = st.number_input("Flight Year", min_value=2000, max_value=2030, value=2024)

# Time conversion helper
def convert_to_minutes(time_str):
    try:
        h, m = map(int, time_str.split(":"))
        return h * 60 + m
    except:
        return np.nan

# Prediction
if st.button("Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    sched_arr_min = convert_to_minutes(sched_arr)
    actual_dep_min = convert_to_minutes(actual_dep)

    if np.isnan(sched_dep_min) or np.isnan(sched_arr_min) or np.isnan(actual_dep_min):
        st.error("❌ Invalid time format. Use HH:MM (e.g., 13:30).")
    else:
        # Business Rule Check
        if actual_dep_min > sched_dep_min + 15:
            st.warning("⚠️ Flight delayed by more than 15 mins (based on actual departure).")
        else:
            # Prepare input features (7 features)
            X = np.array([[ 
                le_origin.transform([origin])[0],
                le_dest.transform([destination])[0],
                le_carrier.transform([carrier])[0],
                sched_dep_min,
                sched_arr_min,
                actual_dep_min,
                year
            ]])
            pred = model.predict(X)[0]
            if pred == 1:
                st.error("🛑 Prediction: Flight is likely to be **Delayed**.")
            else:
                st.success("✅ Prediction: Flight is likely to be **On-Time**.")
