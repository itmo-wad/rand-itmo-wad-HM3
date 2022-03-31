import pymongo
import os


class Config:
    # Connection
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/"
    CONNECTION = pymongo.MongoClient(CONNECTION_STRING)

    # Database name
    DATABASE = CONNECTION.get_database('ITMO')

    # Collections
    USERS_COLLECTION = DATABASE.users
    POSTS_COLLECTION = DATABASE.posts
