import chrono
import logging
import mqttmodule
import scheduler
from env import Env
from dbaccess import MongoDbAccess
from dailyevents import DailyEvent

def main():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    broker_host, broker_port = Env.get_mqtt_connection_params()
    if broker_host is None:
        logging.fatal("broker host is empty")
    
    mongo_url = Env.get_mongo_connection_url()
    if mongo_url is None:
        logging.fatal("mongo url is empty")

    mqttmodule.start_mqtt_client(broker_host=broker_host, broker_port=broker_port)

    with MongoDbAccess(mongo_url=mongo_url) as mongo_db_access:

        cursor = mongo_db_access.get_timings()
        if cursor is None:
            logging.fatal("error to get mongo collection")

        for schedule in cursor:
            if DailyEvent(schedule["type"]) == DailyEvent.WAKEUP_TIME:
                job = chrono.wakeup_event
            elif DailyEvent(schedule["type"]) == DailyEvent.BED_TIME:
                job = chrono.bedtime_event
            else:
                job = chrono.custom_time_event

            scheduler.add_cron_job(job, schedule["hour"], schedule["minute"])

    nearest_job, date = chrono.get_nearest_event()
    if nearest_job is not None and date is not None:
        scheduler.add_planned_job(nearest_job, date)

    zero_hour_job_date = chrono.get_tomorrow_zero_hour()

    scheduler.add_planned_job(chrono.zero_hour_event, zero_hour_job_date)

    logging.info("starting scheduler")
    scheduler.start_scheduler()
    logging.info("scheduler finished")

if __name__ == '__main__':
    main()