from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from core.config import settings


class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(300), nullable=True)
    email = Column(String(300), index=True, nullable=False, unique=True)
    senha = Column(String(300), nullable=False)
    ativo = Column(Boolean, default=True)
    grupo_id = Column(Integer, ForeignKey('grupos.id'))

    grupo = relationship(
        "GrupoModel",
        back_populates='usuarios',
        lazy='joined'
    )

