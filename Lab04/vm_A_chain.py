import paho.mqtt.client as mqtt
import time

USERNAME = "mebeling" 
PORT = 1883
BROKER = "172.20.10.3"
START_NUMBER = 1  # first number

def on_message(client, userdata, msg):
    number = int(msg.payload.decode()) + 1
    print(f"Received {msg.payload.decode()} on {msg.topic}, publishing {number} to {USERNAME}/ping")

    time.sleep(1)  # make it wait . SLEEP!
    client.publish(f"{USERNAME}/ping", str(number))

def on_connect(client, userdata, flags, rc):
    print(f"Connected. RC: {rc}")
    if rc == 0:
        client.subscribe(f"{USERNAME}/pong")
    else:
        print("Failed to connect. RC: ", rc)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.reconnect_delay_set(min_delay=1, max_delay=10)

try:
    client.connect(BROKER, PORT, 60)
    print(f"Sending this, {START_NUMBER}, to {USERNAME}/ping")
    client.publish(f"{USERNAME}/ping", str(START_NUMBER))
    client.loop_forever()
except Exception as e:
    print(f"Error: {e}")


