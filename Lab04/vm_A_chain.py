import paho.mqtt.client as mqtt
import time

USERNAME = "mebeling"  # Replace with your actual username
PORT = 1883
BROKER = "broker.hivemq.com"
START_NUMBER = 1  # Initial number to start the ping-pong sequence

def on_message(client, userdata, msg):
    """Handle incoming messages on 'pong' topic."""
    number = int(msg.payload.decode()) + 1
    print(f"Received {msg.payload.decode()} on {msg.topic}, publishing {number} to {USERNAME}/ping")

    time.sleep(1)  # Slow down the cycle
    client.publish(f"{USERNAME}/ping", str(number))

def on_connect(client, userdata, flags, rc):
    """Subscribe to the pong topic upon connection."""
    print(f"Connected with result code {rc}")
    if rc == 0:
        client.subscribe(f"{USERNAME}/pong")
    else:
        print("Failed to connect, return code", rc)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.reconnect_delay_set(min_delay=1, max_delay=10)  # Prevent aggressive reconnections

try:
    client.connect(BROKER, PORT, 60)
    print(f"Publishing initial number {START_NUMBER} to {USERNAME}/ping")
    client.publish(f"{USERNAME}/ping", str(START_NUMBER))
    client.loop_forever()
except Exception as e:
    print(f"Connection error: {e}")
