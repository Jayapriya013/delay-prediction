import streamlit as st
import pickle

# Title
st.title("✈️ Flight Delay Prediction")

# Load model and encoders
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("origin_enc.pkl", "rb") as f:
    origin_enc = pickle.load(f)
with open("destination_enc.pkl", "rb") as f:
    destination_enc = pickle.load(f)
with open("carrier_enc.pkl", "rb") as f:
    carrier_enc = pickle.load(f)

# Function to convert HH:MM to total minutes
def time_to_minutes(t):
    try:
        h, m = map(int, t.split(":"))
        return h * 60 + m
    except:
        st.error("⛔ Please enter time in HH:MM format (e.g., 08:30)")
        return None

# --- Form inputs ---
origin = st.selectbox("Origin Airport", origin_enc.classes_)
destination = st.selectbox("Destination Airport", destination_enc.classes_)
carrier = st.selectbox("Carrier", carrier_enc.classes_)

sched_dep_time = st.text_input("Scheduled Departure Time (HH:MM)", "08:00")
sched_arr_time = st.text_input("Scheduled Arrival Time (HH:MM)", "10:00")
actual_dep_time = st.text_input("Actual Departure Time (HH:MM)", "08:10")

year = st.number_input("Flight Year", min_value=2000, max_value=2100, value=2020)

# --- Predict Button ---
if st.button("Predict Delay"):
    # Convert time to minutes
    sched_dep_min = time_to_minutes(sched_dep_time)
    sched_arr_min = time_to_minutes(sched_arr_time)
    actual_dep_min = time_to_minutes(actual_dep_time)

    if None not in (sched_dep_min, sched_arr_min, actual_dep_min):
        try:
            # Encode categorical features
            origin_code = origin_enc.transform([origin])[0]
            destination_code = destination_enc.transform([destination])[0]
            carrier_code = carrier_enc.transform([carrier])[0]

            # Create input vector
            X = [[origin_code, destination_code, carrier_code,
                  sched_dep_min, sched_arr_min, actual_dep_min, year]]

            # Predict
            prediction = model.predict(X)[0]

            # Show result
            if prediction == 1:
                st.error("🟥 Prediction: Delayed")
            else:
                st.success("🟩 Prediction: On-Time")
        except Exception as e:
            st.error(f"❌ Prediction Error: {str(e)}")
