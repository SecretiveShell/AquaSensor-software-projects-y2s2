import paho.mqtt.client as mqtt
import os

def on_connect(cl,dat,flags,r,p):
    cl.subscribe("sensor/#")

def msg(c,d,m):
    p=m.payload.decode("utf-8")
    p=p[1:-1]
    dat=[str(x) for x in p.split(',') if p.strip()]
    date=dat[0]
    time=dat[1]
    sensor=dat[2]
    temp=dat[4]
    dioxp=dat[5]
    diox=dat[6]

conn=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
conn.on_connect=on_connect
conn.on_message=msg

conn.connect(os.environ.get("aquasensor_mqtt"),1883,60)

conn.loop_forever(retry_first_connection=False)
