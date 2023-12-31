import logging
from paho.mqtt import client as mqtt_client
import topics
import random
from dailyevents import DailyEvent
from env import Env

def __on_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT")
    else:
        logging.fatal("Failed to connect to MQTT, return code: %d\n", rc)

def send_timing_event(event_type: DailyEvent):
    MQTT_CLIENT_INSTANCE.publish(topic=topics.TIMING_EVENT, payload=event_type.value, qos=2)
    
    if Env.get_publish_to_tg():
        MQTT_CLIENT_INSTANCE.publish(topic=topics.SEND_MESSAGE, payload=f"event {event_type.name} is coming")

def start_mqtt_client(broker_host: str, broker_port: int, broker_username : str | None = None, broker_password: str | None = None):
    global MQTT_CLIENT_INSTANCE

    client_id = "horizon-hues-{}".format(random.randint(0, 1000))

    MQTT_CLIENT_INSTANCE = mqtt_client.Client(client_id=client_id)
    MQTT_CLIENT_INSTANCE.on_connect = __on_mqtt_connect
    MQTT_CLIENT_INSTANCE.username_pw_set(broker_username, broker_password)
    MQTT_CLIENT_INSTANCE.connect(broker_host, broker_port)
    MQTT_CLIENT_INSTANCE.loop_start()

