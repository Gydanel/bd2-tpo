from datetime import datetime

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
        schemas.UserDocument(user_id=new_user.id, registered_date=new_user.fecha_registro).model_dump()
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
        users_collection: AsyncIOMotorCollection = Depends(mongo.users)
):

    new_empresa=models.Empleo(
        titulo=empleo.titulo,
        descripcion=empleo.descripcion,
        ubicacion=empleo.ubicacion,
        habilidades=','.join(empleo.habilidades),
        empresa_id=empresaId,
    )
    mysqldb.add(new_empresa)
    mysqldb.commit()
    mysqldb.refresh(new_empresa)
    # await users_collection.insert_one(
    #     schemas.UserDocument(user_id=new_job.id, registered_date=new_job.fecha_registro).model_dump()
    # )
    return new_empresa

@router.get("/usecase/one")
async def total_registered_users_by_year(
        users_collection: AsyncIOMotorCollection = Depends(mongo.users)
):
    since = datetime.now() - relativedelta(years=1)
    result = await users_collection.count_documents({
        "registered_date": {"$gte": since}
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