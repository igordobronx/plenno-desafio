#aq a gnt constroi as rotas com as funcoes ja feitas na em services.membro_services.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.database.membro import MembroCreate, MembroInativo, MembroResponse, AlertaRequest, AlertaResponse
from api.services import membro_services

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/membros", tags=["Membros"])


@router.post("/", response_model=MembroResponse, status_code=status.HTTP_201_CREATED,)
def cadastrar_membro(dados:MembroCreate, db: Session = Depends(get_db)):
    membro = membro_services.criar_membro(db, dados)
    logger.info(f"membro cadastrado | id={membro.id} nome={membro.nome}")
    return membro

@router.get("/inativos", response_model=list[MembroInativo],)
def listar_membros_inativos(db: Session = Depends(get_db)):
    inativos = membro_services.listar_inativos(db)
    logger.info(f"consulta de inativos | total: {len(inativos)}")
    return inativos

@router.post("/alertas", response_model=AlertaResponse, status_code=status.HTTP_201_CREATED,)
def disparar_alerta(payload: AlertaRequest, db: Session = Depends(get_db)):
    alerta = membro_services.registrar_alerta(db, payload.membro_id)

    if not alerta:
        raise HTTPException(status_code=404, detail=f"membro {payload.membro_id} nao foi encontrado.")

    logger.info(
        f"alerta disparado | membro_id= {alerta.membro_id}"
        f"tipo={alerta.tipo_inatividade} | timestamp={alerta.timestamp}")
    
    return AlertaResponse(
        membro_id=alerta.membro_id,
        nome=alerta.membro.nome,
        tipo_inatividade=alerta.tipo_inatividade,
        timestamp=alerta.timestamp,
    )