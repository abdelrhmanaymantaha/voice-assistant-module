import paho.mqtt.client as mqtt
import json
import time  # For adding delays

class MQTTSender:
    def __init__(self, broker, port, topic, username=None, password=None):
        """
        Initialize the MQTT sender.

        :param broker: The broker's address (e.g., 'broker.emqx.io').
        :param port: The broker's port (default is 1883).
        :param topic: The MQTT topic to publish messages to.
        :param username: The username for authentication (optional).
        :param password: The password for authentication (optional).
        """
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.client = mqtt.Client()

        # Assign the connection callback
        self.client.on_connect = self.on_connect

        # Set username and password if provided
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback function for connection.
        """
        if rc == 0:
            print("Connected to broker successfully!")
        else:
            print(f"Connection failed with code {rc}")

    def send_message(self, message):
        """
        Send a message to the specified MQTT topic.

        :param message: The message to publish (can be a string or JSON).
        """
        try:
            # If the message is a dictionary, convert it to JSON
            if isinstance(message, dict):
                message = json.dumps(message)
            
            # Publish the message
            self.client.publish(self.topic, message)
            print(f"Message '{message}' published to topic '{self.topic}'")
        except Exception as e:
            print(f"An error occurred: {e}")

def mqtt_send(message: dict, username, password, topic: str) -> None:
    """
    Helper function to send a JSON message via MQTT.

    :param message: A dictionary to be serialized into JSON.
    :param username: The username for authentication (optional).
    :param password: The password for authentication (optional).
    :param topic: The MQTT topic to publish the message to.
    """
    mqtt_sender = MQTTSender(
        broker='broker.emqx.io',
        port=1883,
        topic=topic,
        username=username,
        password=password
    )
    mqtt_sender.client.connect(mqtt_sender.broker, mqtt_sender.port)
    
    # Start the loop to process network traffic and dispatch callbacks
    mqtt_sender.client.loop_start()
    time.sleep(2)  # Wait for 1 second to ensure the connection is established
    
    # Send the message
    mqtt_sender.send_message(message)
    
    # Stop the loop and disconnect
    mqtt_sender.client.loop_stop()
    mqtt_sender.client.disconnect()