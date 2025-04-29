from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.v1.routes import router
from db.postgres.connection import create_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_database()
    yield


app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/docs.json",
    lifespan=lifespan,
)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
