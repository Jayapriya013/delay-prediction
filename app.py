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
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM)", "13:30")
actual_dep = st.text_input("Actual Departure Time (HH:MM)", "12:10")
year = st.number_input("Flight Year", min_value=2000, max_value=2035, value=2024)

def convert_to_minutes(time_str):
    try:
        h, m = map(int, time_str.split(":"))
        return h * 60 + m
    except:
        return np.nan

# Predict
if st.button("Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    sched_arr_min = convert_to_minutes(sched_arr)
    actual_dep_min = convert_to_minutes(actual_dep)

    if np.isnan(sched_dep_min) or np.isnan(sched_arr_min) or np.isnan(actual_dep_min):
        st.error("❌ Invalid time format. Use HH:MM (e.g., 13:30).")
    else:
        # Business logic: Delay if actual departure > scheduled by 15+ mins
        delay_threshold = 15
        delay_diff = actual_dep_min - sched_dep_min

        if delay_diff > delay_threshold:
            st.warning(f"⚠️ Business Rule: Flight delayed by {delay_diff} minutes.")
        else:
            # Model-based prediction
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
                st.error("🛑 Flight is likely to be Delayed.")
            else:
                st.success("✅ Flight is likely to be On-Time.")
