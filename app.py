from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Battery Monitoring System"

def get_config():
    # Create a new connection for this request
    config_conn = sqlite3.connect('config.db')
    config_c = config_conn.cursor()

    config_c.execute("SELECT * FROM config")
    config = config_c.fetchone()

    # Close the connection after using it
    config_conn.close()

    return config[1], config[2]

@app.route('/configure', methods=['POST'])
def configure():
    data = request.get_json()
    new_threshold = data.get('threshold')
    new_interval = data.get('interval')

    if new_threshold is not None and new_interval is not None:
        # Create a new connection for this request
        config_conn = sqlite3.connect('config.db')
        config_c = config_conn.cursor()

        # Update the configuration in the database
        config_c.execute("UPDATE config SET threshold = ?, interval = ?", (new_threshold, new_interval))
        config_conn.commit()

        # Close the connection after using it
        config_conn.close()

        return jsonify({'message': 'Configuration updated successfully'}), 200
    else:
        return jsonify({'message': 'Invalid configuration data'}), 400

@app.route('/current_config', methods=['GET'])
def get_current_config():
    threshold, interval = get_config()
    return jsonify({'threshold': threshold, 'interval': interval}), 200

@app.route('/alarms', methods=['GET'])
def get_alarms():
    # Create a new connection for this request
    conn = sqlite3.connect('alarms.db')
    c = conn.cursor()

    c.execute("SELECT * FROM alarms")
    alarms = c.fetchall()

    # Close the connection after using it
    conn.close()

    return jsonify({'alarms': alarms}), 200

if __name__ == '__main__':
    app.run(debug=True)
