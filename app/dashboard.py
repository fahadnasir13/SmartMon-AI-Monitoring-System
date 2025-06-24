import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sklearn.ensemble import IsolationForest
from prophet import Prophet

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SmartMon – AI Monitoring",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .main {
        background-color: #0d1117;
    }
    h1, h3, h4 {
        color: #00f0ff;
    }
    .css-1aumxhk {
        background-color: #161b22;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0,240,255,0.1);
    }
    div.row-widget.stRadio > div {
        flex-direction: row;
        gap: 20px;
    }
    label[data-baseweb="radio"] > div {
        background-color: #161b22;
        color: #00f0ff;
        padding: 10px 20px;
        border-radius: 10px;
        border: 1px solid #00f0ff;
        transition: 0.2s;
    }
    label[data-baseweb="radio"]:hover {
        background-color: #1f2937;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("<h1 style='text-align: center; font-size: 50px;'>SmartMon</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>AI Monitoring System</h3>", unsafe_allow_html=True)
st.markdown("---")

# ==================== TOGGLE VIEW ====================
st.markdown("<h4 style='color:#00f0ff;'>📊 Monitoring Panel</h4>", unsafe_allow_html=True)
toggle_option = st.radio("Choose view:", ["📈 Live Dashboard", "🔮 CPU Forecast"], horizontal=True)

# ==================== LOAD DATA ====================
log_file = "data/metrics_log.csv"
if not os.path.exists(log_file):
    st.warning("⚠️ No monitoring data found.")
    st.stop()

df = pd.read_csv(log_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# ==================== LIVE DASHBOARD ====================
if toggle_option == "📈 Live Dashboard":
    st.subheader("📈 Real-Time Monitoring with Anomaly Detection")

    # Date filter
    date_range = st.date_input("📅 Filter by Date", [df['timestamp'].min().date(), df['timestamp'].max().date()])
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    # Isolation Forest Anomaly Detection
    features = ['cpu_percent', 'memory_percent', 'disk_percent']
    df.dropna(subset=features, inplace=True)
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(df[features])
    df['is_anomaly'] = df['anomaly'] == -1

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧠 CPU Usage with Anomalies")
        fig_cpu = px.line(df, x='timestamp', y='cpu_percent', title="CPU Usage (%)", labels={'cpu_percent': 'CPU %'})
        fig_cpu.add_scatter(x=df[df['is_anomaly']]['timestamp'], y=df[df['is_anomaly']]['cpu_percent'],
                            mode='markers', name='Anomalies', marker=dict(color='red', size=8))
        st.plotly_chart(fig_cpu, use_container_width=True)

    with col2:
        st.markdown("### 💾 Memory Usage with Anomalies")
        fig_mem = px.line(df, x='timestamp', y='memory_percent', title="Memory Usage (%)", labels={'memory_percent': 'Memory %'})
        fig_mem.add_scatter(x=df[df['is_anomaly']]['timestamp'], y=df[df['is_anomaly']]['memory_percent'],
                            mode='markers', name='Anomalies', marker=dict(color='red', size=8))
        st.plotly_chart(fig_mem, use_container_width=True)

    st.markdown("### 💽 Disk Usage with Anomalies")
    fig_disk = px.line(df, x='timestamp', y='disk_percent', title="Disk Usage (%)", labels={'disk_percent': 'Disk %'})
    fig_disk.add_scatter(x=df[df['is_anomaly']]['timestamp'], y=df[df['is_anomaly']]['disk_percent'],
                         mode='markers', name='Anomalies', marker=dict(color='red', size=8))
    st.plotly_chart(fig_disk, use_container_width=True)

# ==================== FORECASTING VIEW ====================
elif toggle_option == "🔮 CPU Forecast":
    st.subheader("🔮 CPU Usage Forecast with Prophet")

    cpu_data = df[['timestamp', 'cpu_percent']].rename(columns={'timestamp': 'ds', 'cpu_percent': 'y'})

    period = st.slider("⏱️ Forecast minutes ahead", 10, 180, 60)

    model = Prophet()
    model.fit(cpu_data)

    future = model.make_future_dataframe(periods=period, freq='min')
    forecast = model.predict(future)

    st.markdown("### 📉 Forecasted CPU Usage")
    fig_forecast = px.line(forecast, x='ds', y='yhat', title="CPU Forecast", labels={'yhat': 'CPU %'})
    st.plotly_chart(fig_forecast, use_container_width=True)

    st.markdown("### 🔍 Trends & Seasonality")
    st.write("Prophet components:")
    st.pyplot(model.plot_components(forecast))
