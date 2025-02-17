from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import paho.mqtt.client as mqtt

import os

influx = InfluxDBClient(url=os.environ.get("DB_URL"),token=os.environ.get("DB_TOKEN"),org=os.environ.get("DB_ORG"))

def on_connect(cl,dat,flags,r,p):
    cl.subscribe("sensor/#")

def msg(c,d,m):
    p=m.payload.decode("utf-8")
    p=p[1:-1]
    dat=[str(x) for x in p.split(',') if p.strip()]
    date=dat[0]
    time=dat[1]
    ts="20"+date[6:8]+"-"+date[3:5]+"-"+date[0:2]+"T"+time
    sensor=dat[2]
    temp=dat[4]
    dioxp=dat[5]
    diox=dat[6]

    t=Point("Sensor").tag("location",sensor).field("Temperature",float(temp)).time(ts,WritePrecision.S)
    d=Point("Sensor").tag("location",sensor).field("Dissolved Oxygen",float(diox)).time(ts,WritePrecision.S)
    with influx.write_api(write_options=SYNCHRONOUS) as wa:
        wa.write(bucket=os.environ.get("DB_BUCKET",record=t)
        wa.write(bucket=os.environ.get("DB_BUCKET",record=d)

conn=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
conn.on_connect=on_connect
conn.on_message=msg

conn.connect(os.environ.get("aquasensor_mqtt"),1883,60)

conn.loop_forever(retry_first_connection=False)
