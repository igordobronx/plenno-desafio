import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.database.database import init_db
from api.routes import membros

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="PLENNO - gestão de membros",
    description="monitoramento de menmbros inativos e dispara de alertas",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(membros.router)