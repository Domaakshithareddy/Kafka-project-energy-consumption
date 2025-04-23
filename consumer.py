from kafka import KafkaConsumer
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

logging.getLogger("kafka").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOPIC = "eia_electricity_data"
BOOTSTRAP_SERVERS = ["localhost:9092"]
PORT = 8000

latest_data = []

class DataHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(latest_data).encode("utf-8"))

def run_server():
    server = HTTPServer(("", PORT), DataHandler)
    logger.info(f"Server running on port {PORT}")
    server.serve_forever()

def main():
    global latest_data
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id='eia-consumer-group'
    )
    
    import threading
    threading.Thread(target=run_server, daemon=True).start()
    
    for message in consumer:
        record = message.value
        if record["period"] not in [d["period"] for d in latest_data]: 
            latest_data.append(record)
            latest_data.sort(key=lambda x: x["period"])  
            latest_data = latest_data[-100:]  
            logger.info(f"Received record: {record['period']}")

if __name__ == "__main__":
    main()