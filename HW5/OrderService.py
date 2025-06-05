from mcp_base import MCPServer
import requests
import json
from flask import Flask, request, jsonify

class OrderService(MCPServer):
    def __init__(self, inventory_service_url="http://localhost:5001"):
        super().__init__("order_service", 5000)
        self.orders = []
        self.inventory_service_url = inventory_service_url
        self.register_routes()
        self.register_error_handlers()
        
    def register_routes(self):
        @self.app.route('/orders', methods=['POST'])
        def create_order():
            try:
                print("Creating order")
                data = request.get_json()
                
                # Validate input
                if not data or 'item' not in data or 'quantity' not in data:
                    return jsonify({'error': 'Invalid input'}), 400
                
                # Check inventory first
                inventory_check = requests.get(
                    f"{self.inventory_service_url}/inventory/{data['item']}"
                )
                
                if inventory_check.status_code != 200:
                    return jsonify({'error': 'Inventory service unavailable'}), 503
                    
                inventory_data = inventory_check.json()
                if inventory_data['quantity'] < data['quantity']:
                    return jsonify({'error': 'Insufficient inventory'}), 400
                
                # Update inventory
                update_response = requests.put(
                    f"{self.inventory_service_url}/inventory/{data['item']}",
                    json={'quantity': data['quantity']}
                )
                
                if update_response.status_code != 200:
                    return jsonify({'error': 'Failed to update inventory'}), 500
                
                # Create order
                order = {
                    'id': len(self.orders) + 1,
                    'item': data['item'],
                    'quantity': data['quantity'],
                    'status': 'confirmed'
                }
                self.orders.append(order)
                
                self.logger.info(f"Order created: {json.dumps(order)}")
                return jsonify({
                    'message': 'Order registered successfully',
                    'order': order
                }), 201
                
            except requests.RequestException as e:
                self.logger.error(f"Service communication error: {str(e)}")
                return jsonify({'error': 'Service communication error'}), 503
            except Exception as e:
                self.logger.error(f"Error processing order: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500

        @self.app.route('/orders', methods=['GET'])
        def get_orders():
            print("Getting orders")
            return jsonify(self.orders), 200

if __name__ == '__main__':
    order_service = OrderService()
    order_service.run()