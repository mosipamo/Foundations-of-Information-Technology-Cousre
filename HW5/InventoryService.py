from flask import Flask, request, jsonify
from mcp_base import MCPServer
import json

class InventoryService(MCPServer):
    def __init__(self):
        super().__init__("inventory_service", 5001)
        self.inventory = {
            'item1': 100,
            'item2': 50
        }
        self.register_routes()
        self.register_error_handlers()
        
    def register_routes(self):
        @self.app.route('/inventory/<item>', methods=['GET'])
        def check_inventory(item):
            try:
                print("Checking inventory")
                if item not in self.inventory:
                    return jsonify({'error': 'Item not found'}), 404
                    
                quantity = self.inventory.get(item)
                self.logger.info(f"Inventory check for {item}: {quantity}")
                return jsonify({'item': item, 'quantity': quantity}), 200
                
            except Exception as e:
                self.logger.error(f"Error checking inventory: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500

        @self.app.route('/inventory/<item>', methods=['PUT'])
        def update_inventory(item):
            try:
                print("Updating inventory") 
                if item not in self.inventory:
                    return jsonify({'error': 'Item not found'}), 404
                    
                data = request.get_json()
                if not data or 'quantity' not in data:
                    return jsonify({'error': 'Invalid input'}), 400
                    
                quantity = data['quantity']
                if not isinstance(quantity, (int, float)) or quantity < 0:
                    return jsonify({'error': 'Invalid quantity'}), 400
                    
                if self.inventory[item] < quantity:
                    return jsonify({'error': 'Insufficient inventory'}), 400
                    
                self.inventory[item] -= quantity
                self.logger.info(f"Updated inventory for {item}: {self.inventory[item]}")
                
                return jsonify({
                    'message': f'Inventory for {item} updated',
                    'new_quantity': self.inventory[item]
                }), 200
                
            except Exception as e:
                self.logger.error(f"Error updating inventory: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500

        @self.app.route('/inventory', methods=['GET'])
        def get_all_inventory():
            return jsonify(self.inventory), 200

if __name__ == '__main__':
    inventory_service = InventoryService()
    inventory_service.run()