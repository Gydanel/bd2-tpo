from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.server_api import ServerApi
import os

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL, server_api=ServerApi('1'))


def database() -> AsyncIOMotorDatabase:
    return client.get_database('tpo')


def users() -> AsyncIOMotorCollection:
    return database().get_collection('users')

def empleos() -> AsyncIOMotorCollection:
    return database().get_collection('empleos')
