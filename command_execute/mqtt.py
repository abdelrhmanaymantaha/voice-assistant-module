import paho.mqtt.client as mqtt
import json  # For JSON serialization

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
            # Publish the message
            self.client.publish(self.topic, message)
            print(f"Message '{message}' published to topic '{self.topic}'")
        except Exception as e:
            print(f"An error occurred: {e}")

def mqtt_send(message: dict, username, password):
    """
    Helper function to send a JSON message via MQTT.

    :param message: A dictionary to be serialized into JSON.
    :param username: The username for authentication (optional).
    :param password: The password for authentication (optional).
    """
    mqtt_sender = MQTTSender(
        broker='broker.emqx.io',
        port=1883,
        topic='home/assistant',
        username=username,
        password=password
    )
    mqtt_sender.client.connect(mqtt_sender.broker, mqtt_sender.port)
    
    # Start the loop to process network traffic and dispatch callbacks
    mqtt_sender.client.loop_start()
    
    # Convert the dictionary to a JSON string
    json_message = json.dumps(message)
    
    # Send the JSON message
    mqtt_sender.send_message(json_message)
    
    # Give some time for the message to be sent
    mqtt_sender.client.loop_stop()
    mqtt_sender.client.disconnect()