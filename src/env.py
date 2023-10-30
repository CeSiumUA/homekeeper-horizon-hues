from os import environ
import logging

class Env:

    MQTT_HOST = "MQTT_HOST"
    MQTT_PORT = "MQTT_PORT"
    MQTT_USERNAME = "MQTT_USERNAME"
    MQTT_PASSWORD = "MQTT_PASSWORD"
    MONGO_URL = "MONGO_URL"
    MONGO_HOMEKEEPER_DB = "MONGO_HOMEKEEPER_DB"
    MONGO_SCHEDULES_COLL = "MONGO_SCHEDULES_COLL"
    DEVICE_LON = "DEVICE_LONGITUDE"
    DEVICE_LAT = "DEVICE_LATITUDE"
    PUBLISH_TO_TG = "PUBLISH_TO_TG"

    def get_mqtt_connection_params():
        broker_host = environ.get(Env.MQTT_HOST)
        broker_port = environ.get(Env.MQTT_PORT)
        if broker_port is None:
            broker_port = 1883
        else:
            broker_port = int(broker_port)

        broker_username = environ.get(Env.MQTT_USERNAME)
        broker_password = environ.get(Env.MQTT_PASSWORD)

        return broker_host, broker_port, broker_username, broker_password
        
    def get_mongo_connection_url():
        mongo_url = environ.get(Env.MONGO_URL)
        return mongo_url
    
    def get_mongo_db_name():
        return environ.get(Env.MONGO_HOMEKEEPER_DB)
    
    def get_mongo_schedules_coll_name():
        return environ.get(Env.MONGO_SCHEDULES_COLL)

    def get_device_lon_lat():
        lon = environ.get(Env.DEVICE_LON)
        lat = environ.get(Env.DEVICE_LAT)

        return lon, lat
    
    def get_publish_to_tg():
        publish_to_tg = environ.get(Env.PUBLISH_TO_TG)

        if publish_to_tg is None:
            return False
        
        return int(publish_to_tg) == 1