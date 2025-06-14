from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

import mongo, mysql, schemas, routes

@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    # Startup logic
    mysql.start_up()
    yield  # Wait for app shutdown

app = FastAPI(
    lifespan=lifespan
)
app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get(
    path="/test",
    response_description="Get a single student",
    response_model=schemas.ExampleCollection,
    response_model_by_alias=False,
)
async def test(mongodb: AsyncIOMotorDatabase = Depends(mongo.database)):
    await mongodb.get_collection("example").insert_one({"test": "data"})
    result = await mongodb.get_collection("example").find().to_list()
    return schemas.ExampleCollection(examples=result)