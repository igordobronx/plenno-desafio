import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from automacao.agente import rodar_agente

from api.database.database import init_db
from api.routes import membros

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")
scheduler.add_job(rodar_agente, "cron", hour=8, minute=0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(
    title="PLENNO - gestão de membros",
    description="monitoramento de menmbros inativos e dispara de alertas",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(membros.router)