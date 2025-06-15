from datetime import datetime

import neo4j
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from sqlalchemy.orm import Session
from starlette import status

import schemas, models, mongo
import dependencies

router = APIRouter()

@router.get("/users")
async def read_users(
        mysqldb: Session = Depends(dependencies.get_mysql_db)
):
    users = mysqldb.query(models.Usuario).all()
    return users


@router.post(
    path="/users",
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user: schemas.UserCreate,
        mysqldb: Session = Depends(dependencies.get_mysql_db),
        users_collection: AsyncIOMotorCollection = Depends(mongo.users)
):
    # Check for existing email
    existing = mysqldb.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe el email registrado")

    # Create new user
    new_user = models.Usuario(
        nombre = user.nombre,
        email = user.email,
        foto_perfil = user.foto_perfil,
        telefono = user.telefono,
    )
    mysqldb.add(new_user)
    mysqldb.commit()
    mysqldb.refresh(new_user)
    await users_collection.insert_one(
        {
            "_id": user.id,
            "fecha_registro": user.fecha_registro
        }
    )
    return new_user


@router.get("/empresas")
async def read_corporation(
        mysqldb: Session = Depends(dependencies.get_mysql_db)
):
    empresas = mysqldb.query(models.Empresa).all()
    return empresas


@router.get("/empresas/{empresaId}")
async def read_corporation(
        empresaId: int,
        mysqldb: Session = Depends(dependencies.get_mysql_db)
):
    empresa = mysqldb.query(models.Empresa).filter(models.Empresa.id == empresaId).first()
    return empresa

@router.post(
    path="/empresas",
    status_code=status.HTTP_201_CREATED
)
async def create_corporation(
        empresa: schemas.EmpresaCreate,
        mysqldb: Session = Depends(dependencies.get_mysql_db),
):
    new_empresa = models.Empresa(
        nombre = empresa.nombre,
        descripcion = empresa.descripcion,
        ubicacion = empresa.ubicacion,
    )
    mysqldb.add(new_empresa)
    mysqldb.commit()
    mysqldb.refresh(new_empresa)
    return new_empresa


@router.get("/empresas/{empresaId}/empleos")
async def read_jobs(
        empresaId: int,
        mysqldb: Session = Depends(dependencies.get_mysql_db)
):
    empresa = mysqldb.query(models.Empresa).filter(models.Empresa.id == empresaId).first()
    return empresa.empleos


@router.post(
    path="/empresas/{empresaId}/empleos",
    status_code=status.HTTP_201_CREATED
)
async def create_job(
        empresaId: int,
        empleo: schemas.EmpleoCreate,
        mysqldb: Session = Depends(dependencies.get_mysql_db),
        jobs_collection: AsyncIOMotorCollection = Depends(mongo.jobs)
):

    new_empresa=models.Empleo(
        titulo=empleo.titulo,
        descripcion=empleo.descripcion,
        ubicacion=empleo.ubicacion,
        categoria=empleo.categoria,
        habilidades=','.join(empleo.habilidades),
        empresa_id=empresaId,
    )
    mysqldb.add(new_empresa)
    mysqldb.commit()
    mysqldb.refresh(new_empresa)
    # await jobs_collection.insert_one(
    #     schemas.UserDocument(user_id=new_job.id, registered_date=new_job.fecha_registro).model_dump()
    # )
    return new_empresa

@router.get("/usecase/one")
async def total_registered_users_by_year(
        users_collection: AsyncIOMotorCollection = Depends(mongo.users)
):
    since = datetime.now() - relativedelta(years=1)
    result = await users_collection.count_documents({
        "fecha_registro": {"$gte": since}
    })
    return {"total_registered_users": result, "time": since}

@router.get("/usecase/two")
async def habilidades_mas_solicitadas(
        jobs_collection: AsyncIOMotorCollection = Depends(mongo.jobs)
):
    result = await jobs_collection.aggregate([
        {"$unwind": "$habilidades"},
        {"$group": {"_id": "$habilidades", "count": { "$sum": 1 } } },
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]).to_list()
    return {"response": result }

@router.get("/usecase/three")
async def more_active_companies(
        jobs_collection: AsyncIOMotorCollection = Depends(mongo.jobs)
):
    result = await jobs_collection.aggregate([
        {
            "$match": {
                "usuario_contratado": { "$exists": True}
            }
        },
        {"$group": {"_id": "$empresa.nombre", "count": { "$sum": 1 } } },
        {"$sort": {"count": -1}},
        {"$limit": 5},
        {
            "$project": {
                "_id": 0,
                "empresa": "$_id",
                "count": "$count"
            }
        }
    ]).to_list()
    return {"response": result }

@router.get("/usecase/four")
async def recomendations_by_user(
        id: int,
        neo: neo4j.Driver = Depends(dependencies.get_neo4j_db)
):
    with neo.session() as session:
        result = session.run("""
            MATCH (:Empresa)-[r:RECOMMENDED]->(u:Usuario {id: $id})
            RETURN count(r) AS recommendations_count
        """, id=id)
        return {"total": result.single()["recommendations_count"] }

@router.get("/usecase/five")
async def users_by_region(
        users_collection: AsyncIOMotorCollection = Depends(mongo.users)
):
    result = await users_collection.aggregate([
        {
            "$group": {
                "_id": {
                    "region": "$region",
                    "month": {"$substr": ["$fecha_registro", 0, 7]}
                },
                "total": {"$sum": 1}
            }
        },
        {"$sort": {"_id.region": 1, "_id.month": 1} },
        {
            "$project": {
                "_id": 0,
                "region": "$_id.region",
                "month": "$_id.month",
                "total": "$total"
            }
        }
    ]).to_list()
    return {"response": result }

@router.get("/usecase/six")
async def users_with_friends_and_conn(
        conn: int,
        friends: int,
        neo: neo4j.Driver = Depends(dependencies.get_neo4j_db)
):
    with neo.session() as session:
        result = session.run("""
            MATCH (u:Usuario)-[:CONNECTED_TO]-(f:Usuario)
            WITH u, count(f) AS total_connections
            WHERE total_connections > $conn
    
            MATCH (u)-[:CONNECTED_TO]-(f1)-[:CONNECTED_TO]-(u2:Usuario)
            WHERE u <> u2 AND (u)-[:CONNECTED_TO]-(u2)
            WITH u, u2, count(DISTINCT f1) AS common_friends
            WHERE common_friends >= $friends
            RETURN DISTINCT u AS usuario, u2 As amigo
        """, conn=conn, friends=friends).fetch(10)
        return {"response": result }


@router.get("/usecase/seven")
async def habilidades_mas_solicitadas_en_marketing_o_tecnologia(
        jobs_collection: AsyncIOMotorCollection = Depends(mongo.jobs)
):
    result = await jobs_collection.aggregate([
        {
            "$match": {
                "categoria": {"$in": ["Tecnología", "Marketing"]}
            }
        },
        {
            "$group": {
                "_id": "$categoria",
                "habilidades": {
                    "$addToSet": "$habilidades"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "categoria": "$_id",
                "habilidades": {
                    "$reduce": {
                        "input": "$habilidades",
                        "initialValue": [],
                        "in": {
                            "$setUnion": [
                                "$$value",
                                "$$this"
                            ]
                        }
                    }
                }
            }
        }
    ]).to_list()
    return {"response": result }