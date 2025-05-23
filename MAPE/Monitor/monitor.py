import os
import time
import requests
from flask import Flask, jsonify

# Configuration via variables d’environnement
MONITOR_HOST = os.getenv("MONITOR_HOST", "10.0.0.20")  # IP sur laquelle écouter
MONITOR_PORT = int(os.getenv("MONITOR_PORT", "5000"))  # Port

app = Flask(__name__)

@app.route('/monitor', methods=['GET'])
def monitor():
    try:
        r = requests.get('http://10.0.0.2:8181/health', timeout=2)

        if r.status_code == 200:
            data = r.json()
            return jsonify({
                "status": "OK",
                "data": data
            })
        else:
            return jsonify({
                "status": "ERROR",
                "message": f"Status code: {r.status_code}"
            }), 500
        
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500
    
if __name__ == '__main__':
    print(f"Starting monitor on {MONITOR_HOST}:{MONITOR_PORT}")
    app.run(host=MONITOR_HOST, port=MONITOR_PORT)
    