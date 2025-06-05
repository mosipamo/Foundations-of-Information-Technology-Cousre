from flask import Flask, request, jsonify
import logging

class MCPServer:
    def __init__(self, name, port):
        self.app = Flask(name)
        self.port = port
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def run(self):
        self.logger.info(f"Starting {self.__class__.__name__} on port {self.port}")
        self.app.run(host='0.0.0.0', port=self.port)
        
    def register_error_handlers(self):
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Not found'}), 404

        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({'error': 'Internal server error'}), 500 