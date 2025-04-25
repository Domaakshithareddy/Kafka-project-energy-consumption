import requests
import json
from kafka import KafkaProducer
import time
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from config import API_KEY

logging.getLogger("kafka").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = "Ep4uXcVkAyKXSG9vLCGlSvcgkvXffgxYEAHeJYgM"
URL = "https://api.eia.gov/v2/electricity/retail-sales/data/"
TOPIC = "eia_electricity_data"
BOOTSTRAP_SERVERS = ["localhost:9092"]

def fetch_eia_data(start_period):
    params = {
        "api_key": API_KEY,
        "frequency": "monthly",
        "data[0]": "price",
        "data[1]": "sales",
        "facets[stateid][]": "OH",
        "facets[sectorid][]": "RES",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "start": start_period,
        "end": (datetime.strptime(start_period, "%Y-%m") + relativedelta(months=1)).strftime("%Y-%m"),
        "length": 1
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()
        if "response" in data and "data" in data["response"] and data["response"]["data"]:
            return data["response"]["data"][0]
        logger.warning(f"No data found for period {start_period}")
        return None
    except requests.RequestException as e:
        logger.error(f"Error fetching data for period {start_period}: {e}")
        return None

def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    
    current_period = datetime(2019, 12, 1)
    end_period = datetime(2025, 1, 1)
    
    while current_period < end_period:
        period_str = current_period.strftime("%Y-%m")
        record = fetch_eia_data(period_str)
        if record:
            producer.send(TOPIC, value=record)
            logger.info(f"Sent record for Ohio Residential {period_str}: {record}")
            producer.flush()
        else:
            logger.info(f"Skipping period {period_str} due to no data")
        current_period += relativedelta(months=1)
        time.sleep(2)

if __name__ == "__main__":
    main()