from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Membro(Base):
    __tablename__ = "membros"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)
    telefone: str = Column(String(20), nullable=False)
    ultima_presenca = Column(Date, nullable=False)
    ultimo_dizim = Column(Date, nullable=False)

    alertas = relationship("Alerta", back_populates="membro")

class Alerta(Base):
    __tablename__ = "alertas"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    membro_id: int = Column(Integer, ForeignKey("membros.id"), nullable=False)
    tipo_inatividade: str = Column(Text, nullable=True)
    mensagem: str = Column(Text, nullable=True)
    timestamp: str = Column(String(30), nullable=False)

    membro = relationship("Membro", back_populates="alertas")