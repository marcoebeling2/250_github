import paho.mqtt.client as mqtt
import time

USERNAME = "mebeling"  # Replace with your actual username
BROKER = "172.20.10.3"
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
    client.subscribe(f"{USERNAME}/pong")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_start()

# Publish the initial number
print(f"Publishing initial number {START_NUMBER} to {USERNAME}/ping")
client.publish(f"{USERNAME}/ping", str(START_NUMBER))

client.loop_forever()
