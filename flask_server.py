from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

# === INDIVIDUAL VEHICLE DATA ===
latest_data = {
    "rpm": 0,
    "speed": 0,
    "fuel_level": 100,
    "battery_voltage": 12.6,
    "engine_temperature": 70,
    "ignition": False,
    "gps": {"lat": 0, "lon": 0},
    "dtcs": [],
    "event": None
}

@app.route("/data", methods=["POST"])
def receive_data():
    incoming = request.json
    print("[Individual] Received:", incoming)
    latest_data.update(incoming)
    return jsonify({"status": "success"}), 200

@app.route("/latest", methods=["GET"])
def get_latest_data():
    return jsonify(latest_data), 200

# === FLEET VEHICLE DATA ===
fleet_data = [
    {
        "id": "VICU-001",
        "status": "offline",
        "speed": 0,
        "fuel_level": 100,
        "rpm": 0,
        "location": {"lat": 0, "lon": 0},
        "dtcs": [],
        "engine_temperature": 70,
    },
    {
        "id": "VICU-002",
        "status": "offline",
        "speed": 0,
        "fuel_level": 100,
        "rpm": 0,
        "location": {"lat": 0, "lon": 0},
        "dtcs": [],
        "engine_temperature": 70,
    },
    {
        "id": "VICU-003",
        "status": "offline",
        "speed": 0,
        "fuel_level": 100,
        "rpm": 0,
        "location": {"lat": 0, "lon": 0},
        "dtcs": [],
        "engine_temperature": 70,
    }
]

alerts = []
reports = []

@app.route("/update_fleet/<vehicle_id>", methods=["POST"])
def update_fleet(vehicle_id):
    incoming = request.json
    print(f"[Fleet] Update for {vehicle_id}:", incoming)

    # Update fleet data
    for vehicle in fleet_data:
        if vehicle["id"] == vehicle_id:
            vehicle.update(incoming)

            # Log alerts/reports if DTCs are present
            dtcs = incoming.get("dtcs", [])
            if dtcs:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                entry = {
                    "id": vehicle_id,
                    "timestamp": timestamp,
                    "dtcs": dtcs,
                    "location": incoming.get("location", {})
                }
                alerts.append(entry)
                reports.append(entry)
            break

    return jsonify({"status": "updated"}), 200

@app.route("/fleet", methods=["GET"])
def get_fleet():
    return jsonify(fleet_data), 200

@app.route("/alerts", methods=["GET"])
def get_alerts():
    return jsonify(alerts), 200

@app.route("/reports", methods=["GET"])
def get_reports():
    return jsonify(reports), 200

@app.route("/")
def home():
    return "<h2>✅ VICU Flask API is Live</h2><p>Try /latest or /fleet</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
