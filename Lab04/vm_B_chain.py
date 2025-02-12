import paho.mqtt.client as mqtt
import time

USERNAME = "mebeling"  # Replace with your actual username
PORT = 1883
BROKER = "broker.hivemq.com"  # Corrected broker address

def on_message(client, userdata, msg):
    """Handle incoming messages on 'ping' topic."""
    number = int(msg.payload.decode()) + 1
    print(f"Received {msg.payload.decode()} on {msg.topic}, publishing {number} to {USERNAME}/pong")

    time.sleep(1)  # Slow down the cycle
    client.publish(f"{USERNAME}/pong", str(number))

def on_connect(client, userdata, flags, rc):
    """Subscribe to the ping topic upon connection."""
    print(f"Connected with result code {rc}")
    if rc == 0:
        client.subscribe(f"{USERNAME}/ping")
    else:
        print("Failed to connect, return code", rc)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Ensure correct broker format
try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"Connection error: {e}")
