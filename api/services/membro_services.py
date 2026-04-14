from datetime import date, timedelta
from typing import Literal
from sqlalchemy.orm import Session

from api.database.models import Membro, Alerta
from api.database.membro import MembroCreate, MembroInativo


LIMITE = 30 #isso aq fica de regra de negocio (engenharia de software, meu curso), se caso necessita de mudança, apenas mudar aqui e já é automaticamente alterado

def _calcular_tipo_inatividade(dias_presenca: int, dias_dizimo: int) -> Literal["presenca", "dizimo", "ambos"] | None:
    inativo_presenca = dias_presenca > LIMITE
    inativo_dizimo = dias_dizimo > LIMITE

    if inativo_dizimo and inativo_presenca:
        return "ambos"

    if inativo_dizimo:
        return "dizimo"

    if inativo_presenca:
        return "presenca"

    return None

def criar_membro(db: Session, dados: MembroCreate) -> Membro:
    membro = Membro(nome=dados.nome, telefone=dados.telefone, ultima_presenca=dados.ultima_presenca, ultimo_dizim=dados.ultimo_dizim)

    db.add(membro)
    db.commit()
    db.refresh(membro)
    return membro


def listar_inativos(db: Session) -> list[MembroInativo]:
    hoje = date.today()
    corte = hoje - timedelta(days=LIMITE)

    membros = (
        db.query(Membro).filter(
            (Membro.ultima_presenca < corte) | (Membro.ultimo_dizim < corte)
        ).all()
    )
    resultado = []
    for m in membros:
        dias_presenca = (hoje - m.ultima_presenca).days
        dias_dizimo = (hoje - m.ultimo_dizim).days
        tipo = _calcular_tipo_inatividade(dias_presenca, dias_dizimo)

        resultado.append(
            MembroInativo(
                id=m.id,
                nome=m.nome,
                telefone=m.telefone,
                ultima_presenca=m.ultima_presenca,
                ultimo_dizim=m.ultimo_dizim,
                dias_sem_presenca=dias_presenca,
                dias_sem_dizimo=dias_dizimo,
                tipo_inatividade=tipo,
            )
        )
    return resultado


def registrar_alerta(db: Session, membro_id: int, ) -> Alerta:

    membro = db.query(Membro).filter(Membro.id == membro_id).first()

    if not membro:
        return None

    hoje = date.today()
    dias_presenca = (hoje - membro.ultima_presenca).days
    dias_dizimo = (hoje - membro.ultimo_dizim).days
    tipo = _calcular_tipo_inatividade(dias_presenca, dias_dizimo)

    alerta = Alerta(
        membro_id=membro_id,
        tipo_inatividade=tipo or "indefinido",
        timestamp=hoje.isoformat(),
    )

    db.add(alerta)
    db.commit()
    db.refresh(alerta)
    return alerta

