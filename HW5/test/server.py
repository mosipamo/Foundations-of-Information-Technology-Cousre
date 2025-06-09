from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    agent = data.get("agent")
    message = data.get("message")

    if agent == "order":
        resp = requests.post("http://localhost:5000/orders", json=message)
        return jsonify(resp.json()), resp.status_code
    elif agent == "inventory":
        item = message.get("item")
        resp = requests.get(f"http://localhost:5001/inventory/{item}")
        return jsonify(resp.json()), resp.status_code
    else:
        return jsonify({"error": "Unknown agent"}), 400

@app.route('/ask', methods=['GET'])
def ask_inventory():
    agent = request.args.get("agent")
    if agent == "inventory":
        resp = requests.get("http://localhost:5001/inventory")
        return jsonify(resp.json()), resp.status_code
    return jsonify({"error": "Unknown agent"}), 400

if __name__ == '__main__':
    app.run(port=8000)
