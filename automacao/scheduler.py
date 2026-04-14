import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.schedulers.blocking import BlockingScheduler
from automacao.agente import rodar_agente

scheduler = BlockingScheduler(timezone="America/Sao_paulo")

@scheduler.scheduled_job("cron", hour=8, minute=0)
def job_diario():
    print("scheduler iniciado  -- verificando membros inativos...")
    rodar_agente()

if __name__ == "__main__":
    print("Agendador rodando, todas execcucaoes acontecem todos os dias as 8h")
    scheduler.start()