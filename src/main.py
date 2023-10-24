import suntime
import datetime
import os
import logging
import random
from apscheduler.schedulers.background import BlockingScheduler
from paho.mqtt import client as mqtt_client
import topics

def get_lon_lat():
    longtitude = os.environ.get("DEVICE_LONGTITUDE")
    if longtitude is None:
        logging.fatal("longtitude not setted")
    longtitude = float(longtitude)

    latitude = os.environ.get("DEVICE_LATITUDE")
    if latitude is None:
        logging.fatal("latitude not setted")
    latitude = float(latitude)

    return longtitude, latitude

def on_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT")
    else:
        logging.fatal("Failed to connect to MQTT, return code: %d\n", rc)

def start_mqtt_client():
    global MQTT_CLIENT_INSTANCE
    broker_host = os.environ.get("MQTT_HOST")
    if broker_host is None:
        logging.fatal("broker host is empty")
    broker_port = os.environ.get("MQTT_PORT")
    if broker_port is None:
        broker_port = 1883
    else:
        broker_port = int(broker_port)

    client_id = "horizon-hues-{}".format(random.randint(0, 1000))

    MQTT_CLIENT_INSTANCE = mqtt_client.Client(client_id=client_id)
    MQTT_CLIENT_INSTANCE.on_connect = on_mqtt_connect
    MQTT_CLIENT_INSTANCE.connect(broker_host, broker_port)
    MQTT_CLIENT_INSTANCE.loop_start()

def calculate_dusk_dawn():
    lon, lat = get_lon_lat()

    sun_obj = suntime.Sun(lat=lat, lon=lon)

    today = datetime.date.today()

    today_sunrise = sun_obj.get_local_sunrise_time(today)
    today_sunset = sun_obj.get_local_sunset_time(today)

    return today_sunrise, today_sunset

def sunrise_event():
    MQTT_CLIENT_INSTANCE.publish(topic=topics.SEND_MESSAGE, payload="Sunrise is coming!")

def sunset_event():

    MQTT_CLIENT_INSTANCE.publish(topic=topics.SEND_MESSAGE, payload="Sunset is coming!")

    tomorrow_zero_hour = get_tomorrow_zero_hour()
    SCHEDULER.add_job(zero_hour_event, 'date', run_date=tomorrow_zero_hour)

def zero_hour_event():
    sr, ss = calculate_dusk_dawn()

    SCHEDULER.add_job(sunrise_event, 'date', run_date=sr)
    SCHEDULER.add_job(sunset_event, 'date', run_date=ss)

def get_tomorrow_zero_hour(curr_datetime: datetime.datetime | None = None):
    if curr_datetime is None:
        curr_datetime = datetime.datetime.now()
    tomorrow = curr_datetime + datetime.timedelta(days=1)
    tomorrow_zero_hour = tomorrow.replace(hour=0, minute=1)
    return tomorrow_zero_hour

def main():
    global SCHEDULER
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    start_mqtt_client()

    SCHEDULER = BlockingScheduler()
    
    sr, ss = calculate_dusk_dawn()

    current_datetime = datetime.datetime.now()

    if current_datetime.timestamp() < sr.timestamp():
        next_run = sr
        scheduled_fn = sunrise_event
    elif current_datetime.timestamp() > sr.timestamp() and current_datetime.timestamp() < ss.timestamp():
        next_run = ss
        scheduled_fn = sunset_event
    else:
        next_run = get_tomorrow_zero_hour(curr_datetime=current_datetime)
        scheduled_fn = zero_hour_event

    SCHEDULER.add_job(scheduled_fn, 'date', run_date=next_run)

    try:
        logging.info("starting scheduler...")
        SCHEDULER.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main()