from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy.orm import Session

import models
import mysql
import schemas
import mongo

@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    # Startup logic
    mysql.start_up()
    yield  # Wait for app shutdown

app = FastAPI(lifespan=lifespan)

# Dependency
def get_db():
    db = mysql.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check for existing email
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/test")
async def test(mongodb: AsyncIOMotorDatabase = Depends(mongo.database)):
    await mongodb.client.admin.command("ping")
    return { "result": "MongoDB connection successful" }