from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.server_api import ServerApi
import os

import dependencies
import models

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL, server_api=ServerApi('1'))
db = client.get_database('tpo')

def database() -> AsyncIOMotorDatabase:
    return client.get_database('tpo')


def users() -> AsyncIOMotorCollection:
    return database().get_collection('users')

def jobs() -> AsyncIOMotorCollection:
    return database().get_collection('jobs')


async def start_up():
    mydb = next(dependencies.get_mysql_db())
    usuarios = mydb.query(models.Usuario).all()
    for user in usuarios:
        await db.get_collection('users').update_many({"_id": user.id}, [{
            "$set": {
                "_id": user.id,
                "fecha_registro": user.fecha_registro
            }
        }], upsert=True)


    empleos = mydb.query(models.Empleo).all()
    for empleo in empleos:
        await db.get_collection('jobs').update_many({"_id": empleo.id}, [{
            "$set": {
                "_id": empleo.id,
                "empresa": {
                    "nombre": empleo.empresa.nombre
                },
                "categoria": empleo.categoria,
                "habilidades": empleo.habilidades.split(',')
            }
        }], upsert=True)
    print("✅ creadas las collections")