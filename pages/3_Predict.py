import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Load model and preprocessor
@st.cache_resource
def load_models():
    model_path = Path("model/ridge_model.joblib")
    preprocessor_path = Path("model/preprocessor.joblib")
    
    return {
        "model": joblib.load(model_path),
        "preprocessor": joblib.load(preprocessor_path)
    }

models = load_models()

# Page configuration
st.set_page_config(
    page_title="⏱️ Delivery Time Prediction",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar - model info
with st.sidebar:
    st.markdown("## 🧠 Model Info")
    st.markdown("**Algorithm:** Ridge Regression")
    st.markdown("**Preprocessor:** Scaler + Encoder")
    st.markdown("**Features Used:**")
    st.markdown("""
    - 📏 Distance (km)  
    - ☁️ Weather Condition  
    - 🚦 Traffic Level  
    - 🕒 Time of Day  
    - 🚚 Vehicle Type  
    - ⏲️ Preparation Time  
    - 👤 Courier Experience  
    """)

# Title and intro
st.title("⏱️ Food Delivery Time Prediction")
st.markdown("Predict the delivery time based on your order details below. All fields are required.")
st.divider()

# Input Form
with st.form("prediction_form"):
    st.subheader("📝 Order Details")
    
    col1, col2 = st.columns(2)

    with col1:
        distance = st.number_input(
            "📏 Distance (km)",
            min_value=0.1,
            max_value=50.0,
            value=5.0,
            step=0.1,
            help="Delivery distance in kilometers"
        )

        weather = st.selectbox(
            "☁️ Weather Condition",
            options=["Clear", "Rainy", "Snowy", "Foggy", "Windy"],
            index=0
        )

        time_of_day = st.selectbox(
            "🕒 Time of Day",
            options=["Morning", "Afternoon", "Evening", "Night"],
            index=2
        )

    with col2:
        traffic = st.selectbox(
            "🚦 Traffic Level",
            options=["Low", "Medium", "High"],
            index=1
        )

        vehicle = st.selectbox(
            "🚚 Vehicle Type",
            options=["Bike", "Scooter", "Car"],
            index=0
        )

        prep_time = st.number_input(
            "⏲️ Preparation Time (minutes)",
            min_value=1,
            max_value=120,
            value=15,
            step=1
        )

        experience = st.number_input(
            "👤 Courier Experience (years)",
            min_value=0,
            max_value=20,
            value=3,
            step=1
        )

    submitted = st.form_submit_button("🚀 Predict Delivery Time")

# Prediction Logic
if submitted:
    try:
        with st.spinner("Making prediction..."):
            input_data = pd.DataFrame([{
                "Distance_km": distance,
                "Weather": weather,
                "Traffic_Level": traffic,
                "Time_of_Day": time_of_day,
                "Vehicle_Type": vehicle,
                "Preparation_Time_min": prep_time,
                "Courier_Experience_yrs": experience
            }])

            # Preprocess input
            X = models["preprocessor"].transform(input_data)
            prediction = models["model"].predict(X)

        # Output
        st.success("✅ Prediction completed successfully!")

        with st.container():
            st.subheader("📊 Prediction Result")
            col_r1, col_r2 = st.columns(2)

            with col_r1:
                st.metric(
                    label="🚴 Estimated Delivery Time",
                    value=f"{prediction[0]:.1f} minutes",
                    help="Predicted time from order acceptance to delivery completion"
                )

            with col_r2:
                total_time = prediction[0] + prep_time
                st.metric(
                    label="🕰️ Total Order Time",
                    value=f"{total_time:.1f} minutes",
                    help="Includes preparation and delivery time"
                )

        # Input Summary
        st.divider()
        st.subheader("📋 Input Summary")
        st.dataframe(input_data, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error("❌ An error occurred during prediction.")
        st.exception(e)
