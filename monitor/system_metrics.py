import psutil
import time
import datetime
import csv
import os
from alerts.email_alert import send_alert  # Import email function

# Constants
LOG_FILE = "data/metrics_log.csv"
CPU_THRESHOLD = 80  # % usage to trigger alert

# Ensure 'data' folder exists
os.makedirs("data", exist_ok=True)

# Create CSV file with headers if not exists
if not os.path.isfile(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'cpu_percent', 'memory_percent', 'disk_percent', 'net_sent', 'net_recv'])

# Metric collector
def get_metrics():
    return [
        datetime.datetime.now().isoformat(),
        psutil.cpu_percent(interval=1),
        psutil.virtual_memory().percent,
        psutil.disk_usage('/').percent,
        psutil.net_io_counters().bytes_sent,
        psutil.net_io_counters().bytes_recv
    ]

# Main loop
if __name__ == "__main__":
    print("📡 Monitoring system... Logging every 5 seconds... (Press Ctrl+C to stop)")

    while True:
        metrics = get_metrics()
        timestamp, cpu, mem, disk, sent, recv = metrics

        # 🔔 Trigger alert if CPU is too high
        if cpu > CPU_THRESHOLD:
            send_alert(
                subject="🚨 High CPU Alert from SmartMon",
                body=f"CPU usage at {cpu}% at {timestamp} (Threshold: {CPU_THRESHOLD}%)"
            )

        # Save to CSV
        with open(LOG_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(metrics)

        print(f"[{timestamp}] CPU: {cpu}% | RAM: {mem}% | Disk: {disk}%")
        time.sleep(5)
