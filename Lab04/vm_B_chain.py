import paho.mqtt.client as mqtt
import time

USERNAME = "mebeling"
PORT = 1883
BROKER = "172.20.10.3" 

def on_message(client, userdata, msg):
    number = int(msg.payload.decode()) + 1
    print(f"Received {msg.payload.decode()} on {msg.topic}, publishing {number} to {USERNAME}/pong")

    time.sleep(1)  # slow that jawn down
    client.publish(f"{USERNAME}/pong", str(number))

def on_connect(client, userdata, flags, rc):
    print(f"Connected. With rc code: {rc}")
    if rc == 0:
        client.subscribe(f"{USERNAME}/ping")
    else:
        print("Failed to connnect with rc:", rc)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"Errorr: {e}")
