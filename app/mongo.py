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
    empleos = mydb.query(models.Empleo).all()
    for empleo in empleos:
        await db.get_collection('jobs').update_many({"_id": empleo.id}, [{
            "$set": {
                "_id": empleo.id,
                "empresa": {
                    "nombre": empleo.empresa.nombre
                },
                "habilidades": empleo.habilidades.split(',')
            }
        }], upsert=True)
    # Insert documents into 'jobs' collection
    # await db.get_collection('jobs').update_many({}, [
    #     {
    #         "_id": 1,
    #         "empresa": {"nombre": "Tech Solutions"},
    #         "habilidades": ["Python", "SQL", "Docker"]
    #     },
    #     {
    #         "_id": 2,
    #         "empresa": {"nombre": "Salud Global"},
    #         "habilidades": ["Excel", "PowerBI", "SQL"]
    #     },
    #     {
    #         "_id": 3,
    #         "empresa": {"nombre": "Finanzas Hoy"},
    #         "habilidades": ["Python", "Excel"]
    #     },
    #     {
    #         "_id": 4,
    #         "empresa": {"nombre": "Educación Plus"},
    #         "habilidades": ["Python", "Zoom"]
    #     },
    #     {
    #         "_id": 5,
    #         "empresa": {"nombre": "AgroFuturo"},
    #         "habilidades": ["Agronomía", "Drones"]
    #     },
    #     {
    #         "_id": 6,
    #         "empresa": {"nombre": "EcoVida"},
    #         "habilidades": ["Medio Ambiente", "Drones"]
    #     },
    #     {
    #         "_id": 7,
    #         "empresa": {"nombre": "ConstruyeYa"},
    #         "habilidades": ["Gestión de Proyectos", "Drones"]
    #     },
    #     {
    #         "_id": 8,
    #         "empresa": {"nombre": "Viajes Mundo"},
    #         "habilidades": ["Atención al Cliente", "Drones"]
    #     },
    #     {
    #         "_id": 9,
    #         "empresa": {"nombre": "Legal Asesores"},
    #         "habilidades": ["Derecho", "Redacción"]
    #     },
    #     {
    #         "_id": 10,
    #         "empresa": {"nombre": "Arte Digital"},
    #         "habilidades": ["Photoshop", "Illustrator"]
    #     }
    # ], upsert=True)
    print("✅ creadas las collections")