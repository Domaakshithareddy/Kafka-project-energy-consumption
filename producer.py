import requests
import json
from kafka import KafkaProducer
import time
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = "gSHiMoyLOWks5Fcvfh07qyrZaNsCL9gDOEUbhqsV"
URL = "https://api.eia.gov/v2/electricity/retail-sales/data/"
TOPIC = "eia_electricity_data"
BOOTSTRAP_SERVERS = ["localhost:9092"]

def fetch_eia_data(start_period):
    params = {
        "api_key": API_KEY,
        "frequency": "monthly",
        "data[0]": "price",
        "data[1]": "sales",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "start": start_period,
        "end": (datetime.strptime(start_period, "%Y-%m") + timedelta(days=31)).strftime("%Y-%m"),
        "length": 1  # Fetch one record per request
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()
        if "response" in data and "data" in data["response"] and data["response"]["data"]:
            return data["response"]["data"][0]
        return None
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None

def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    
    current_period = datetime(2020, 1, 1)
    end_period = datetime(2025, 4, 1)  # Up to current month
    
    while current_period < end_period:
        period_str = current_period.strftime("%Y-%m")
        record = fetch_eia_data(period_str)
        if record:
            producer.send(TOPIC, value=record)
            logger.info(f"Sent record for {period_str}")
            producer.flush()
        current_period += timedelta(days=31)  # Approximate one month
        time.sleep(2)  # Wait 2 seconds before next month

if __name__ == "__main__":
    main()