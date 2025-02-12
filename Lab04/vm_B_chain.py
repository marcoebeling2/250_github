import paho.mqtt.client as mqtt
import time

USERNAME = "mebeling/"  # Replace with your actual username
BROKER = "http://broker.hivemq.com/"

def on_message(client, userdata, msg):
    """Handle incoming messages on 'ping' topic."""
    number = int(msg.payload.decode()) + 1
    print(f"Received {msg.payload.decode()} on {msg.topic}, publishing {number} to {USERNAME}/pong")

    time.sleep(1)  # Slow down the cycle
    client.publish(f"{USERNAME}/pong", str(number))

def on_connect(client, userdata, flags, rc):
    """Subscribe to the ping topic upon connection."""
    print(f"Connected with result code {rc}")
    client.subscribe(f"{USERNAME}/ping")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
