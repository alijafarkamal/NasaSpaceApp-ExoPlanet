import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model and scaler
with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Define feature names (these must match the order used in training)
FEATURE_NAMES = [
    'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
    'koi_insol', 'koi_model_snr', 'koi_fpflag_nt', 'koi_fpflag_ss',
    'koi_fpflag_co', 'koi_fpflag_ec', 'koi_steff', 'koi_slogg',
    'koi_srad', 'koi_kepmag'
]

# Streamlit app title
st.title("🪐 Exoplanet Prediction App")
st.write("Enter the features below to predict whether it's a confirmed exoplanet, false positive, or candidate.")

# Input fields for all features
input_values = []

for feature in FEATURE_NAMES:
    user_input = st.text_input(f"Enter value for {feature}")
    try:
        val = float(user_input)
    except ValueError:
        st.warning(f"Please enter a valid number for {feature}")
        val = 0.0  # fallback
    input_values.append(val)
# Predict button
if st.button("Predict"):
    try:
        # Create input DataFrame
        input_df = pd.DataFrame([input_values], columns=FEATURE_NAMES)

        # Scale
        input_scaled = scaler.transform(input_df)

        # Predict
        prediction = model.predict(input_scaled)[0]

        # Show prediction
        st.success(f"🌍 Prediction: **{prediction}**")

    except Exception as e:
        st.error(f"Error during prediction: {e}")
