import streamlit as st
import numpy as np
from joblib import load
import random

def recommendation():
    # Load the trained Random Forest model
    model = load('RandomForest.joblib')

    # Title of the app
    st.title("Crop Recommendation System")

    # Initialize session state for inputs if they don't exist
    if 'N' not in st.session_state:
        st.session_state.N = 0
    if 'P' not in st.session_state:
        st.session_state.P = 0
    if 'K' not in st.session_state:
        st.session_state.K = 0
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.0
    if 'humidity' not in st.session_state:
        st.session_state.humidity = 0
    if 'ph' not in st.session_state:
        st.session_state.ph = 0.0
    if 'rainfall' not in st.session_state:
        st.session_state.rainfall = 0.0

    # Create three columns for inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.N = st.number_input("Nitrogen (N)", min_value=0, max_value=500, value=st.session_state.N, step=1)

    with col2:
        st.session_state.P = st.number_input("Phosphorus (P)", min_value=0, max_value=500, value=st.session_state.P, step=1)

    with col3:
        st.session_state.K = st.number_input("Potassium (K)", min_value=0, max_value=500, value=st.session_state.K, step=1)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.session_state.temperature = st.number_input("Temp (°C)", min_value=0.0, max_value=50.0, value=st.session_state.temperature, step=0.1)

    with col5:
        st.session_state.humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=st.session_state.humidity, step=1)

    with col6:
        st.session_state.ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=st.session_state.ph, step=0.1)

    # Create a row for rainfall with an empty column for center alignment
    col7, col8, col9 = st.columns([1, 2, 1])  # Adjust the weights for centering

    with col7:
        pass  # Leave this column empty

    with col8:
        st.session_state.rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=st.session_state.rainfall, step=0.1)

    with col9:
        pass  # Leave this column empty

    # Create a row for buttons
    button_col1, button_col2 = st.columns(2)

    with button_col1:
        if st.button("Generate Test Values"):
            # Generate random values
            st.session_state.N = random.randint(0, 500)
            st.session_state.P = random.randint(0, 500)
            st.session_state.K = random.randint(0, 500)
            st.session_state.temperature = random.uniform(0.0, 50.0)
            st.session_state.humidity = random.randint(0, 100)
            st.session_state.ph = random.uniform(0.0, 14.0)
            st.session_state.rainfall = random.uniform(0.0, 500.0)

            # Display a success message
            st.success("Test values generated!")

    with button_col2:
        if st.button("Predict"):
            # Check input values against their limits
            errors = []
            
            if st.session_state.N < 0 or st.session_state.N > 500:
                errors.append("Nitrogen (N) value should be between 0 and 500.")
            if st.session_state.P < 0 or st.session_state.P > 500:
                errors.append("Phosphorus (P) value should be between 0 and 500.")
            if st.session_state.K < 0 or st.session_state.K > 500:
                errors.append("Potassium (K) value should be between 0 and 500.")
            if st.session_state.temperature < 0.0 or st.session_state.temperature > 50.0:
                errors.append("Temperature value should be between 0°C and 50°C.")
            if st.session_state.humidity < 0 or st.session_state.humidity > 100:
                errors.append("Humidity value should be between 0% and 100%.")
            if st.session_state.ph < 0.0 or st.session_state.ph > 14.0:
                errors.append("Soil pH value should be between 0.0 and 14.0.")
            if st.session_state.rainfall < 0.0 or st.session_state.rainfall > 500.0:
                errors.append("Rainfall value should be between 0.0 and 500.0 mm.")

            # If there are any errors, display them
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create a numpy array for the input data
                input_data = np.array([[st.session_state.N, st.session_state.P, st.session_state.K,
                                         st.session_state.temperature, st.session_state.humidity,
                                         st.session_state.ph, st.session_state.rainfall]])
                
                # Make prediction
                prediction = model.predict(input_data)

                # Display the prediction in a center-aligned container at the bottom
                st.markdown(
                    "<div style='text-align: center; margin-top: 120px;'>"
                    f"<h2 style='color: #00695c;'> The recommended crop is: <strong>{prediction[0]}</strong> </h2>"
                    "</div>",
                    unsafe_allow_html=True
                )

    # Optional: Add some spacing at the bottom
    st.write("\n")

# Call the recommendation function to run the app
if __name__ == "__main__":
    recommendation()
