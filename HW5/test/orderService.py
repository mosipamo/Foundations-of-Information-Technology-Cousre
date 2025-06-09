from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

orders = []

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    item = data.get('item')
    quantity = data.get('quantity')

    # Forward inventory update
    inventory_response = requests.put(f"http://localhost:5001/inventory/{item}", json={'quantity': quantity})
    
    if inventory_response.status_code == 200:
        order = {
            'id': len(orders) + 1,
            'item': item,
            'quantity': quantity
        }
        orders.append(order)
        return jsonify({'message': 'Order registered successfully', 'order': order}), 201
    else:
        return jsonify({'message': 'Failed to update inventory'}), 400

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
