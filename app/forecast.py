import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import os

st.set_page_config(page_title="SmartMon – CPU Forecast", layout="centered")

st.title("🔮 CPU Usage Forecast – SmartMon AI")

log_file = "data/metrics_log.csv"

# Load and prepare data
if not os.path.exists(log_file):
    st.warning("No data file found.")
    st.stop()

df = pd.read_csv(log_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Prophet needs 'ds' (date) and 'y' (target)
cpu_data = df[['timestamp', 'cpu_percent']].rename(columns={'timestamp': 'ds', 'cpu_percent': 'y'})

# Forecast horizon
periods = st.slider("⏱️ Forecast How Many Minutes?", 10, 120, 30)

# Train Prophet
m = Prophet()
m.fit(cpu_data)

# Create future dataframe
future = m.make_future_dataframe(periods=periods, freq='min')
forecast = m.predict(future)

# Show forecast chart
st.subheader("📈 Forecasted CPU Usage")
fig1 = m.plot(forecast)
st.pyplot(fig1)

# Show component breakdown
st.subheader("🧠 Trend + Seasonality")
fig2 = m.plot_components(forecast)
st.pyplot(fig2)

st.success("✅ Prediction Complete. Try adjusting the slider to see different ranges!")
