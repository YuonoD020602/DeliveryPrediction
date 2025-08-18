import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("🚚 Delivery Food Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("data/Food_Delivery_Times_Cleaned.csv")

df = load_data()

# --- Filter Section ---
st.markdown("### 🔍 Filter Data")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    vehicle = st.selectbox("Vehicle", ["All"] + sorted(df["Vehicle_Type"].unique().tolist()))
with col2:
    experience_range = st.slider("Courier Experience (Years)", 0, 9, (0, 9))
with col3:
    traffic = st.selectbox("Traffic Level", ["All"] + sorted(df["Traffic_Level"].unique().tolist()))
with col4:
    time_of_day = st.selectbox("Time of Day", ["All"] + sorted(df["Time_of_Day"].unique().tolist()))
with col5:
    weather = st.selectbox("Weather", ["All"] + sorted(df["Weather"].unique().tolist()))

# --- Apply Filters ---
filtered = df[
    (df['Courier_Experience_yrs'] >= experience_range[0]) &
    (df['Courier_Experience_yrs'] <= experience_range[1])
]

if vehicle != "All":
    filtered = filtered[filtered["Vehicle_Type"] == vehicle]
if traffic != "All":
    filtered = filtered[filtered["Traffic_Level"] == traffic]
if time_of_day != "All":
    filtered = filtered[filtered["Time_of_Day"] == time_of_day]
if weather != "All":
    filtered = filtered[filtered["Weather"] == weather]

# --- Key Metrics ---
st.markdown("### 📌 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🛒 Total Orders", f"{len(filtered):,}")
col2.metric("📏 Avg Distance", f"{filtered['Distance_km'].mean():.2f} km")
col3.metric("🍳 Avg Prep Time", f"{filtered['Preparation_Time_min'].mean():.2f} mins")
col4.metric("👨‍💼 Avg Courier Exp", f"{filtered['Courier_Experience_yrs'].mean():.2f} yrs")
col5.metric("⏱️ Avg Delivery Time", f"{filtered['Delivery_Time_min'].mean():.2f} mins")

# --- Vehicle Distribution ---
st.markdown("### 🚗 Vehicle Distribution")
vehicle_counts = filtered['Vehicle_Type'].value_counts().reset_index()
vehicle_counts.columns = ['Vehicle', 'Count']
vehicle_counts['Percentage'] = (vehicle_counts['Count'] / vehicle_counts['Count'].sum() * 100).round(1)

col1, col2 = st.columns([1, 2])
with col1:
    for _, row in vehicle_counts.iterrows():
        st.markdown(f"<div style='display: flex; justify-content: space-between; padding: 5px 10px; border-bottom: 1px solid #eee;'>"
                    f"<span>{row['Vehicle']}</span><span>{row['Count']} ({row['Percentage']}%)</span></div>", unsafe_allow_html=True)
with col2:
    fig = px.pie(vehicle_counts, values='Count', names='Vehicle', hole=0.3,
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- Delivery Time by Experience ---
st.markdown("### 📈 Delivery Time by Courier Experience")
scatter = alt.Chart(filtered).mark_circle(size=60, opacity=0.7).encode(
    x=alt.X("Courier_Experience_yrs:Q", title="Experience (Years)"),
    y=alt.Y("Delivery_Time_min:Q", title="Delivery Time (Minutes)"),
    color=alt.value('#4285F4')
).properties(height=400)

trend = scatter.transform_regression('Courier_Experience_yrs', 'Delivery_Time_min').mark_line(
    color='#FB8C00', strokeWidth=3)
st.altair_chart(scatter + trend, use_container_width=True)

# --- Time of Day Distribution ---
st.markdown("### 🌞 Time of Day Distribution")
time_counts = filtered['Time_of_Day'].value_counts().reset_index()
time_counts.columns = ['Time_of_Day', 'Count']

bars = alt.Chart(time_counts).mark_bar(color='#34A853').encode(
    x=alt.X('Time_of_Day:N', sort=['Morning', 'Afternoon', 'Evening', 'Night']),
    y=alt.Y('Count:Q', title="Order Count")
)
labels = alt.Chart(time_counts).mark_text(
    align='center', baseline='middle', dy=10, fontSize=16, color='white'
).encode(
    x=alt.X('Time_of_Day:N', sort=['Morning', 'Afternoon', 'Evening', 'Night']),
    y=alt.Y('Count:Q'),
    text='Count:Q'
)
st.altair_chart(bars + labels, use_container_width=True)

# --- Traffic & Weather Distribution ---
st.markdown("### 🚦 Traffic & ☁️ Weather Distribution")
col1, col2 = st.columns(2)

with col1:
    traffic_counts = filtered['Traffic_Level'].value_counts().reset_index()
    traffic_counts.columns = ['Traffic_Level', 'Count']
    traffic_counts = traffic_counts.sort_values(by='Traffic_Level',
                                                key=lambda col: col.map({"Low": 0, "Medium": 1, "High": 2}))

    traffic_color_map = {
        "Low": "#A8E6CF",
        "Medium": "#FFD3B6",
        "High": "#FF8B94"
    }

    fig = px.pie(
        traffic_counts,
        values='Count',
        names='Traffic_Level',
        hole=0.3,
        color='Traffic_Level',
        color_discrete_map=traffic_color_map
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    weather_counts = filtered['Weather'].value_counts().reset_index()
    weather_counts.columns = ['Weather', 'Count']

    bars = alt.Chart(weather_counts).mark_bar(color='#34A853').encode(
        x=alt.X('Weather:N', sort='-y'),
        y=alt.Y('Count:Q', title="Order Count")
    )
    labels = alt.Chart(weather_counts).mark_text(
        align='center', baseline='middle', dy=10, fontSize=16, color='white'
    ).encode(
        x=alt.X('Weather:N', sort='-y'),
        y=alt.Y('Count:Q'),
        text='Count:Q'
    )
    st.altair_chart(bars + labels, use_container_width=True)

# --- Delivery Time by Factors ---
st.markdown("### 📊 Delivery Time by Factors")
factors = ['Time_of_Day', 'Vehicle_Type', 'Traffic_Level', 'Weather']
tabs = st.tabs([f.replace('_', ' ') for f in factors])

for tab, factor in zip(tabs, factors):
    with tab:
        avg_times = filtered.groupby(factor)['Delivery_Time_min'].mean().reset_index()
        avg_times.columns = [factor, 'Avg_Delivery_Time']

        bars = alt.Chart(avg_times).mark_bar(color='#FB8C00').encode(
            x=alt.X(f'{factor}:N', sort='-y'),
            y=alt.Y('Avg_Delivery_Time:Q', title="Avg Delivery Time (mins)")
        )
        labels = alt.Chart(avg_times).mark_text(
            align='center', baseline='middle', dy=10, fontSize=16, color='white'
        ).encode(
            x=alt.X(f'{factor}:N', sort='-y'),
            y=alt.Y('Avg_Delivery_Time:Q'),
            text=alt.Text('Avg_Delivery_Time:Q', format=".2f")
        )
        st.altair_chart(bars + labels, use_container_width=True)

# --- Delivery Time Histogram ---
st.markdown("### 📦 Delivery Time Distribution")
hist = alt.Chart(filtered).mark_bar(color='#FB8C00', opacity=0.9).encode(
    x=alt.X("Delivery_Time_min:Q", bin=alt.Bin(maxbins=30), title="Delivery Time (Minutes)"),
    y=alt.Y('count()', title='Order Count')
)
labels = hist.mark_text(
    align='center', baseline='middle', dy=10, fontSize=14, color='white'
).encode(
    text='count():Q'
)
st.altair_chart(hist + labels, use_container_width=True)

# --- Delivery Time by Distance & Prep Time ---
st.markdown("### 🔍 Delivery Time Relationships")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**By Distance**")
    scatter = alt.Chart(filtered).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X("Distance_km:Q"),
        y=alt.Y("Delivery_Time_min:Q"),
        color=alt.value('#34A853')
    ).properties(height=350)
    trend = scatter.transform_regression('Distance_km', 'Delivery_Time_min').mark_line(
        color='#FB8C00', strokeWidth=3)
    st.altair_chart(scatter + trend, use_container_width=True)

with col2:
    st.markdown("**By Preparation Time**")
    scatter = alt.Chart(filtered).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X("Preparation_Time_min:Q"),
        y=alt.Y("Delivery_Time_min:Q"),
        color=alt.value('#34A853')
    ).properties(height=350)
    trend = scatter.transform_regression('Preparation_Time_min', 'Delivery_Time_min').mark_line(
        color='#FB8C00', strokeWidth=3)
    st.altair_chart(scatter + trend, use_container_width=True)