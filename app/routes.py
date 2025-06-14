from datetime import datetime
from http.client import HTTPException

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from sqlalchemy.orm import Session
from starlette import status
from typing import List, Dict
from app.mongo import empleos  # o solo 'import mongo' si usás mongo.empleos()
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends


import schemas, models, mongo
import dependencies

router = APIRouter()

@router.get("/users")
async def read_users(
        mysqldb: Session = Depends(dependencies.get_mysql_db)
):
    users = mysqldb.query(models.User).all()
    return users


@router.post(
    path="/users",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user: schemas.UserCreate,
        mysqldb: Session = Depends(dependencies.get_mysql_db),
        users_collection: AsyncIOMotorCollection = Depends(mongo.users)
):
    # Check for existing email
    existing = mysqldb.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = models.User(name=user.name, email=user.email)
    mysqldb.add(new_user)
    mysqldb.commit()
    mysqldb.refresh(new_user)
    await users_collection.insert_one(
        schemas.UserDocument(user_id=new_user.id, registered_date=new_user.created_at).model_dump()
    )
    return new_user


@router.get("/usecase/total")
async def total_registered_users_by_year(
        users_collection: AsyncIOMotorCollection = Depends(mongo.users)
):
    since = datetime.now() - relativedelta(years=1)
    result = await users_collection.count_documents({
        "registered_date": {"$gte": since}
    })
    return {"total_registered_users": result, "time": since}

@router.get("/usecase/dos")
async def total_registered_users_by_year(
        users_collection: AsyncIOMotorCollection = Depends(mongo.users)
):
    result = await users_collection.find().to_list()
    return schemas.UserDocumentCollection(users=result)

@router.get("/empleos/habilidades-mas-solicitadas", response_model=List[Dict[str, int]])
async def habilidades_mas_solicitadas():
    pipeline = [
        {"$unwind": "$habilidades"},
        {"$group": {"_id": "$habilidades", "cantidad": {"$sum": 1}}},
        {"$sort": {"cantidad": -1}}
    ]
    cursor = empleos().aggregate(pipeline)
    resultados = []
    async for doc in cursor:
        resultados.append({"habilidad": doc["_id"], "cantidad": doc["cantidad"]})
    return resultados

@router.get("/usecase/empresas-activas")
async def empresas_que_mas_contratan(
    mysqldb: Session = Depends(dependencies.get_mysql_db)
):
    resultados = (
        mysqldb.query(
            models.Company.name.label("empresa"),
            func.count(models.Job.id).label("cantidad_empleos")
        )
        .join(models.Job, models.Job.company_id == models.Company.id)
        .group_by(models.Company.name)
        .order_by(func.count(models.Job.id).desc())
        .all()
    )
    return [{"empresa": r.empresa, "cantidad_empleos": r.cantidad_empleos} for r in resultados]