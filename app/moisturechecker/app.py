import paho.mqtt.client as mqtt
from gpiozero import Button as Sensor
import os


def on_event(client, topics, message):
    def func():
        for topic in topics:
            client.publish(topic, message)

    return func


if __name__ == '__main__':
    mqtt_url = os.environ['growmemoisturechecker_mqtturl']
    mqtt_topics = os.environ['growmemoisturechecker_mqtttopics'].split(",")
    sensor_pin = int(os.environ['growmemoisturechecker_sensor'])

    client = mqtt.Client("moisture_54263841")
    client.username_pw_set(mqtt_url.split("@")[0].split(":")[0], mqtt_url.split("@")[0].split(":")[1])
    client.connect(mqtt_url.split("@")[1].split(":")[0], int(mqtt_url.split("@")[1].split(":")[1]))

    sensor = Sensor(sensor_pin)
    sensor.when_pressed = on_event(client, mqtt_topics, "wet")
    sensor.when_released = on_event(client, mqtt_topics, "dry")

    client.loop_forever()
