import asyncio
import random
import datetime
import gmqtt

# MQTT Broker details
BROKER = "localhost"  # Replace with your broker address
PORT = 1883
CLIENT_ID = "test_publisher"

client = gmqtt.Client(CLIENT_ID)


def generate_sensor_data(sensor_id):
    now = datetime.datetime.now().strftime("%y-%m-%d,%H:%M:%S")
    c_value = random.randint(1000, 5000)
    p0 = round(random.uniform(1.0, 10.0), 2)
    p1 = round(random.uniform(100.0, 110.0), 2)
    p2 = round(random.uniform(10.0, 20.0), 2)
    return f"{{{now},{sensor_id},{c_value},{p0},{p1},{p2}}}"


def generate_aqua_data(sensor_id):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    ts = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
    ms = random.randint(1000000, 2000000)
    c_value = random.randint(1000, 5000)
    f_value = c_value + random.randint(1, 100)
    p0 = round(random.uniform(1.0, 10.0), 2)
    p1 = round(random.uniform(100.0, 110.0), 2)
    p2 = round(random.uniform(10.0, 20.0), 2)
    i_value = round(random.uniform(20.0, 250.0), 2)
    v_value = round(random.uniform(4.0, 6.0), 2)
    return f'{{"t":"{now}","ts":"{ts}","ms":{ms},"rr":3,"m":10,"c":{c_value},"f":{f_value},"p0":{p0},"p1":{p1},"p2":{p2},"p3":{p2},"i":{i_value},"v":{v_value}}}'


async def connect():
    await client.connect(BROKER, PORT)
    print("Connected to MQTT broker")


async def publish_messages():
    sensor_ids = [941205, 941184]
    while True:
        for sensor_id in sensor_ids:
            sensor_data = generate_sensor_data(sensor_id)
            aqua_data = generate_aqua_data(sensor_id)
            client.publish(f"sensor/{sensor_id}", sensor_data)
            print(f"Published to sensor/{sensor_id}: {sensor_data}")
            await asyncio.sleep(1)
            client.publish(f"aqua/{sensor_id}", aqua_data)
            print(f"Published to aqua/{sensor_id}: {aqua_data}")
            await asyncio.sleep(1)


async def main():
    await connect()
    await publish_messages()


if __name__ == "__main__":
    asyncio.run(main())
