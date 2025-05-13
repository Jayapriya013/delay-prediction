import streamlit as st
import pickle

# Load model and encoders
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

origin_enc = encoders["origin"]
destination_enc = encoders["destination"]
carrier_enc = encoders["carrier"]

# UI
st.title("✈️ Flight Delay Prediction")

# Dropdowns for encoded inputs
origins = list(origin_enc.classes_)
destinations = list(destination_enc.classes_)
carriers = list(carrier_enc.classes_)

origin = st.selectbox("Origin Airport", origins)
destination = st.selectbox("Destination Airport", destinations)
carrier = st.selectbox("Carrier", carriers)

# Scheduled and actual time as dropdowns (hour + minute)
st.subheader("Scheduled Departure Time")
sched_dep_hour = st.selectbox("Hour", list(range(0, 24)), index=8)
sched_dep_min = st.selectbox("Minute", list(range(0, 60, 5)), index=0)

st.subheader("Scheduled Arrival Time")
sched_arr_hour = st.selectbox("Hour ", list(range(0, 24)), index=10)
sched_arr_min = st.selectbox("Minute ", list(range(0, 60, 5)), index=0)

st.subheader("Actual Departure Time")
actual_dep_hour = st.selectbox("Hour  ", list(range(0, 24)), index=8)
actual_dep_min = st.selectbox("Minute  ", list(range(0, 60, 5)), index=10)

year = st.number_input("Flight Year", min_value=2000, max_value=2100, value=2020, step=1)

# Convert to minutes since midnight
sched_dep_total_min = sched_dep_hour * 60 + sched_dep_min
sched_arr_total_min = sched_arr_hour * 60 + sched_arr_min
actual_dep_total_min = actual_dep_hour * 60 + actual_dep_min

# Predict
if st.button("Predict Delay"):
    try:
        origin_code = origin_enc.transform([origin])[0]
        destination_code = destination_enc.transform([destination])[0]
        carrier_code = carrier_enc.transform([carrier])[0]

        X = [[origin_code, destination_code, carrier_code,
              sched_dep_total_min, sched_arr_total_min,
              actual_dep_total_min, year]]

        prediction = model.predict(X)[0]

        if prediction == 1:
            st.error("🟥 Prediction: Delayed")
        else:
            st.success("🟩 Prediction: On-Time")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
