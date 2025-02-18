import asyncio
import os
import json
from pydantic import BaseModel, Field, ValidationError
from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
import gmqtt
from datetime import datetime

# Retrieve and assert required environment variables
DB_URL = os.getenv("INFLUXDB_URL")
DB_TOKEN = os.getenv("INFLUXDB_TOKEN")
DB_ORG = os.getenv("INFLUXDB_ORG")
DB_BUCKET = os.getenv("INFLUXDB_BUCKET")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_CLIENT_ID = "mqtt_client"

assert DB_URL, "INFLUXDB_URL environment variable is not set."
assert DB_TOKEN, "INFLUXDB_TOKEN environment variable is not set."
assert DB_ORG, "INFLUXDB_ORG environment variable is not set."
assert DB_BUCKET, "INFLUXDB_BUCKET environment variable is not set."
assert MQTT_BROKER, "MQTT_BROKER environment variable is not set."

# Initialize InfluxDB client
influx = InfluxDBClient(url=DB_URL, token=DB_TOKEN, org=DB_ORG)
write_api = influx.write_api(write_options=ASYNCHRONOUS)

# Define Pydantic models for validation
class SensorData(BaseModel):
    timestamp: datetime
    sensor: str
    temperature: float = Field(..., gt=-50, lt=100)
    dissolved_oxygen: float = Field(..., gt=0, lt=20)

# MQTT client setup
client = gmqtt.Client(MQTT_CLIENT_ID)

def on_connect(client, flags, rc, properties):
    print("Connected to MQTT broker.")
    client.subscribe("sensor/#")

def on_message(client, topic, payload, qos, properties):
    asyncio.create_task(process_message(topic, payload))

client.on_connect = on_connect
client.on_message = on_message

async def write_to_influx(points):
    write_api.write(DB_BUCKET, record=points)  # No 'await' here

async def process_message(topic, payload):
    try:
        p = payload.decode("utf-8").strip()

        if topic.startswith("sensor/") and p.startswith("{") and p.endswith("}"):
            p = p[1:-1]
            dat = [x.strip() for x in p.split(',') if x.strip()]

            if len(dat) < 7:
                print("Invalid payload received:", p)
                return

            date, time, sensor, _, temp, _, diox = dat
            ts = f"20{date[6:8]}-{date[3:5]}-{date[0:2]}T{time}"

        else:
            print(f"Unknown topic format: {topic}")
            return

        if temp is None or diox is None:
            print("Missing required fields in payload")
            return

        sensor_data = SensorData(timestamp=ts, sensor=sensor, temperature=float(temp), dissolved_oxygen=float(diox))

        t = Point("Sensor").tag("location", sensor_data.sensor).field("Temperature", sensor_data.temperature).time(sensor_data.timestamp, WritePrecision.S)
        d = Point("Sensor").tag("location", sensor_data.sensor).field("Dissolved Oxygen", sensor_data.dissolved_oxygen).time(sensor_data.timestamp, WritePrecision.S)

        print(f"Writing to InfluxDB: {t}, {d}")
        asyncio.create_task(write_to_influx([t, d]))  # Schedule it without blocking

    except (ValueError, ValidationError) as e:
        print(f"Error processing message: {e}")

async def mqtt_loop():
    await client.connect(MQTT_BROKER)
    await asyncio.Future()  # Keep the loop running

async def main():
    await mqtt_loop()

if __name__ == "__main__":
    asyncio.run(main())
