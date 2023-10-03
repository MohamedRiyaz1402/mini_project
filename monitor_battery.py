import psutil
from datetime import datetime
import time
import sqlite3

# Initialize database connection for configuration
config_conn = sqlite3.connect('config.db')
config_c = config_conn.cursor()

# Initialize previous percentage to None
previous_percent = None

def get_config():
    config_c.execute("SELECT * FROM config")
    config = config_c.fetchone()
    return config[1], config[2]

def update_config(new_threshold, new_interval):
    config_c.execute("UPDATE config SET threshold = ?, interval = ?", (new_threshold, new_interval))
    config_conn.commit()

# Initialize database connection for alarms
conn = sqlite3.connect('alarms.db')
c = conn.cursor()

def monitor_battery():
    global previous_percent
    while True:
        try:
            threshold, interval = get_config()

            battery = psutil.sensors_battery()
            percent = battery.percent

            if previous_percent is not None:
                if percent > threshold and previous_percent <= threshold:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    action = f"Above {threshold}%"
                    c.execute("INSERT INTO alarms (timestamp, action) VALUES (?, ?)", (current_time, action))
                    conn.commit()
                    print(f"Alert: Battery Percentage is now above {threshold}% at {current_time}")
                elif percent < threshold and previous_percent >= threshold:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    action = f"Below {threshold}%"
                    c.execute("INSERT INTO alarms (timestamp, action) VALUES (?, ?)", (current_time, action))
                    conn.commit()
                    print(f"Alert: Battery Percentage is now below {threshold}% at {current_time}")
            else:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                action = f"At {percent}%"
                c.execute("INSERT INTO alarms (timestamp, action) VALUES (?, ?)", (current_time, action))
                conn.commit()
                print(f"Initial Alert: Battery Percentage is {percent}% at {current_time}")

            previous_percent = percent

            time.sleep(interval)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    monitor_battery()