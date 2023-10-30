import suntime
import datetime
from env import Env
import scheduler
import mqttmodule
import logging
from dailyevents import DailyEvent

def sunrise_event():
    mqttmodule.send_timing_event(DailyEvent.SUNRISE)

def custom_time_event():
    mqttmodule.send_timing_event(DailyEvent.CUSTOM_TIME)

def wakeup_event():
    mqttmodule.send_timing_event(DailyEvent.WAKEUP_TIME)

def bedtime_event():
    mqttmodule.send_timing_event(DailyEvent.BED_TIME)

def sunset_event():
    mqttmodule.send_timing_event(DailyEvent.SUNSET)

def zero_hour_event():
    sr, ss = calculate_dusk_dawn()
    
    tomorrow_zero_hour = get_tomorrow_zero_hour()

    scheduler.add_planned_job(sunrise_event, run_date=sr)
    scheduler.add_planned_job(sunset_event, run_date=ss)
    scheduler.add_planned_job(zero_hour_event, run_date=tomorrow_zero_hour)

def get_tomorrow_zero_hour(curr_datetime: datetime.datetime | None = None):
    if curr_datetime is None:
        curr_datetime = datetime.datetime.now()
    tomorrow = curr_datetime + datetime.timedelta(days=1)
    tomorrow_zero_hour = tomorrow.replace(hour=0, minute=1)
    return tomorrow_zero_hour

def calculate_dusk_dawn():
    lon, lat = Env.get_device_lon_lat()

    if lon is None:
        logging.fatal("longitude not set")
    lon = float(lon)

    if lat is None:
        logging.fatal("latitude not set")
    lat = float(lat)

    sun_obj = suntime.Sun(lat=lat, lon=lon)

    today = datetime.date.today()

    today_sunrise = sun_obj.get_local_sunrise_time(today)
    today_sunset = sun_obj.get_local_sunset_time(today)

    return today_sunrise, today_sunset

def get_nearest_event():
    sr, ss = calculate_dusk_dawn()

    current_datetime = datetime.datetime.now()

    if current_datetime.timestamp() < sr.timestamp():
        next_run = sr
        scheduled_fn = sunrise_event
    elif current_datetime.timestamp() > sr.timestamp() and current_datetime.timestamp() < ss.timestamp():
        next_run = ss
        scheduled_fn = sunset_event
    else:
        scheduled_fn = None
        next_run = None

    return scheduled_fn, next_run