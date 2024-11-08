# config/config.py
HOST = 'localhost' 
PORT = 5000

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092, kafka2:9093, kafka3:9094'  # Replace with your Kafka server address
KAFKA_INPUT_TOPIC = 'input_images'
KAFKA_OUTPUT_TOPIC = 'output_images'