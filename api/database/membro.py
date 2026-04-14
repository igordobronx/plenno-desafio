from pydantic import BaseModel, field_validator
from datetime import date
from typing import Literal

#aqui a gente vai fazer a validacao de entreada e saida da aPi

class MembroCreate(BaseModel):
    nome: str
    telefone: str
    ultima_presenca: date
    ultimo_dizim: date

    @field_validator("ultima_presenca", "ultimo_dizim", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v

class MembroResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    ultima_presenca: date
    ultimo_dizim: date

    model_config = {"from_attributes": True} #isso aq ta permitinod o pydantic ler e converter ORM

class MembroInativo(MembroResponse):
    dias_sem_presenca: int
    dias_sem_dizimo: int
    tipo_inatividade: Literal["presenca", "dizimo", "ambos"]

class AlertaRequest(BaseModel):
    membro_id: int

class AlertaResponse(BaseModel):
    membro_id: int
    nome: str
    tipo_inatividade: str
    timestamp: str