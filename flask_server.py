from flask import Flask, request, jsonify

app = Flask(__name__)
latest_data = {}

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data
    incoming = request.json
    print("Received data:", incoming)
    latest_data.update(incoming)  # <-- Fix: update dict in-place
    return jsonify({'status': 'success'}), 200


@app.route('/latest', methods=['GET'])
def get_latest_data():
    return jsonify(latest_data), 200

@app.route('/')
def home():
    return "<h2>✅ VICU Flask API is Live</h2><p>POST to <code>/data</code>, GET from <code>/latest</code></p>"


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
