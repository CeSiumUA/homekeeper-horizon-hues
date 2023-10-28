import pymongo
from env import Env

class MongoDbAccess:

    

    def __init__(self, mongo_url) -> None:
        self.__mongo_url = mongo_url

    def __enter__(self):
        self.__client = pymongo.MongoClient(self.__mongo_url)
        return self

    def __exit__(self, *args):
        self.__client.close()

    def __get_database(self):
        db_name = Env.get_mongo_db_name()
        if db_name is None:
            return None
        return self.__client[db_name]
    
    def __get_schedules_collection(self):
        db = self.__get_database()
        if db is None:
            return None
        collection_name = Env.get_mongo_schedules_coll_name()
        if collection_name is None:
            return None
        return db[collection_name]

    def get_timings(self):
        schedules_collection = self.__get_schedules_collection()
        if schedules_collection is None:
            return None
        return schedules_collection.find({})