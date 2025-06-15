from contextlib import asynccontextmanager

from fastapi import FastAPI

import mongo, mysql, routes, neo

@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    # Startup logic
    mysql.start_up()
    await mongo.start_up()
    neo.start_up()
    yield  # Wait for app shutdown

app = FastAPI(
    lifespan=lifespan
)
app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "API is running"}
