import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Introduction - Food Delivery Time Predictor",
    page_icon="📦",
    layout="centered"
)

# Header with improved styling
st.title("📦 Food Delivery Time Prediction System")
st.markdown("""
<style>
    .main h1 {
        font-size: 3rem;
        color: #FF6F00;
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.divider()

# Project description
st.markdown("""
## 🧾 About This Application

Welcome to the **Food Delivery Time Prediction System**, an intelligent tool designed to help food delivery businesses and analysts understand how various operational factors impact delivery efficiency.

This predictive analytics system leverages real-world delivery data to generate insights and estimate delivery times more accurately.

### 🔍 Core Features

The prediction is based on the following input parameters:

- 📍 **Distance (Distance_km)**: The total travel distance from the restaurant to the customer in kilometers.
- 🌦️ **Weather Conditions**: Reflects the current climate such as *Clear*, *Rainy*, *Snowy*, *Foggy*, and *Windy*.
- 🚦 **Traffic Level**: Represents congestion levels on the road – *Low*, *Medium*, or *High*.
- 🛵 **Vehicle Type**: Type of vehicle used for delivery – *Bike*, *Scooter*, or *Car*.
- 🍳 **Preparation Time**: The time required to prepare the food order, measured in minutes.
- 👨‍✈️ **Courier Experience**: Indicates the delivery agent's years of experience in the field.

---

## 🎯 Purpose & Benefits

This system was developed with the following objectives in mind:

- 📈 Enhance delivery performance forecasting using historical patterns.
- 🧠 Empower operations managers to make data-driven decisions.
- ⏱️ Help reduce delivery time variances and boost customer satisfaction.

---

## 🛠️ Technology Stack

- **Streamlit**: Frontend user interface
- **Pandas**: Data manipulation
- **Altair & Plotly**: Visualization tools
- **Machine Learning**: Predictive model (integrated separately)

---

## 🚀 Get Started

Proceed to the **Prediction** page to input your delivery conditions and receive an estimated delivery time. You can also explore trends and patterns in the **Dashboard**.

Let's make deliveries faster, smarter, and more reliable!
""")
