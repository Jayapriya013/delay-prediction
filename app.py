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
sched_arr = st.text_input("Scheduled Arrival Time (HH:MM)", "10:45")
year = st.number_input("Flight Year", min_value=2000, max_value=2030, value=2024)

def convert_to_minutes(time_str):
    try:
        h, m = map(int, time_str.split(":"))
        return h * 60 + m
    except:
        return np.nan

# Prediction Logic
if st.button("Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    sched_arr_min = convert_to_minutes(sched_arr)

    if np.isnan(sched_dep_min) or np.isnan(sched_arr_min):
        st.error("❌ Invalid time format. Use HH:MM (e.g., 13:30).")
    else:
        # ✅ Business logic rule
        if sched_dep_min > sched_arr_min + 15:
            st.warning("⚠️ Based on time logic: Flight is likely to be **Delayed** (Departure > Arrival + 15 mins).")
        elif sched_dep_min <= sched_arr_min + 15:
            st.success("✅ Based on time logic: Flight is likely to be **On-Time** (Departure within 15 mins of Arrival).")
        else:
            # Fallback to model prediction
            X = np.array([[ 
                le_origin.transform([origin])[0],
                le_dest.transform([destination])[0],
                le_carrier.transform([carrier])[0],
                sched_dep_min,
                sched_arr_min,
                year
            ]])
            pred = model.predict(X)[0]
            if pred == 1:
                st.error("🛑 Model Prediction: Flight is likely to be Delayed.")
            else:
                st.success("✅ Model Prediction: Flight is likely to be On-Time.")
