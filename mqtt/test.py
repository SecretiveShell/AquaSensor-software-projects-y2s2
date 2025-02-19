import asyncio
import gmqtt

# MQTT Broker details
BROKER = "localhost"  # Replace with your broker address
PORT = 1883
CLIENT_ID = "test_publisher"

# Data to be published
MESSAGES = [
    ("sensor/941205", "{18-02-25,12:03:28,941205,2991,3.85,106.44,14.11}"),
    ("sensor/941205", "{18-02-25,12:03:28,941205,2991,3.85,106.44,14.11}"),
    (
        "aqua/941205",
        '{"t":s,"m":10,"c":2991,"p0":3.85,"p1":106.44,"p2":14.11,"p3":14.11,"i":23.00,"v":5.14}',
    ),
    ("sensor/941184", "{18-02-25,12:02:29,941184,1555,7.76,105.64,12.68}"),
    ("sensor/941184", "{18-02-25,12:02:29,941184,1555,7.76,105.64,12.68}"),
    (
        "aqua/941184",
        '{"t":s,"ts":52-39-75 133:42:00,"ms":1125946,"rr":3,"m":10,"c":1555,"f":1562,"p0":7.76,"p1":105.64,"p2":12.68,"p3":12.68,"i":246.00,"v":5.05}',
    ),
]

client = gmqtt.Client(CLIENT_ID)


async def connect():
    await client.connect(BROKER, PORT)
    print("Connected to MQTT broker")


async def publish_messages():
    while True:
        for topic, message in MESSAGES:
            client.publish(topic, message)
            print(f"Published to {topic}: {message}")
            await asyncio.sleep(1)  # Adjust delay as needed


async def main():
    await connect()
    await publish_messages()


if __name__ == "__main__":
    asyncio.run(main())
