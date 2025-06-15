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
        document = {
            "_id": user.id,
            "fecha_registro": user.fecha_registro,
            "region": user.country,
        }
        await db.get_collection('users').update_many({"_id": user.id}, [{
            "$set": document
        }], upsert=True)


    empleos = mydb.query(models.Empleo).all()
    for empleo in empleos:
        document = {
            "_id": empleo.id,
            "empresa": {
                "nombre": empleo.empresa.nombre
            },
            "categoria": empleo.categoria,
            "habilidades": empleo.habilidades.split(',')
        }
        usuario_contratado = mydb.query(models.ApplicationAEmpleo).filter(
            models.ApplicationAEmpleo.empleo_id == empleo.id,
            models.ApplicationAEmpleo.estado == 'aceptado'
        ).first()
        if usuario_contratado:
            document['usuario_contratado'] = True
        await db.get_collection('jobs').update_many({"_id": empleo.id}, [{
            "$set": document
        }], upsert=True)
    print("✅ creadas las collections")