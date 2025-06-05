import requests

class AgentA:
    def __init__(self):
        self.order_service_url = "http://localhost:5000/orders"
        self.inventory_service_url = "http://localhost:5001/inventory"

    def create_order(self, item, quantity):
        print(f"Agent A: Creating order for {item}, quantity {quantity}")
        # Check inventory with Agent B
        response = requests.get(f"{self.inventory_service_url}/{item}")
        inventory_data = response.json()
        available_quantity = inventory_data['quantity']

        if available_quantity >= quantity:
            # Register order
            order_data = {'item': item, 'quantity': quantity}
            order_response = requests.post(self.order_service_url, json=order_data)
            print(f"Agent A: Order registered: {order_response.json()}")
            # Request Agent B to update inventory
            update_data = {'quantity': quantity}
            update_response = requests.put(f"{self.inventory_service_url}/{item}", json=update_data)
            print(f"Agent A: Agent B response for inventory update: {update_response.json()}")
        else:
            print(f"Agent A: Insufficient inventory. Current quantity: {available_quantity}")

class AgentB:
    def __init__(self):
        self.inventory_service_url = "http://localhost:5001/inventory"

    def check_inventory(self, item):
        print(f"Agent B: Checking inventory for {item}")
        response = requests.get(f"{self.inventory_service_url}/{item}")
        print(f"Agent B: Current inventory: {response.json()}")
        return response.json()

    def update_inventory(self, item, quantity):
        print(f"Agent B: Updating inventory for {item}, reducing quantity {quantity}")
        update_data = {'quantity': quantity}
        response = requests.put(f"{self.inventory_service_url}/{item}", json=update_data)
        print(f"Agent B: Inventory updated: {response.json()}")

if __name__ == "__main__":
    agent_a = AgentA()
    agent_b = AgentB()

    # Scenario: Customer places an order for 30 units of item1
    agent_a.create_order("item1", 30)