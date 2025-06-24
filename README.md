🧠 SmartMon – AI Monitoring System

SmartMon is an AI-powered system monitoring dashboard built with Streamlit. It displays real-time system metrics (CPU, RAM, Disk), detects anomalies using Isolation Forest, and predicts CPU usage with Prophet.


## 🚀 Features

- 📊 Real-time monitoring (CPU, RAM, Disk)
- ⚠️ Anomaly detection using Isolation Forest
- 🔮 Forecasting with Prophet
- 🖥️ Interactive charts via Plotly
- 📅 Date filters for log viewing
- 👨‍💼 Admin panel (add/delete user, report access)
- 🌙 Dark-themed modern UI

## 📂 Folder Structure

├── app/
│ ├── dashboard.py # Streamlit app
│ ├── system_metrics.py # Metrics logger
│ └── alerts/
│ └── email_alert.py # Email alerts (optional)
├── data/
│ └── metrics_log.csv # Logged system metrics
├── requirements.txt
├── README.md



## 🛠️ Installation

```bash
git clone https://github.com/your-username/SmartMon-AI-Monitoring-System.git
cd SmartMon-AI-Monitoring-System
pip install -r requirements.txt

🧪 Run the App


# Start the metrics logger in background
python app/system_metrics.py

# Then launch the dashboard
streamlit run app/dashboard.py

📬 Contact

Built with ❤️ by Fahad Nasir
