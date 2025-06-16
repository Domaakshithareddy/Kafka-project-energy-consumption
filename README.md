
# Kafka Project: Energy Consumption Streaming Pipeline

This project demonstrates real-time data streaming for energy consumption using Apache Kafka. It simulates consumption data generation, Kafka topic streaming, and real-time processing using a Kafka consumer.

---

## Technologies Used

* Python
* Apache Kafka
* Kafka Python library
* Pandas
* JSON

---

## Project Structure

```
├── producer.py         # Sends data to Kafka topic
├── consumer.py         # Reads and processes data from Kafka
├── requirements.txt    # Required Python packages
├── imdex.html          # Shows histogram of sales and prices
```

---

## Prerequisites

Ensure the following are installed on your system:

* Python 3.7+
* Apache Kafka and Zookeeper
* Kafka-Python: `pip install kafka-python`
* Other dependencies: `pip install -r requirements.txt`

---

## Execution Steps

### 1. Start Zookeeper and Kafka Server

Start Zookeeper:

```bash
zookeeper-server-start.sh config/zookeeper.properties
```

In a new terminal, start Kafka:

```bash
kafka-server-start.sh config/server.properties
```

> Make sure both Zookeeper and Kafka servers are running before proceeding.

---

### 2. Create Kafka Topic

```bash
kafka-topics.sh --create --topic energy-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

### 3. Start Kafka Producer

Send the generated data to Kafka topic:

```bash
python producer.py
```

This script reads data from the file and pushes it to the `energy-data` topic.

---

### 4. Start Kafka Consumer

Consume the streamed data:

```bash
python consumer.py
```

This script reads messages from the Kafka topic and processes or prints them to the console.

---

### 5. Open index.html

This shows the histogram of sales and prices in the web page.

---
