# run.py
from app import app
from config.config import HOST, PORT
from threading import Thread
from app.routes import consume_messages

# Start Kafka consumer on a separate thread before starting the Flask server
if __name__ == '__main__':
    # Start consuming messages in a separate thread
    Thread(target=consume_messages, daemon=True).start()
    
    # Run the Flask app
    app.run(host=HOST, port=PORT, debug=True)
