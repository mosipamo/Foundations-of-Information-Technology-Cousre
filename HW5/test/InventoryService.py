from flask import Flask, request, jsonify

app = Flask(__name__)

inventory = {
    "item1": 100,
    "item2": 50
}

@app.route('/inventory/<item>', methods=['GET'])
def check_inventory(item):
    quantity = inventory.get(item, 0)
    return jsonify({'item': item, 'quantity': quantity}), 200

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route('/inventory/<item>', methods=['PUT'])
def update_inventory(item):
    data = request.get_json()
    quantity = data.get('quantity', 0)
    if item in inventory:
        inventory[item] -= quantity
        return jsonify({'message': f'Inventory for {item} updated', 'new_quantity': inventory[item]}), 200
    return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
